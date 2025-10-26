from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    split_block = block.split("\n")
    if "#" in split_block[0]:
        header_split = split_block[0]
        if len(header_split[0]) <= 6 and header_split[0].count("#") == len(header_split[0]):
            return BlockType.HEADING
    if split_block[0][:3] == "```" and split_block[-1][-3:] == "```":
        return BlockType.CODE
    quote_count = 0
    unordered_list_count = 0
    ordered_list_count = 0
    for index in range(len(split_block)):
        if split_block[index][0] == ">":
            quote_count += 1
        elif split_block[index][:2] == "- ":
            unordered_list_count += 1
        elif split_block[index][:3] == f"{index + 1}. ":
            ordered_list_count += 1
    if quote_count == len(split_block):
        return BlockType.QUOTE
    if unordered_list_count == len(split_block):
        return BlockType.UNORDERED_LIST
    if ordered_list_count == len(split_block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
        