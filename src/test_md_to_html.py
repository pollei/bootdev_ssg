
import unittest
from htmlnode import HtmlNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from md_to_html import *


class TestMDToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("url node", TextType.LINK, "https://junk/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "url node")
        self.assertEqual(html_node.props["href"], "https://junk/")
        self.assertEqual(html_node.to_html(),
            '<a href="https://junk/">url node</a>')
    def test_img(self):
        node = TextNode("img node", TextType.IMAGE, "https://junk/pretty")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        #self.assertEqual(html_node.value, "img node")
        self.assertEqual(html_node.props["src"], "https://junk/pretty")
        self.assertEqual(html_node.props["alt"], "img node")
        self.assertEqual(html_node.to_html(),
            '<img src="https://junk/pretty" alt="img node">')
    def test_md2html_line_to_textnodes(self):
        ret = line_to_textnodes("This is text with a `code block` word")
        #print(f"{ret=}")
        ret = line_to_textnodes("This is text with a `code block` and a **bolded phrase**")
        #print(f"{ret=}")
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)" )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"),
             ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
             [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
              ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
    @unittest.skip("used different way that doesn't use this at all")
    def test_split_images(self):
        # return # used different way that doesn't use this at all
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN, )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode( "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"  ), 
            ], new_nodes,  )
    def test_text_to_textnodes(self):
        text = ("This is **text** with an _italic_ word and a `code block` and" +
            " an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),] , nodes,  )
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        #print("blck tests")
        hblk = "# This is a heading"
        self.assertEqual(block_to_block_type(hblk), BlockType.HEADING)
        lblk = """
- This is the first list item in a list block
- This is a list item
- This is another list item
""".strip()
        self.assertTrue(lblk.startswith("- "))
        lblk_type = block_to_block_type(lblk)
        #print(f"{lblk=} {lblk_type=}") 
        self.assertEqual( lblk_type , BlockType.UNORDERED_LIST)
        lblk = """
1. This is the first list item in a list block
2. This is a list item
3. This is another list item
""".strip()
        self.assertTrue(lblk.startswith("1. "))
        self.assertEqual(block_to_block_type(lblk), BlockType.ORDERED_LIST)
        for blck in blocks:
            blk_type = block_to_block_type(blck)
            #print(f"{blck=} {blk_type=}")
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_markdown_specials_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

1. first things first
2.    .....
3. profit

>this could be a blockquote
>we shall see
> seems like it smashes together if not done right
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            #print(f"{html=}")
            self.assertTrue(len(html) > 50)







    
if __name__ == "__main__":
    unittest.main()