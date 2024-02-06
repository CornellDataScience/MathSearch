'''
Crop function.
'''


from PIL import Image
import os
from tqdm import tqdm
from IPython.display import display


dir = "im2latex/gold_formula_images/"
dir_save = "im2latex/crop_formula_images/"


def crop(dir, dir_save):
    '''
    Crops a directory of image rendered latex.

    Args:
        dir: input directory
        dir_save: output directory

    Returns:
        None

    Raises:
        None
    '''
    for filename in tqdm(os.listdir(dir)):
        f = os.path.join(dir, filename)

        if os.path.isfile(f):
            img = Image.open(f)
            # img.show()

            img = img.convert("RGBA")
            pixdata = img.load()
            width, height = img.size

            # find right
            for x in range(width):
                for y in range(height):
                    if pixdata[x, y] == (0, 0, 0, 255):
                        right = x
                        break
            # find left
            for x in reversed(range(width)):
                for y in range(height):
                    if pixdata[x, y] == (0, 0, 0, 255):
                        left = x
                        break
            # find bottom
            for y in range(height):
                for x in range(width):
                    if pixdata[x, y] == (0, 0, 0, 255):
                        bottom = y
                        break
            # find top
            for y in reversed(range(height)):
                for x in range(width):
                    if pixdata[x, y] == (0, 0, 0, 255):
                        top = y
                        break
            # print(left,top,right,bottom)
            img = img.crop((left-220, top-110, right+220, bottom+110))

            img.save(dir_save+filename, "PNG")
