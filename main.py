import os
import cv2
import numpy as np
import shutil

def format_float(num):
    if num < 10:
        return f'{num:06.3f}'  # Format as 00.000 for single-digit
    return f'{num:0.3f}'  # Format as 12.345 for multi-digit

def cut_image_horizontally(mainpath, filename, num_slices, output_path, output_folder):
    image_path = mainpath + filename
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")

    # Get the image dimensions
    height, width, _ = image.shape

    # Calculate the height of each slice
    slice_height = height // num_slices

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path+output_folder):
        os.makedirs(output_path+output_folder)

    # Slice the image and save each part
    for i in range(num_slices):
        # Calculate the start and end pixel row for this slice
        start_row = i * slice_height
        # For the last slice, make sure it includes any remaining pixels
        end_row = (i + 1) * slice_height if i < num_slices - 1 else height

        # Slice the image
        slice_img = image[start_row:end_row, :]

        # Save the slice
        output_path_ext = os.path.join(output_path, output_folder, format_float(end_lat - (i/lat_divisions))+'.png')
        print(output_path_ext)
        cv2.imwrite(output_path_ext, slice_img)
    print(f"{num_slices} slices saved to '{output_folder}'.")

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
    # cv2.imshow('Scaled Image', scaled_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
def scale_image(image_path, scale, output_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")
    
    # Get the original dimensions
    original_height, original_width = image.shape[:2]
    
    # Calculate the new dimensions
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    
    # Resize the image
    scaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    # Save or display the scaled image
    cv2.imwrite(output_path, scaled_image)
    cv2.imshow('Scaled Image', scaled_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
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
    combined_image = np.vstack(images[::-1])
    
    # Ensure the directory for the output file exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the combined image
    cv2.imwrite(output_file, combined_image)

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

def delete_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Delete the folder and all its contents
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been deleted.")
    else:
        print(f"Folder '{folder_path}' does not exist.")

mainpath = os.path.join(r'C:\Users\verci\Documents\Python Code\Test-Repo', 'test images\\')
filename = 'ksc_ellis.png'


# Start params
start_lat = 0
end_lat = 80
lat_divisions = 2
num_slices = (end_lat - start_lat) * lat_divisions
dlat = 1 / lat_divisions
lat_list = np.arange(start_lat, end_lat + dlat, dlat)

# Input path
mainpath = os.path.join(r'C:\Users\verci\Documents\Python Code\Test-Repo', 'test images\\')
filename = 'ksc_heightmap_1.png'

# Output path
output_path = mainpath
output_folder = f'{filename}_sliced'

def main():
    cut_image_horizontally(mainpath, filename, num_slices, output_path, output_folder)
    temp_directory = mainpath + output_folder
    file_paths = get_all_file_paths(temp_directory)
    # Print the list of file paths
    for path in file_paths:
        print(path)
    filenames = get_filenames_from_paths(file_paths)
    filenames = [float(item) for item in filenames]

    conv_list = mercator_conversion(lat_list)
    print(conv_list)

    output_file = os.path.join(mainpath, f'{filename}_combined.png')
    for path, name, conv in zip(file_paths, filenames,conv_list):
        print(path, name, conv)
        scale_image_height(path, conv, path)
        print(f'slice_{name} stretched')
    combine_images_vertically(file_paths, output_file)
    print ('Image successfully converted')
    delete_folder(temp_directory)
if __name__=='__main__':
    main()



