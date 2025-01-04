from mailer import send_mail_with_images
import time
import os
from configuration import default_misc_config
import pickle


def find_new_files(folder_path):
    """
    # Example usage:
    folder_path = "/var/lib/motion/"
    new_files, deleted_files = find_new_files(folder_path)
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError("The folder {} does not exist.".format(folder_path))

    pickle_file_path = os.path.join(folder_path, "file_list.pkl")

    # load the existing file list from the pickle file
    try:
        with open(pickle_file_path, "rb") as pickle_file:
            saved_files = pickle.load(pickle_file)
    except (FileNotFoundError, pickle.UnpicklingError):
        saved_files = set()

    # get the current list of JPG files in the folder
    current_files = set(
        file
        for file in os.listdir(folder_path)
        if file.lower().endswith(default_misc_config.image_extension)
    )

    # identify new files and deleted files
    new_files = current_files - saved_files
    deleted_files = saved_files - current_files

    # update the saved files in the pickle file
    with open(pickle_file_path, "wb") as pickle_file:
        pickle.dump(current_files, pickle_file)

    return list(new_files), list(deleted_files)


sync_delay = 5
folder_path = default_misc_config.path_image_folder

while True:
    try:
        new_files, deleted_files = find_new_files(folder_path)
        print("new files:", new_files, flush=True)
        print("deleted files:", deleted_files, flush=True)
        send_mail_with_images(folder_path, new_files)
        time.sleep(sync_delay)
    except Exception as e:
        print(e, flush=True)
