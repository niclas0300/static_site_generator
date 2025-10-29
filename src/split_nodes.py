from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from extracting_raw_text import extract_markdown_images, extract_markdown_links
from block_node import block_to_block_type, BlockType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type.value != "text":
            new_nodes.append(node)
        else:
            split_list = node.text.split(delimiter)
            if len(split_list) % 2 == 0:
                raise ValueError("Missing closing delimiter")
            for index in range(len(split_list)):
                if split_list[index] == "":
                    continue
                if index % 2 == 0:
                    new_node = TextNode(split_list[index], TextType.PLAIN)
                    new_nodes.append(new_node)
                else:
                    new_node = TextNode(split_list[index], text_type)
                    new_nodes.append(new_node)

    return new_nodes
        
def split_nodes_link(old_nodes):
    result_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            result_list.append(old_node)
            continue
        if len(old_node.text) == 0:
            continue
        links_data = extract_markdown_links(old_node.text)
        if len(links_data) == 0:
            result_list.append(old_node)
        else:
            temp_text = old_node.text
            for index in range(len(links_data)):
                link_text = links_data[index][0]
                link = links_data[index][1]
                split_list = temp_text.split(f"[{link_text}]({link})", 1)
                if len(split_list) != 2:
                    raise ValueError("invalid markdown, image section not closed")
                if split_list[0] != "":
                    result_list.append(TextNode(split_list[0], TextType.PLAIN))   
                result_list.append(TextNode(link_text, TextType.LINK, link))
                temp_text = split_list[1]

            if len(temp_text) != 0:
                result_list.append(TextNode(temp_text, TextType.PLAIN))
    return result_list


def split_nodes_image(old_nodes):
    result_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            result_list.append(old_node)
            continue
        if len(old_node.text) == 0:
            continue
        image_data = extract_markdown_images(old_node.text)
        if len(image_data) == 0:
            result_list.append(old_node)
        else:
            temp_text = old_node.text
            for image in image_data:
                image_text = image[0]
                image_link = image[1]
                split_list = temp_text.split(f"![{image_text}]({image_link})", 1)
                if len(split_list) != 2:
                    raise ValueError("invalid markdown, image section not closed")
                if split_list[0] != "":
                    result_list.append(TextNode(split_list[0], TextType.PLAIN))   
                result_list.append(TextNode(image_text, TextType.IMAGE, image_link))
                temp_text = split_list[1]

            if len(temp_text) != 0:
                result_list.append(TextNode(temp_text, TextType.PLAIN))
    return result_list
        

def text_to_textnodes(text):
    node_text = TextNode(text, TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node_text], "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.PLAIN)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)