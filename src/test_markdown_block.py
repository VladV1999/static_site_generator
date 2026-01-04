import unittest

from markdown_block import MarkdownBlock, block_to_block

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
        markdown_string = """# List item 1"""
        result = block_to_block(markdown_string)
        self.assertEqual(result, MarkdownBlock.HEADING)

    def test_markdown_block_heading_invalid(self):
        markdown_string = """# List item 1
        checking for heading"""
        result = block_to_block(markdown_string)
        self.assertNotEqual(result, MarkdownBlock.HEADING)

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