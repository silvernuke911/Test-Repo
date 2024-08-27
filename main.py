import os
import numpy as np
from functions import *

# Input
mainpath = 'test images\\'
filename = 'Kerbin_heightmap_all.png'

start_lat = 0
end_lat   = 80
lat_divisions = 1

# Output
output_folder = f'{filename}_sliced'
output_path = mainpath + output_folder
output_file = os.path.join(mainpath, f'{filename}_converted_2.png')

def main():
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

if __name__=='__main__':
    main()