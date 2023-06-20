import numpy as np
from PIL import Image
import py360convert

def main():
    image = np.array(Image.open('input/image1.jpeg'))
    e_img = py360convert.e2c(image, face_w=256, cube_format='dice')
    Image.fromarray(e_img).save('output/image1_e2c.jpeg')
    
if __name__ == "__main__":
    main()