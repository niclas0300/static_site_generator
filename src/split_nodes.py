from textnode import TextNode, TextType

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
        

        
        

