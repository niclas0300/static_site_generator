from recursive_copy_static import copy_job
from page_generation import generate_pages_recursive
import sys


def main():
    dest_dir = "./public"
    src = "./static"
    content_path = "./content"

    if len(sys.argv[0]) != 0:
        basepath = sys.argv[0]
    
    basepath = "/"

    copy_job(src, dest_dir)
    generate_pages_recursive(content_path, "template.html", dest_dir, basepath)



main()