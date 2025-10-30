from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from recursive_copy_static import copy_job
from page_generation import generate_page


def main():
    dest_dir = "./public"
    src = "./static"
    content_path = "./content/index.md"
    contact_path = "./content/contact/index.md"
    glorfindel_path = "./content/blog/glorfindel/index.md"
    majesty_path = "./content/blog/majesty/index.md"
    tom_path = "./content/blog/tom/index.md"
    copy_job(src, dest_dir)
    generate_page(content_path, "template.html", dest_dir)
    generate_page(contact_path, "template.html", dest_dir)
    generate_page(glorfindel_path, "template.html", dest_dir)
    generate_page(majesty_path, "template.html", dest_dir)
    generate_page(tom_path, "template.html", dest_dir)


main()