import os
import cv2
import numpy as np

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

def combine_images_vertically(image_paths, output_file):
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
directory = r'C:\Users\verci\Documents\Python Code\Test-Repo\test images\output_slices_ellis_test'  # Replace with your directory path
file_paths = get_all_file_paths(directory)

# Specify the output file path (including the filename and extension)
output_file = r'C:\Users\verci\Documents\Python Code\Test-Repo\test images\output_slices_ellis_test\combined_image.png'

# Combine the images
combine_images_vertically(file_paths, output_file)