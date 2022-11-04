from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

import torch
import torchvision.transforms as T
import torchvision.transforms.functional as TF
from torchvision.utils import save_image

from torchvision.io import read_image, write_jpeg

import os


import random


image = Image.open(str(Path('1a0db875f9.png')))
image = image.convert('RGB')

to_tensor = T.ToTensor()
to_pil = T.ToPILImage()

# dims = image.shape

# image = image.reshape((dims[1], dims[2], dims[0]))

# print(image.shape)


proportionality = 0.7

path = Path('output')

if not path.exists():
    os.mkdir(path)


def augment(imgs):
    for name, img in imgs:
        a = to_tensor(img)
        dims = a.shape

        new_dims = (int(dims[1] * proportionality),
                    int(dims[2] * proportionality))

        temp_path = path / 'name'

        if not temp_path.exists():
            os.mkdir(temp_path)

        temp_path_folder = temp_path / 'transformed'

        if not temp_path_folder.exists():
            os.mkdir(temp_path_folder)

        img.save(temp_path / 'original_file.jpeg')

        for i in range(5):
            random_crop_func = T.RandomCrop(size=new_dims)
            test = random_crop_func(a)
            to_pil(test).save(temp_path_folder / f'{i}.jpeg')


class Rotatations:
    """Rotate by one of the given angles."""

    def __init__(self, angles):
        self.angles = angles

    def __call__(self, x):
        angle = random.choice(self.angles)
        return TF.rotate(x, angle)


# rotation_transform = Rotatations(angles=[-30, -15, 0, 15, 30])

# print(image.shape)


augment([('testing_image', image)])


# randomcrop = T.RandomCrop()
