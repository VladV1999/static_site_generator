import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode
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
    
class TestParentNode(unittest.TestCase):
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
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_with_props_and_child(self):
        child = LeafNode("span", "hi")
        parent = ParentNode("div", [child], {"class": "box", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div> class="box" id="main"<span>hi</span></div>',
        )
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_diff(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertNotEqual(html_node.tag, "test")
        self.assertNotEqual(html_node.value, "This is a meant to be wrong node")

    def test_link(self):
        node = TextNode("This is a text node w a link",
                        TextType.LINK, "www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node w a link")
        self.assertEqual(html_node.props, {'href': 'www.boot.dev'})

    def test_img(self):
        node = TextNode("This is a text node w an image",
                        TextType.IMAGE, "www.boot.dev/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "www.boot.dev/image.png")
        self.assertEqual(html_node.props["alt"], "This is a text node w an image")