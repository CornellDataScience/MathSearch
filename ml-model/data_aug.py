from PIL import Image

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import torch
import torchvision.transforms as T
import torchvision.transforms.functional as TF
from torchvision.utils import save_image

from torchvision.io import read_image, write_jpeg

from tqdm import tqdm

import os
import random

from concurrent.futures import ProcessPoolExecutor, as_completed


to_tensor = T.ToTensor()
to_pil = T.ToPILImage()

blur = T.GaussianBlur((7, 13))


def img_input(file_name, name):
    image = Image.open(str(Path(file_name)))
    image = image.convert('RGB')

    return (name, image)

# dims = image.shape

# image = image.reshape((dims[1], dims[2], dims[0]))

# print(image.shape)


proportionality = 0.7

path = Path('output')

if not path.exists():
    os.mkdir(path)


def augment(name, img):

    temp_path = path / name

    if not temp_path.exists():
        os.mkdir(temp_path)
    else:
        return

    a = to_tensor(img)
    dims = a.shape

    new_dims = (int(dims[1] * proportionality),
                int(dims[2] * proportionality))

    temp_path_folder = temp_path / 'transformed'

    if not temp_path_folder.exists():
        os.mkdir(temp_path_folder)

    img.save(temp_path / 'original_file.jpeg')

    img_left = torch.rot90(a, dims=[1, 2])

    to_pil(img_left).save(temp_path_folder / 'left_rotate.jpeg')

    img_right = torch.rot90(a, k=3, dims=[1, 2])
    to_pil(img_right).save(temp_path_folder / 'right_rotate.jpeg')

    # random crop
    for i in range(5):
        random_crop_func = T.RandomCrop(size=new_dims)
        test = random_crop_func(a)
        to_pil(test).save(temp_path_folder / f'{i}_randomcrop.jpeg')

    blurs = [blur(img) for _ in range(5)]

    for i, j in enumerate(blurs):
        j.save(temp_path_folder / f'{i}_blur.jpeg')


# with ProcessPoolExecutor(max_workers=4) as executor:
for filename in tqdm(os.listdir('crop_formula_images')):
    name, img = img_input(f'crop_formula_images/{filename}', filename)
    augment(name, img)


class Rotatations:
    """Rotate by one of the given angles."""

    def __init__(self, angles):
        self.angles = angles

    def __call__(self, x):
        angle = random.choice(self.angles)
        return TF.rotate(x, angle)


# randomcrop = T.RandomCrop()
