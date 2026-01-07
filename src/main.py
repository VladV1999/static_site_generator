from textnode import TextNode, TextType
from website_prep import recursive_copy_to_destination, generate_page

def main():
    recursive_copy_to_destination("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
if __name__ == "__main__":
    main()