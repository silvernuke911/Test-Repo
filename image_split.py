import numpy as np
import cv2
import os

mainpath = os.path.join(r'C:\Users\verci\Documents\Python Code\Test-Repo', 'test images\\')
filename = 'anti-aliasing god un.png'
image_path = mainpath+filename
img = cv2.imread(image_path)
print(np.size(img))
resized_img = cv2.resize(img, (500, 500))
cv2.imshow('Anti-Aliased Image', resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

def cut_image_horizontally(image_path, num_slices, output_folder):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")

    # Get the image dimensions
    height, width, _ = image.shape

    # Calculate the height of each slice
    slice_height = height // num_slices

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Slice the image and save each part
    for i in range(num_slices):
        # Calculate the start and end pixel row for this slice
        start_row = i * slice_height
        # For the last slice, make sure it includes any remaining pixels
        end_row = (i + 1) * slice_height if i < num_slices - 1 else height

        # Slice the image
        slice_img = image[start_row:end_row, :]

        # Save the slice
        output_path = os.path.join(output_folder, f'slice_{i + 1}.jpg')
        cv2.imwrite(output_path, slice_img)

    print(f"{num_slices} slices saved to '{output_folder}'.")

# Example usage:
image_path = mainpath+filename
num_slices = 10
output_folder = mainpath+'output_slices'

cut_image_horizontally(image_path, num_slices, output_folder)