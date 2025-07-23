
import unittest
from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_junk(self):
        body_node=HtmlNode("body")
        a_node= HtmlNode("a", props = {
            "href": "https://www.boot.dev" })
        #print(f"{a_node=} {a_node.props_to_html()=}")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        hello_p = LeafNode("p", "Hello, world!")
        self.assertEqual(hello_p.to_html(), "<p>Hello, world!</p>")
        google_a =LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        #print(f"{google_a=}")
        self.assertEqual(google_a.to_html(),'<a href="https://www.google.com">Click me!</a>')
        empty_text=LeafNode()
        self.assertEqual(empty_text.to_html(),"")


class TestLeafNode(unittest.TestCase):
    def parent_node_empty_children(self):
        node = ParentNode( "p",  [])
        self.assertEqual(node.to_html(),
            "<p></p>")
    def parent_node_one_layer(self):
        node = ParentNode( "p",  [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"), ] )
        self.assertEqual(node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"  )
    def parent_node_with_props(self):
        node = ParentNode( "div",  [
             ParentNode( "p",  [
                LeafNode("a", "Click me!", {"href": "https://www.google.com"}) ])
        ], { "id": "x"})
        self.assertEqual(
            node.to_html(),
            '<div id="x"><p><a href="https://www.google.com">Click me!</a></p></div>'  )

    
if __name__ == "__main__":
    unittest.main()
