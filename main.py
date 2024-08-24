import os
import cv2
import numpy as np
import shutil

def distribute_sum_centrally_even(m, n):
    quotient, remainder = divmod(m, n)
    result = [quotient] * n
    
    # Calculate the intervals for distributing the remainder
    interval = n / (remainder + 1)
    
    # Distribute the remainder values
    for i in range(remainder):
        # Calculate the position to add the extra value
        pos = int(round(interval * (i + 1))) - 1
        result[pos] += 1
    
    return result

def cut_image_horizontally(image_path, num_slices, output_path):
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError('Image not found')

    height, width, _ = image.shape

    # Calculate the heights of each slice based on the central distribution
    heights = distribute_sum_centrally_even(height, num_slices)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    start_row = 0
    height_small_list = []

    for i, slice_height in enumerate(heights):
        end_row = start_row + slice_height
        height_small = end_row - start_row
        height_small_list.append(height_small)
        
        # Slice the image
        slice_img = image[start_row:end_row, :]

        # Save the slice
        output_path_ext = os.path.join(output_path, f'slice_{i:06}.png')

        cv2.imwrite(output_path_ext, slice_img)

        # Update start_row for the next slice
        start_row = end_row


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
    #INTER_NEAREST_EXACT
    cv2.imwrite(output_path, scaled_image)


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
    combined_image = np.vstack(images[::])
    
    # Ensure the directory for the output file exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the combined image
    cv2.imwrite(output_file, combined_image)

def delete_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Delete the folder and all its contents
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been deleted.")
    else:
        print(f"Folder '{folder_path}' does not exist.")

# Input

mainpath = os.path.join(r'C:\Users\verci\Documents\Python Code\Test-Repo', 'test images\\')
filename = 'ksc_heightmap_1.png'


start_lat = 0
end_lat = 80
lat_divisions = 1


# Output

output_folder = f'{filename}_sliced'
output_path = mainpath + output_folder
output_file = os.path.join(mainpath, f'{filename}_converted.png')

num_slices = (end_lat - start_lat) * lat_divisions
dlat = 1 / lat_divisions
lat_list = np.arange(start_lat, end_lat, dlat)
lat_list = [(x + dlat if x >= 0 else x) for x in lat_list]
lat_list = lat_list[::-1]

cut_image_horizontally(mainpath+filename,num_slices,output_path)
filenames = get_all_file_paths(output_path)
conv_list = mercator_conversion(lat_list)

for path, lat, conv in zip(filenames,lat_list,conv_list):
    scale_image_height(path, conv, path)
    print(f'{path}, {lat} stretched by {conv:.3f}')

print('Slice stretching complete')
combine_images_vertically(filenames, output_file)
print('Slice combination complete')
delete_folder(output_path)