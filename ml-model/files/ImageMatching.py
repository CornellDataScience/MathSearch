
import json

import numpy as np
import pandas as pd
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
    """Computes embedding layer of an image. 

    Args:
      x: torch tensor representing image.

    Returns:
      Embedding tensor.

    Raises:
      None
    """
		# It will take the input 'x' until it returns the feature vector called 'out'
    out = self.features(x)
    out = self.pooling(out)
    out = self.flatten(out)
    out = self.fc(out) 
    return out 


def get_similarity(img_1_path, img_2_path):
  """Computes similarity measure between 2 images. 

  Args:
    img1_name: string address to 1st image
    img2_name: string address to 2nd image

  Returns:
    Float cosine similarity from VGG embedding

  Raises:
      None
  """
  img1 = torch.from_numpy(np.array(Image.open(img_1_path).convert(mode='RGB'))).permute(2, 0, 1).unsqueeze(0).float()
  img2 = torch.from_numpy(np.array(Image.open(img_2_path).convert(mode='RGB'))).permute(2, 0, 1).unsqueeze(0).float()
  one = feature_extrator.forward(img1).detach().flatten()
  two = feature_extrator.forward(img2).detach().flatten()
  return np.dot(one, two)/(np.linalg.norm(one)*np.linalg.norm(two))


if __name__ == "__main__":
  """
  Returns top5.csv containing top 5 matches of [target.json] 
  by iterating over all rows in [img_database.csv]

  Args:
    target.json: file name of target image
    img_database.csv: table with 2 rows 
      (image_name = file name, image_source = which pdf its from)
  """
  vgg19_model = models.vgg19(pretrained=True)
  feature_extrator = FeatureExtractor(vgg19_model)

  target = json.load(open("target.json"))['name']
  db = pd.read_csv("img_database.csv")

  similarity_scores = []
  for _, row in db.iterrows():
    similarity_scores.append(get_similarity("target/"+target, "dataset/"+row["image_name"]))
  
  top5 = pd.DataFrame(columns=db.columns)
  top5_index = sorted(range(len(similarity_scores)), key=lambda i: similarity_scores[i])[-5:]
  top5_index.reverse()

  for idx in top5_index:
    top5 = top5.append(db.iloc[idx])
  
  # print(similarity_scores)
  # print(top5_index)

  top5.to_csv("top5.csv", index=False)

  # img_1_path = "image1.jpg"
  # img_2_path = "image2.jpg"

  # get_similarity(img_1_path, img_2_path)

  # print("1 1",np.dot(one, one)/(np.linalg.norm(one)*np.linalg.norm(one)))
  # print("1 2", np.dot(one, two)/(np.linalg.norm(one)*np.linalg.norm(two)))
  # print("2 2", np.dot(two, two)/(np.linalg.norm(two)*np.linalg.norm(two)))
  # print("done")
