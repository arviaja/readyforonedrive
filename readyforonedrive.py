import os
import re

# Set the maximum path length allowed by OneDrive
MAX_PATH_LENGTH = 400

# Ask the user for the path to their Dropbox folder
dropbox_path = input("Enter the path to your Dropbox folder: ")

# Change to the Dropbox directory
os.chdir(os.path.expanduser(dropbox_path))

# Ask the user if they want to do a dry run
dry_run = input("Do you want to do a dry run? (y/n): ").lower() == "y"

# Find all files and directories with paths longer than the maximum allowed length
for dirpath, dirnames, filenames in os.walk(".", topdown=False):
    for name in filenames + dirnames:
        file_path = os.path.join(dirpath, name)
        # Check if the file path is too long
        if len(file_path) > MAX_PATH_LENGTH:
            # Calculate the number of characters that need to be removed
            num_chars_to_remove = len(file_path) - MAX_PATH_LENGTH

            # Shorten the file name by removing characters from the end
            new_file_name = file_path[:len(file_path) - num_chars_to_remove]

            if dry_run:
                # Print the proposed new file name
                print(f"Dry run: Would shorten {file_path} to {new_file_name}")
            else:
                # Rename the file or directory
                os.rename(file_path, new_file_name)

# Find and rename all files and directories to be compatible with OneDrive
for dirpath, dirnames, filenames in os.walk(".", topdown=False):
    for name in filenames + dirnames:
        file_path = os.path.join(dirpath, name)
        # Replace any characters that are not allowed in OneDrive file or folder names with underscores
        new_file_name = re.sub(r'[\"*:<>?\/\\|]', "_", name)

        # Rename the file or directory if the name has changed
        if new_file_name != name:
            new_file_path = os.path.join(dirpath, new_file_name)
            if dry_run:
                # Print the proposed new file name
                print(f"Dry run: Would rename {file_path} to {new_file_path}")
            else:
                # Rename the file or directory
                os.rename(file_path, new_file_path)
