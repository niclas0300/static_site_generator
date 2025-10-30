from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from recursive_copy_static import copy_job
from page_generation import generate_page, generate_pages_recursive


def main():
    dest_dir = "./public"
    src = "./static"
    content_path = "./content"
    copy_job(src, dest_dir)
    generate_pages_recursive(content_path, "template.html", dest_dir)



main()