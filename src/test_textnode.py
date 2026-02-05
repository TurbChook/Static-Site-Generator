import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_type(self):
        node = TextNode("This is not a test", TextType.ITALIC)
        node2 = TextNode("This is not a test", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_url(self):
        node = TextNode("URL test", TextType.LINK, "not an url")
        node2 = TextNode("URL test", TextType.LINK)
        self.assertNotEqual(node, node2)
    def test_url2(self):
        node = TextNode("URL test", TextType.LINK, None)
        node2 = TextNode("URL test", TextType.LINK)
        self.assertEqual(node,node2)
if __name__ == "__main__":
    unittest.main()