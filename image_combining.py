import os
import cv2
import numpy as np
import shutil

def copy_folder(src_folder, dst_folder):
    # Check if the destination folder exists, and create it if it doesn't
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
        print(f"Destination folder '{dst_folder}' created.")
    
    # Copy the entire folder and its contents
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dst_path = os.path.join(dst_folder, item)
        
        if os.path.isdir(src_path):
            # Recursively copy subdirectories
            shutil.copytree(src_path, dst_path)
        else:
            # Copy files
            shutil.copy2(src_path, dst_path)
    
    print(f"Folder copied from '{src_folder}' to '{dst_folder}'.")

def get_all_file_paths(directory):
    # List to store file paths
    file_paths = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Only add image files
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                full_path = os.path.join(root, file)
                file_paths.append(full_path)
    return file_paths

def combine_images_vertically(image_paths, output_file):
    if not image_paths:
        raise ValueError("No image files found in the provided paths.")
    
    # Load all images
    images = [cv2.imread(image_path) for image_path in image_paths]
    
    # Check if all images were loaded successfully
    if any(image is None for image in images):
        raise ValueError("One or more images could not be loaded.")
    
    # Get the width of the first image
    width = images[0].shape[1]
    
    # Check if all images have the same width
    if not all(image.shape[1] == width for image in images):
        raise ValueError("Not all images have the same width.")
    
    # Combine images vertically (starting from the lowest)
    combined_image = np.vstack(images[:])
    
    # Ensure the directory for the output file exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the combined image
    cv2.imwrite(output_file, combined_image)
    
    # Display the combined image
    cv2.imshow('Combined Image', combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
directory = r'C:\Users\verci\Documents\Python Code\Test-Repo\test images\output_slices_ellis'  # Replace with your directory path
duplicate_directory = r'C:\Users\verci\Documents\Python Code\Test-Repo\test images\output_slices_ellis_test'

# Copy the folder
copy_folder(directory, duplicate_directory)

# Get all image file paths in the copied folder
file_paths = get_all_file_paths(duplicate_directory)

# Ensure there are files to process
if not file_paths:
    raise ValueError(f"No image files found in '{duplicate_directory}'.")

# Specify the output file path (including the filename and extension)
output_file = os.path.join(duplicate_directory, 'combined_image.png')

# Combine the images
combine_images_vertically(file_paths, output_file)