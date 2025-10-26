from textnode import TextNode, TextType
from extracting_raw_text import extract_markdown_images, extract_markdown_links

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
    split_list = markdown.split("\n\n")
    return_list = []
    for i in range(len(split_list)):
        if len(split_list[i]) == 0:
            continue
        block = split_list[i].strip("\n")
        return_list.append(block)
    return return_list

