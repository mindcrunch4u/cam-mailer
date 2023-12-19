import os
import pickle

def find_new_files(folder_path):
    # Ensure the folder path is valid
    if not os.path.exists(folder_path):
        raise FileNotFoundError("The folder {} does not exist.".format(folder_path))

    # Define the pickle file path
    pickle_file_path = os.path.join(folder_path, 'file_list.pkl')

    # Try to load the existing file list from the pickle file
    try:
        with open(pickle_file_path, 'rb') as pickle_file:
            saved_files = pickle.load(pickle_file)
    except (FileNotFoundError, pickle.UnpicklingError):
        saved_files = set()

    # Get the current list of JPG files in the folder
    current_files = set(file for file in os.listdir(folder_path) if file.lower().endswith('.jpg'))

    # Identify new files and deleted files
    new_files = current_files - saved_files
    deleted_files = saved_files - current_files

    # Update the saved files in the pickle file
    with open(pickle_file_path, 'wb') as pickle_file:
        pickle.dump(current_files, pickle_file)

    return list(new_files), list(deleted_files)

"""
# Example usage:
folder_path = "/var/lib/motion/"
new_files, deleted_files = find_new_files(folder_path)
"""
