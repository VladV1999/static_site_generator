import os
import shutil
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

        