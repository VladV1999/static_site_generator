import unittest

from split_nodes_with_delimeter import split_nodes_delimeter, split_nodes_image, split_nodes_links, text_to_textnodes
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
    
    def test_split_links(self):
        node = TextNode(
            "This is a link with [link](https://docs.python.org/3/library/re.html)",
            TextType.TEXT
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is a link with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://docs.python.org/3/library/re.html")
            ]
        , new_nodes)

    def test_split_links_multiple(self):
        node = TextNode(
            "This is a link with [link](https://docs.python.org/3/library/re.html) and some other [link](https://www.youtube.com/watch?v=X-6riincY-0&list=RDX-6riincY-0&start_radio=1)",
            TextType.TEXT
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is a link with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://docs.python.org/3/library/re.html"),
                TextNode(" and some other ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.youtube.com/watch?v=X-6riincY-0&list=RDX-6riincY-0&start_radio=1")
            ]
        , new_nodes)

    def test_split_links_multiple_text_left_at_end(self):
        node = TextNode(
            "This is a link with [link](https://docs.python.org/3/library/re.html) and some other [link](https://www.youtube.com/watch?v=X-6riincY-0&list=RDX-6riincY-0&start_radio=1) and some good ol leftover text at the end",
            TextType.TEXT
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is a link with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://docs.python.org/3/library/re.html"),
                TextNode(" and some other ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.youtube.com/watch?v=X-6riincY-0&list=RDX-6riincY-0&start_radio=1"),
                TextNode(" and some good ol leftover text at the end", TextType.TEXT)
            ]
            , new_nodes
        )

    def test_split_links_with_link_at_beginning(self):
        node = TextNode(
            "[link](somelink.https://helloworld) This is a link with [link](https://docs.python.org/3/library/re.html) and some other [link](https://www.youtube.com/watch?v=X-6riincY-0&list=RDX-6riincY-0&start_radio=1) and some good ol leftover text at the end",
            TextType.TEXT
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "somelink.https://helloworld"),
                TextNode(" This is a link with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://docs.python.org/3/library/re.html"),
                TextNode(" and some other ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.youtube.com/watch?v=X-6riincY-0&list=RDX-6riincY-0&start_radio=1"),
                TextNode(" and some good ol leftover text at the end", TextType.TEXT)
            ]
        , new_nodes)

    def test_split_links_with_multiple_nodes(self):
        node1 = TextNode(
            "[link](somelink.https://helloworld) This is a link with [link](https://docs.python.org/3/library/re.html) and some other [link](https://www.youtube.com/watch?v=X-6riincY-0&list=RDX-6riincY-0&start_radio=1) and some good ol leftover text at the end",
            TextType.TEXT
        )
        node2 = TextNode(
            "Something simple [to be tested](as a link)", TextType.TEXT
        )
        list_of_nodes = [node1, node2]
        new_nodes = split_nodes_links(list_of_nodes)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "somelink.https://helloworld"),
                TextNode(" This is a link with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://docs.python.org/3/library/re.html"),
                TextNode(" and some other ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.youtube.com/watch?v=X-6riincY-0&list=RDX-6riincY-0&start_radio=1"),
                TextNode(" and some good ol leftover text at the end", TextType.TEXT),
                TextNode("Something simple ", TextType.TEXT),
                TextNode("to be tested", TextType.LINK, "as a link")
            ]
        , new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ]
        , nodes)