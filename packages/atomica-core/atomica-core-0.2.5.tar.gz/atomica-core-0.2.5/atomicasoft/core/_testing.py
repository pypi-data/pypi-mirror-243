import pathlib

def find_in_path_branch(start_dir, folder_name):
    current_dir = pathlib.Path(start_dir).resolve()

    while True:
        target_folder = current_dir / folder_name
        if target_folder.is_dir():
            return target_folder

        # Move one level up
        parent_dir = current_dir.parent
        if current_dir == parent_dir:
            # Reached the root directory, stop searching
            break
        current_dir = parent_dir

    # If 'atm' folder is not found in any parent directory, raise an error
    raise FileNotFoundError("Folder not found in any parent directory.")
