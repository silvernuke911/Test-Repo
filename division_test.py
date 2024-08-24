import os
import cv2
import numpy as np
import shutil

# Start params
start_lat = -40
end_lat = 20
lat_divisions = 2
num_slices = (end_lat - start_lat) * lat_divisions
dlat = 1 / lat_divisions
lat_list = np.arange(start_lat, end_lat + dlat, dlat)

# Input path
mainpath = os.path.join(r'C:\Users\verci\Documents\Python Code\Test-Repo', 'test images\\')
filename = 'map_test.png'

# Output path
output_path = mainpath

image_path = mainpath+filename
output_positive_path = mainpath+f'{filename}_positive.png'
output_negative_path = mainpath+f'{filename}_negative.png'

if not os.path.exists(mainpath + f'{filename}_positive_slices'):
    os.makedirs(mainpath + f'{filename}_positive_slices')
if not os.path.exists(mainpath + f'{filename}_negative_slices'):
    os.makedirs(mainpath + f'{filename}_negative_slices')

def split_map_by_latitude(image_path, min_lat, max_lat,output_positive_path,output_negative_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")
    
    # Handle cases where the map only has positive or negative latitudes
    if min_lat >= 0:
        # Only positive latitudes
        cv2.imwrite(output_positive_path, image)
        print("Map only contains positive latitudes. Original image saved for positive latitudes.")
        return
    elif max_lat <= 0:
        # Only negative latitudes
        cv2.imwrite(output_negative_path, image)
        print("Map only contains negative latitudes. Original image saved for negative latitudes.")
        return
    
    # Get the image dimensions
    height, width, _ = image.shape
    
    # Calculate the ratio of pixels per latitude degree
    lat_range = max_lat - min_lat
    
    # Calculate the pixel row that corresponds to the equator (latitude 0)
    equator_row = int((max_lat / lat_range) * height)
    
    # Split the image at the equator
    positive_latitudes_image = image[:equator_row, :]
    negative_latitudes_image = cv2.flip(image[equator_row:, :],0)
    
    # Save the resulting images
    cv2.imwrite(output_positive_path, positive_latitudes_image)
    print('Positive part saved')
    cv2.imwrite(output_negative_path, negative_latitudes_image)
    print('Negative part saved')
    
def cut_image_horizontally(mainpath, filename, num_slices, output_path, output_folder):
    def format_float(num):
        if num < 10:
            return f'{num:06.3f}'  # Format as 00.000 for single-digit
        return f'{num:0.3f}'  # Format as 12.345 for multi-digit
    
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

split_map_by_latitude(image_path,start_lat,end_lat,output_positive_path,output_negative_path)

# create a file for the positive side and split the images
# create a file for the negative side and split the images, then flip the image upside down