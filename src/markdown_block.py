from enum import Enum

class MarkdownBlock(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block(markdown_block):
    lines = markdown_block.split("\n")
    if len(lines) == 1 and markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return MarkdownBlock.HEADING
    elif len(lines) > 1 and markdown_block.startswith("```") and markdown_block.endswith("```"):
        return MarkdownBlock.CODE
    elif markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return MarkdownBlock.PARAGRAPH
        return MarkdownBlock.QUOTE
    elif markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return MarkdownBlock.PARAGRAPH
        return MarkdownBlock.UNORDERED_LIST
    elif markdown_block.startswith("1. "):
        count = 1
        for line in lines:
            if not line.startswith(f"{count}. "):
                return MarkdownBlock.PARAGRAPH
            else:
                count += 1
        return MarkdownBlock.ORDERED_LIST
    return MarkdownBlock.PARAGRAPH