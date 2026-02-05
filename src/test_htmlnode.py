import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
    def test_eq(self):
        node = HTMLNode("a","b","c","d")
        node2 = HTMLNode("a","b","c","d")
        self.assertEqual(node, node2)
    def test_noteq(self):
        node = HTMLNode("a","b","c",{})
        node2 = HTMLNode("a","b","c")
        self.assertNotEqual(node,node2)
if __name__ == "__main__":
    unittest.main()