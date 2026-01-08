from textnode import TextNode, TextType
from website_prep import recursive_copy_to_destination, generate_pages_recursive
import sys
def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    recursive_copy_to_destination("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
if __name__ == "__main__":
    main()