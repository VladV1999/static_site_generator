from textnode import TextNode, TextType
from extract_from_markdown import extract_markdown_images, extract_markdown_links
def split_nodes_delimeter(old_nodes, delimeter, text_type):
    result = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            result.append(old_node)
            continue
        if old_node.text.count(delimeter) % 2 != 0:
            raise Exception("Invalid markdown syntax!")
        parts = old_node.text.split(delimeter)
        for i, value in enumerate(parts):
            if i % 2 != 0 and len(value) != 0:
                node = TextNode(value, text_type)
                result.append(node)
            elif i % 2 == 0 and len(value) != 0:
                node = TextNode(value, TextType.TEXT)
                result.append(node)
    return result


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        remaining_text = node.text
        image_parts = extract_markdown_images(remaining_text)
        if len(image_parts) == 0:
            result.append(node)
            continue
        for image_part in image_parts:
            alt_text = image_part[0]
            url = image_part[1]
            delimeter = f"![{alt_text}]({url})"
            split_text = remaining_text.split(delimeter, maxsplit=1)
            if split_text[0] != "":
                txt_node = TextNode(split_text[0], TextType.TEXT)
                result.append(txt_node)
            result.append(TextNode(alt_text, TextType.IMAGE, url))
            remaining_text = split_text[1]
        if remaining_text != "":
            result.append(TextNode(remaining_text, TextType.TEXT))
    return result

def split_nodes_links(old_nodes):
    result = []
    for node in old_nodes:
        remaining_text = node.text
        link_parts = extract_markdown_links(remaining_text)
        if len(link_parts) == 0:
            result.append(node)
            continue
        for link_part in link_parts:
            anchor_text = link_part[0]
            url = link_part[1]
            delimeter = f"[{anchor_text}]({url})"
            split_text = remaining_text.split(delimeter, maxsplit=1)
            if split_text[0] != "":
                txt_node = TextNode(split_text[0], TextType.TEXT)
                result.append(txt_node)
            result.append(TextNode(anchor_text, TextType.LINK, url))
            remaining_text = split_text[1]
        if remaining_text != "":
            result.append(TextNode(remaining_text, TextType.TEXT))
    return result