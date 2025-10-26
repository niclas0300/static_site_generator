import re

def extract_markdown_images(text):
    results = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return results

def extract_markdown_links(text):
    results = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return results
