import os
from functions import *

mainpath = os.path.join(r'C:\Users\verci\Documents\Python Code\Test-Repo', 'test images\\')
filename = 'telescope1.png'

image_path = mainpath+filename
num_slices = 20
output_folder = mainpath+'output_slices1'

def main():
    cut_image_horizontally(image_path, num_slices, output_folder)
    
if __name__=='__main__':
    main()



