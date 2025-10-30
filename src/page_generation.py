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



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_dir_list = os.listdir(dir_path_content)
    print(f"list content dir: {content_dir_list}")
    print(f"dest dir path: {dest_dir_path}")
    for content in content_dir_list:
        joined_dir_path = os.path.join(dir_path_content, content)
        print(f"joined content path: {joined_dir_path}")
        joined_dest_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(joined_dir_path):
            print(f"joined path file: {joined_dir_path}")
            content_file = open(joined_dir_path)
            content_read = content_file.read()
            content_file.close()

            template_file = open(template_path)
            template_read = template_file.read()
            template_file.close()

            content_html_string = markdown_to_html_node(content_read).to_html()
            content_html_title = extract_title(content_read)

            content_html_file = template_read.replace("{{ Title }}", content_html_title).replace("{{ Content }}", content_html_string)

            if not os.path.exists(dest_dir_path):
                os.mkdir(dest_dir_path)

            dest_file_path = os.path.join(dest_dir_path, "index.html")
            to_file = open(dest_file_path, "w")
            to_file.write(content_html_file)
            to_file.close()
        else:
            generate_pages_recursive(joined_dir_path, template_path, joined_dest_path)
