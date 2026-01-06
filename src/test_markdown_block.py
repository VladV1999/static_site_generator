import unittest

from markdown_block import MarkdownBlock, block_to_block, markdown_to_html_node, markdown_to_blocks, markdown_block_to_tag
from markdown_block import stripped_markdown_string, ulist_to_stripped_markdown_string, olist_to_stripped_markdown_string
from htmlnode import LeafNode, ParentNode, HTMLNode
class TestMarkdownBlock(unittest.TestCase):
    def test_markdown_block_basic(self):
        markdown_string = """- List item 1
- List item 2
- List item 3"""
        result = block_to_block(markdown_string)
        self.assertEqual(result, MarkdownBlock.UNORDERED_LIST)


    def test_markdown_block_invalid_input(self):
        markdown_string = """- List item 1
- List item 2
- List item 3
invalid input test"""
        result = block_to_block(markdown_string)
        self.assertEqual(result, MarkdownBlock.PARAGRAPH)

    def test_markdown_block_ordered_list(self):
        markdown_string = """1. List item 1
2. List item 2
3. List item 3
4. List item 4"""
        result = block_to_block(markdown_string)
        self.assertEqual(result, MarkdownBlock.ORDERED_LIST)

    def test_markdown_block_heading(self):
        markdown_string = """# List item 1
        ## List item 2"""
        result = block_to_block(markdown_string)
        self.assertEqual(result, MarkdownBlock.HEADING)

    def test_markdown_block_heading_invalid(self):
        markdown_string = """# List item 1 checking for heading"""
        result = block_to_block(markdown_string)
        self.assertEqual(result, MarkdownBlock.HEADING)

    def test_markdown_block_quote(self):
        markdown_string = """> List item 1
> List item 2
> List item 3
> List item 4"""
        result = block_to_block(markdown_string)
        self.assertEqual(result, MarkdownBlock.QUOTE)

    def test_markdown_block_code(self):
        markdown_string = """``` this is
testing to see
if some arbitrary string with ticks
passes as code```"""
        result = block_to_block(markdown_string)
        self.assertEqual(result, MarkdownBlock.CODE)

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