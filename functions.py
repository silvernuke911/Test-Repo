import numpy as np
import cv2
import os

def cut_image_horizontally(image_path, num_slices, output_path, output_folder):
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
        output_path_ext = os.path.join(output_path, output_folder, f'latslice_{startlat+(i/latdiv)}.png')
        print(output_path_ext)
        cv2.imwrite(output_path_ext, slice_img)
        print(f'slice_{i + 1}.png created')
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
    cv2.imwrite(output_path, scaled_image)
    cv2.imshow('Scaled Image', scaled_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
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
    

# # Main path and filenames
# mainpath = os.path.join(r'C:\Users\verci\Documents\Python Code\Test-Repo', 'test images')
# filename = 'telescope1.png'
# image_path = os.path.join(mainpath, filename)

# # Output path and scaling factor
# base_name, ext = os.path.splitext(filename)
# output_name = f'{base_name}_scaled{ext}'
# output_path = os.path.join(r'C:\Users\verci\Documents\Python Code\Test-Repo', 'test images', output_name)
# scale = 1.1

# # Call the function with the correct output path
# scale_image_height(image_path, scale, output_path)

# image = cv2.imread(image_path)
# print(image)
# print(np.size(image))
# print(image.shape)