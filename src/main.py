from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from recursive_copy_static import copy_job


def main():
    dest_dir = "public/"
    src = "static"
    copy_job(src, dest_dir)


main()