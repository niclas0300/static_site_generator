from split_nodes import markdown_to_blocks

def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        if block.startswith("# "):
            stripped_block = block.strip("# ")
            return stripped_block
