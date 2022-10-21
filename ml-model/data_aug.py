from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

import torch
import torchvision.transforms as T
import torchvision.transforms.functional as TF
from torchvision.utils import save_image

import random


image = Image.open(Path('formula_images') / 'fffd617779.png')
class Rotatations:
    """Rotate by one of the given angles."""

    def __init__(self, angles):
        self.angles = angles

    def __call__(self, x):
        angle = random.choice(self.angles)
        return TF.rotate(x, angle)

rotation_transform = Rotatations(angles=[-30, -15, 0, 15, 30])

x = rotation_transform(image)
print(x)
x.show()