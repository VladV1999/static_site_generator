from textnode import TextNode, TextType
from file_copy import recursive_copy_to_destination

def main():
    recursive_copy_to_destination("static", "public")

if __name__ == "__main__":
    main()