import unittest

from split_nodes_with_delimeter import split_nodes_delimeter, split_nodes_image
from textnode import TextNode, TextType

class TestSplitNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)
        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ], new_nodes)

    def test_eq_with_multiple_blocks(self):
        node = TextNode("This is a text with `code block`" \
        "and another `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)
        self.assertEqual([
            TextNode("This is a text with ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode("and another ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ], new_nodes)

    def test_unbalanced_backticks_raises(self):
        node = TextNode("This is a `broken code block", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimeter([node], "`", TextType.CODE)

    def test_diff_type_of_text_type(self):
        node = TextNode("`This is a code block`", TextType.CODE)
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)
        self.assertEqual([
            TextNode("`This is a code block`", TextType.CODE)
        ], new_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )