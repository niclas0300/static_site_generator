from split_nodes import markdown_to_html_node
from htmlnode import ParentNode
from extract_title import extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_path_md_file = open(from_path).read()
    template_file = open(template_path).read()
    html_string = markdown_to_html_node(from_path_md_file).to_html()
    html_title = extract_title(from_path_md_file)
    new_template = template_file.replace("{{ Title }}", html_title).replace("{{ Content }}", html_string)
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    dest_file_path = os.path.join(dest_path, "index.html")
    with open(dest_file_path, "w") as file:
        file.write(new_template)    



