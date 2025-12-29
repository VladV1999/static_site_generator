import unittest

from htmlnode import HTMLNode

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