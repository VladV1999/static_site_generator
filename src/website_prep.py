import os
import pathlib
import shutil

from htmlnode import HTMLNode
from markdown_block import markdown_to_html_node
def recursive_copy_to_destination(source_directory, destination_directory):
    dest_dir_abs_path = os.path.abspath(destination_directory)
    source_dir_abs_path = os.path.abspath(source_directory)
    if os.path.exists(dest_dir_abs_path):
        shutil.rmtree(dest_dir_abs_path)
    list_of_paths = os.listdir(source_dir_abs_path)
    for path in list_of_paths:
        file_path = os.path.abspath(os.path.join(source_dir_abs_path, path))
        if os.path.isfile(file_path):
            dest_file_path = os.path.abspath(os.path.join(dest_dir_abs_path, path))
            if not os.path.exists(dest_dir_abs_path):
                os.makedirs(dest_dir_abs_path)
            shutil.copy(file_path, dest_file_path)
        else:
            new_dest_dir_abs_path = os.path.abspath(os.path.join(destination_directory, path))
            new_source_dir_abs_path = os.path.abspath(os.path.join(source_directory, path))
            recursive_copy_to_destination(new_source_dir_abs_path, new_dest_dir_abs_path)

def extract_title(markdown):
    if not markdown.startswith("#"):
        raise Exception("Cannot extract title, as it is not there")
    return markdown.lstrip("# ").rstrip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        md_file_from_path_text = f.read()

    with open (template_path, 'r') as f:
        md_file_template_path_text = f.read()

    md_text = markdown_to_html_node(md_file_from_path_text)
    html_text = md_text.to_html()
    title = extract_title(md_file_from_path_text)
    print(md_text)
    full_html = md_file_template_path_text.replace("{{ Content }}", html_text)
    full_html = full_html.replace("{{ Title }}", title)

    dir_of_dest_path = os.path.dirname(dest_path)
    if dir_of_dest_path != "" and not os.path.exists(dir_of_dest_path):
        os.makedirs(dir_of_dest_path)
    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_abs_path = os.path.abspath(dir_path_content)
    dest_dir_path_content = os.path.abspath(dest_dir_path)
    list_of_paths = os.listdir(dir_abs_path)
    for path in list_of_paths:
        abs_path = os.path.abspath(os.path.join(dir_path_content, path))
        if os.path.isfile(abs_path):
            parts = abs_path.split(".")
            if parts[-1] == "md":
                dest_dir_file_path = os.path.abspath(os.path.join(dest_dir_path_content, path))
                dest_html_path = pathlib.Path(dest_dir_file_path).with_suffix(".html")
                generate_page(abs_path, template_path, dest_html_path)
        else:
            new_dir_path_content = os.path.abspath(os.path.join(dir_path_content, path))
            new_dest_dir_path = os.path.abspath(os.path.join(dest_dir_path, path))
            generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path)