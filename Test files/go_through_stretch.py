
import os
import numpy as np
import cv2

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
def get_filenames_from_paths(file_paths):
    # Extract the filename from each path
    filenames = [os.path.splitext(os.path.basename(path))[0] for path in file_paths]
    return filenames

def numerical_differentiator(x, func):
    """
    Returns the array of the numerical derivative of a function f(x), dy/dx.
    
    Parameters:
        x (np.ndarray): Array of numbers representing values on the x axis.
        func (callable): A function taking x as an input.
    
    Returns:
        np.ndarray: Array of numerical derivative values.
    """
    y = func(x)  # Creating the function values
    output = np.zeros_like(y)  # Initializing an array
    
    # Calculate differences for the interior points using central difference
    dx = np.diff(x)
    dy = np.diff(y)
    output[1:-1] = (y[2:] - y[:-2]) / (x[2:] - x[:-2])
    
    # Forward difference for the first point
    output[0] = (y[1] - y[0]) / dx[0]
    
    # Backward difference for the last point
    output[-1] = (y[-1] - y[-2]) / dx[-1]
    
    return output

def mercator_function(lat):
    rad_lat = np.deg2rad(lat)
    return np.log(np.tan(rad_lat) + (1 / np.cos(rad_lat)))

def mercator_conversion(latlist):
    # Convert the latitude list to a NumPy array
    lat_list = np.array(latlist)
    conv_list = np.rad2deg(numerical_differentiator(lat_list,mercator_function))
    return conv_list

def scale_image_height(image_path, scale, output_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")
    
    # Get the original dimensions
    original_height, original_width = image.shape[:2]
    
    # Calculate the new height while keeping the width unchanged
    new_height = int(original_height * scale)
    new_width = original_width  # Keep the width the same
    
    # Resize the image
    scaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_NEAREST_EXACT)
    #INTER_LINEAR
    #INTER_NEAREST
    cv2.imwrite(output_path, scaled_image)
    # cv2.imshow('Scaled Image', scaled_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

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

dlat = 1/20
start_lat = 40
end_lat = 44
lat = np.arange(start_lat, end_lat + dlat, dlat)
print(lat)

# Example usage
directory = r'C:\Users\verci\Documents\Python Code\Test-Repo\test images\output_slices_ellis_test'  # Replace with your directory path
file_paths = get_all_file_paths(directory)

# Print the list of file paths
for path in file_paths:
    print(path)

filenames = get_filenames_from_paths(file_paths)
filenames = [float(item) for item in filenames]

# Print the list of filenames
for name in filenames:
    print(name)

conv_list = mercator_conversion(lat)
for num in conv_list:
    print(num)

output_file = os.path.join(directory, 'combined_image.png')

for path, name, conv in zip(file_paths, filenames,conv_list):
    print(path, name, conv)
    scale_image_height(path, conv, path)
    print(f'slice_{name} stretched')
combine_images_vertically(file_paths, output_file)




