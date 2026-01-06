from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType
from split_nodes_with_delimeter import text_to_textnodes
class MarkdownBlock(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block(markdown_block):
    lines = markdown_block.split("\n")
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return MarkdownBlock.HEADING
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for i in range(len(blocks)):
        if len(blocks[i]) == 0:
            continue
        block = blocks[i].strip()
        result.append(block)
    return result

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    children = []
    for block in markdown_blocks:
        type_of_block = block_to_block(block)
        match type_of_block:
            case MarkdownBlock.PARAGRAPH:
                content = stripped_markdown_string(MarkdownBlock.PARAGRAPH, block)
                tag = markdown_block_to_tag(MarkdownBlock.PARAGRAPH, block)
                list_text_children = text_to_children(content)
                paragraph_node = ParentNode(tag, list_text_children)
                children.append(paragraph_node)
            case MarkdownBlock.QUOTE:
                content = stripped_markdown_string(MarkdownBlock.QUOTE, block)
                tag = markdown_block_to_tag(MarkdownBlock.QUOTE, block)
                list_text_children = text_to_children(content)
                quote_node = ParentNode(tag, list_text_children)
                children.append(quote_node)
            case MarkdownBlock.HEADING:
                content = stripped_markdown_string(MarkdownBlock.HEADING, block)
                tag = markdown_block_to_tag(MarkdownBlock.HEADING, block)
                list_text_children = text_to_children(content)
                heading_node = ParentNode(tag, list_text_children)
                children.append(heading_node)
            case MarkdownBlock.CODE:
                content = stripped_markdown_string(MarkdownBlock.CODE, block)
                tag = markdown_block_to_tag(MarkdownBlock.CODE, block)
                leaf_node = LeafNode(None, content)
                code_tag_parent_node = ParentNode("code", [leaf_node])
                pre_tag_parent_node = ParentNode(tag, [code_tag_parent_node])
                children.append(pre_tag_parent_node)
            case MarkdownBlock.UNORDERED_LIST:
                list_of_content = ulist_to_stripped_markdown_string(block)
                tag = markdown_block_to_tag(MarkdownBlock.UNORDERED_LIST, block)
                list_of_children = []
                for entry in list_of_content:
                    content = text_to_children(entry)
                    node = ParentNode("li", content)
                    list_of_children.append(node)
                unordered_list_node = ParentNode(tag, list_of_children)
                children.append(unordered_list_node)
            case MarkdownBlock.ORDERED_LIST:
                list_of_content = olist_to_stripped_markdown_string(block)
                tag = markdown_block_to_tag(MarkdownBlock.ORDERED_LIST, block)
                list_of_children = []
                for entry in list_of_content:
                    content = text_to_children(entry)
                    node = ParentNode("li", content)
                    list_of_children.append(node)
                ordered_list_node = ParentNode(tag, list_of_children)
                children.append(ordered_list_node)
    return ParentNode("div", children)
                
def markdown_block_to_tag(type_of_block, markdown_text):
    match type_of_block:
        case MarkdownBlock.PARAGRAPH:
            return "p"
        case MarkdownBlock.QUOTE:
            return "blockquote"
        case MarkdownBlock.CODE:
            return "pre"
        case MarkdownBlock.UNORDERED_LIST:
            return "ul"
        case MarkdownBlock.ORDERED_LIST:
            return "ol"
        case MarkdownBlock.HEADING:
            heading_level = 0
            for char in markdown_text:
                if char == "#":
                    heading_level += 1
                else:
                    break
            return f"h{heading_level}"
        
def stripped_markdown_string(type_of_block, markdown_text):
    match type_of_block:
        case MarkdownBlock.PARAGRAPH:
            text_to_parse = markdown_text.replace("\n", " ")
            return text_to_parse
        case MarkdownBlock.QUOTE:
            split_text = markdown_text.split("\n")
            cleaned_lines = []
            for line in split_text:
                line = line.lstrip("> ")
                cleaned_lines.append(line)
            parsed_string = " ".join(cleaned_lines)
            return parsed_string
        case MarkdownBlock.CODE:
            raw_content_with_newlines = markdown_text[4:-3]
            return raw_content_with_newlines
        case MarkdownBlock.HEADING:
            heading_count = 0
            for char in markdown_text:
                if char == "#":
                    heading_count += 1
                elif char != "#":
                    break
            parsed_string = markdown_text[heading_count + 1:]
            return parsed_string

def ulist_to_stripped_markdown_string(markdown_text):
    split_entries = markdown_text.split("\n")
    stripped_entries = []
    for entry in split_entries:
        if entry.startswith("- "):
            stripped_entries.append(entry[2:])
        elif entry.startswith("* "):
            stripped_entries.append(entry[2:])
        elif entry.startswith("+ "):
            stripped_entries.append(entry[2:])
    return stripped_entries

def olist_to_stripped_markdown_string(markdown_text):
    split_entries = markdown_text.split("\n")
    stripped_entries = []
    for entry in split_entries:
        dot_space_index = entry.find(". ")
        if dot_space_index != -1:
            stripped_entries.append(entry[dot_space_index + 2])
    return stripped_entries

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children_html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children_html_nodes.append(html_node)
    return children_html_nodes