
import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        tn = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        node_italic = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, tn)
        self.assertNotEqual(node, node_italic)


if __name__ == "__main__":
    unittest.main()
