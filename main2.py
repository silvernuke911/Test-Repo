import os
import cv2
import numpy as np
import shutil

def format_float(num):
    return f'{num:06.3f}'  # Format as 00.000 for single-digit or multi-digit numbers

def get_all_file_paths(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                file_paths.append(os.path.join(root, file))
    return file_paths

def get_filenames_from_paths(file_paths):
    return [os.path.splitext(os.path.basename(path))[0] for path in file_paths]

def cut_image_horizontally(mainpath, filename, start_lat, end_lat, dlat, output_path, output_folder):
    image_path = os.path.join(mainpath, filename)
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")
    
    height, width, _ = image.shape
    num_slices = int((end_lat - start_lat) / dlat)
    slice_height = height // num_slices

    os.makedirs(os.path.join(output_path, output_folder), exist_ok=True)

    for i in range(num_slices):
        start_row = i * slice_height
        end_row = (i + 1) * slice_height if i < num_slices - 1 else height
        slice_img = image[start_row:end_row, :]
        slice_lat = end_lat - i * dlat
        output_file = os.path.join(output_path, output_folder, f'{format_float(slice_lat)}.png')
        cv2.imwrite(output_file, slice_img)

    print(f"{num_slices} slices saved to '{output_folder}'.")

def scale_image_height(image_path, scale, output_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")

    original_height, original_width = image.shape[:2]
    new_height = int(original_height * scale)
    scaled_image = cv2.resize(image, (original_width, new_height), interpolation=cv2.INTER_NEAREST_EXACT)
    cv2.imwrite(output_path, scaled_image)

def combine_images_vertically(image_paths, output_file):
    if not image_paths:
        raise ValueError("No image files found in the provided paths.")

    images = [cv2.imread(path) for path in image_paths]
    if any(image is None for image in images):
        raise ValueError("One or more images could not be loaded.")
    
    width = images[0].shape[1]
    if not all(image.shape[1] == width for image in images):
        raise ValueError("Not all images have the same width.")

    combined_image = np.vstack(images)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    cv2.imwrite(output_file, combined_image)

def flip_image_vertically(image_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")
    
    flipped_image = cv2.flip(image, 0)
    cv2.imwrite(output_path, flipped_image)

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been deleted.")
    else:
        print(f"Folder '{folder_path}' does not exist.")

def mercator_function(lat):
    rad_lat = np.deg2rad(lat)
    return np.log(np.tan(rad_lat) + 1 / np.cos(rad_lat))

def mercator_conversion(latlist):
    lat_list = np.array(latlist)
    return np.rad2deg(np.gradient(mercator_function(lat_list)))

def process_latitude_range(start_lat, end_lat, filename, mainpath, output_folder_prefix):
    dlat = 1.0  # Adjust as necessary
    output_folder = f"{output_folder_prefix}_sliced"
    output_file = os.path.join(mainpath, f"{filename}_combined.png")

    lat_list = np.arange(start_lat, end_lat + dlat, dlat)
    cut_image_horizontally(mainpath, filename, start_lat, end_lat, dlat, mainpath, output_folder)
    temp_directory = os.path.join(mainpath, output_folder)
    file_paths = get_all_file_paths(temp_directory)
    filenames = [float(item) for item in get_filenames_from_paths(file_paths)]

    conv_list = mercator_conversion(lat_list)
    for path, name, conv in zip(file_paths, filenames, conv_list):
        scale_image_height(path, conv, path)
        print(f'slice_{name} stretched')

    combine_images_vertically(file_paths, output_file)
    print('Image successfully converted')
    delete_folder(temp_directory)

def main():
    mainpath = r'C:\Users\verci\Documents\Python Code\Test-Repo\test images\\'
    filename = 'map_test.png'
    start_lat = -60
    end_lat = 0

    if start_lat >= 0 and end_lat > 0:
        process_latitude_range(start_lat, end_lat, filename, mainpath, filename)
    elif start_lat < 0 and end_lat <= 0:
        flip_image_vertically(os.path.join(mainpath, filename), os.path.join(mainpath, f'{filename}_flipped.png'))
        filename_flipped = f'{filename}_flipped.png'
        process_latitude_range(-end_lat, -start_lat, filename_flipped, mainpath, filename_flipped)
    elif start_lat < 0 and end_lat > 0:
        pass  # Implement processing for mixed positive/negative latitudes if needed

if __name__ == '__main__':
    main()