
import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import models


class FeatureExtractor(nn.Module):
  def __init__(self, model):
    super(FeatureExtractor, self).__init__()
		# Extract VGG-16 Feature Layers
    self.features = list(model.features)
    self.features = nn.Sequential(*self.features)
		# Extract VGG-16 Average Pooling Layer
    self.pooling = model.avgpool
		# Convert the image into one-dimensional vector
    self.flatten = nn.Flatten()
		# Extract the first part of fully-connected layer from VGG16
    self.fc = model.classifier[0]
  
  def forward(self, x):
		# It will take the input 'x' until it returns the feature vector called 'out'
    out = self.features(x)
    out = self.pooling(out)
    out = self.flatten(out)
    out = self.fc(out) 
    return out 


def get_similarity(img_1_path, img_2_path):
      img1 = torch.from_numpy(np.array(Image.open(img_1_path))).permute(2, 0, 1).unsqueeze(0).float()
      img2 = torch.from_numpy(np.array(Image.open(img_2_path))).permute(2, 0, 1).unsqueeze(0).float()
      one = feature_extrator.forward(img1).detach().flatten()
      two = feature_extrator.forward(img2).detach().flatten()
      return np.dot(one, two)/(np.linalg.norm(one)*np.linalg.norm(two))


if __name__ == "__main__":
  vgg19_model = models.vgg19(pretrained=True)
  feature_extrator = FeatureExtractor(vgg19_model)
  
  img_1_path = "image1.jpg"
  img_2_path = "image2.jpg"

  get_similarity(img_1_path, img_2_path)

  # print("1 1",np.dot(one, one)/(np.linalg.norm(one)*np.linalg.norm(one)))
  # print("1 2", np.dot(one, two)/(np.linalg.norm(one)*np.linalg.norm(two)))
  # print("2 2", np.dot(two, two)/(np.linalg.norm(two)*np.linalg.norm(two)))
  # print("done")
