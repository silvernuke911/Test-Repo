import os
import cv2
import numpy as np

def combine_images_vertically(image_paths, output_path):
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
    combined_image = np.vstack(images[::-1])  # Reverse the list to start from the lowest
    
    # Save the combined image
    cv2.imwrite(output_path, combined_image)
    
    # Display the combined image
    cv2.imshow('Combined Image', combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
