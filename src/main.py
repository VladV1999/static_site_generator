from textnode import TextNode, TextType
from website_prep import recursive_copy_to_destination, generate_pages_recursive

def main():
    recursive_copy_to_destination("static", "public")
    generate_pages_recursive("content", "template.html", "public")
if __name__ == "__main__":
    main()