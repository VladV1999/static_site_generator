import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "testtest")
        node2 = HTMLNode("p", "testtest")
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = HTMLNode("p", "testtest")
        node2 = HTMLNode("p", "testtestt")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = HTMLNode("p", "this is a test node")
        self.assertEqual("HTMLNode(p, this is a test node, None, None)", repr(node))

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode("p", "testing the string", props=None)
        node2 = LeafNode("p", "testing the string", props=None)
        self.assertEqual(node1, node2)
    def test_not_eq(self):
        node1 = LeafNode("p", "testing the stringggg", props=None)
        node2 = LeafNode("p", "testing the string", props=None)
        self.assertNotEqual(node1, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!", props=None)
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_repr(self):
        node = LeafNode("p", "Hello, World!", props=None)
        self.assertEqual(
            "LeafNode(p, Hello, World!, None)", repr(node)
        )