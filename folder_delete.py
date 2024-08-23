import shutil
import os

def delete_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Delete the folder and all its contents
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been deleted.")
    else:
        print(f"Folder '{folder_path}' does not exist.")

# Example usage
folder_path = r'C:\Users\verci\Documents\Python Code\Test-Repo\test images\output_slices_ellis_test'  # Replace with your folder path
delete_folder(folder_path)