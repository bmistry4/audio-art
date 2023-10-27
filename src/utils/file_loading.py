import os


def create_directory(folder_path):
    """
    Check if directory exists and create it if it doesn't.
    :param folder_path: path of directory
    :return: None
    """
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")
        else:
            print(f"Folder '{folder_path}' already exists.")
    except OSError as e:
        print(f"An error occurred while creating the folder: {e}")