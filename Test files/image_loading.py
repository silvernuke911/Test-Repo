import os

def get_all_file_paths(directory):
    # List to store file paths
    file_paths = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Create the full file path and add it to the list
            full_path = os.path.join(root, file)
            file_paths.append(full_path)
    return file_paths

# Example usage
directory = r'C:\Users\verci\Documents\Python Code\Test-Repo\test images\output_slices_ellis'  # Replace with your directory path
file_paths = get_all_file_paths(directory)

# Print the list of file paths
for path in file_paths:
    print(path)

def get_filenames_from_paths(file_paths):
    # Extract the filename from each path
    filenames = [os.path.splitext(os.path.basename(path))[0] for path in file_paths]
    return filenames

filenames = get_filenames_from_paths(file_paths)

# Print the list of filenames
for name in filenames:
    print(name)