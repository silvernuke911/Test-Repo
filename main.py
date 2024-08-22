import os
from image_split import *

mainpath = os.path.join(r'C:\Users\verci\Documents\Python Code\Test-Repo', 'test images\\')
filename = 'anti-aliasing god un.png'

image_path = mainpath+filename
num_slices = 10
output_folder = mainpath+'output_slices'

def main():
    cut_image_horizontally(image_path, num_slices, output_folder)
    
if __name__=='__main__':
    main()



