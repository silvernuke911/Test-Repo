import os
from functions import *

mainpath = os.path.join(r'C:\Users\verci\Documents\Python Code\Test-Repo', 'test images\\')
filename = 'ksc_ellis.png'

# Input path
image_path = mainpath+filename
num_slices = 20
scale = 1.1

# Start params
start_lat = 4
end_lat = 8
lat_divisions = 4
num_slices = abs(start_lat-end_lat)*lat_divisions
# Output path and scaling factor
base_name, ext = os.path.splitext(filename)
output_name = f'{base_name}_scaled{ext}'
output_path = os.path.join(r'C:\Users\verci\Documents\Python Code\Test-Repo', 'test images\\')
output_folder = 'output_slices_ellis'



def main():
    cut_image_horizontally(image_path, num_slices, output_path, output_folder)
    
if __name__=='__main__':
    main()



