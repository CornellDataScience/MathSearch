
import json

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from PIL import Image
from torchvision import models

import os


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
      img1 = torch.from_numpy(np.array(Image.open(img_1_path).convert(mode='RGB'))).permute(2, 0, 1).unsqueeze(0).float()
      img2 = torch.from_numpy(np.array(Image.open(img_2_path).convert(mode='RGB'))).permute(2, 0, 1).unsqueeze(0).float()
      one = feature_extrator.forward(img1).detach().flatten()
      two = feature_extrator.forward(img2).detach().flatten()
      return np.dot(one, two)/(np.linalg.norm(one)*np.linalg.norm(two))

def manually_create_db():
  # Get list of files written to YOLO output, except for target_file_name
  dir_list = [str(x) for x in os.listdir('/home/ubuntu/MathSearch/ml-model/yolov5/ranking/dcopy/exp/crops/equation')]

  # Construct tbl of generated crops for similarity detection model 
  img_database = pd.DataFrame(columns = ['image_name', 'image_source', 'coo_1', 'coo_2', 'coo_3', 'coo_4'])

  for f in dir_list:
    img_source, rem  = f.split("__")
    eq_number = img_source.split("_")[1]

    eq_number = 1 if eq_number == '' else eq_number

    df = pd.read_csv('/home/ubuntu/MathSearch/ml-model/yolov5/ranking/img_database.csv', delim_whitespace=True, header=None) 
    # new_row = {'image_name': f, 'image_source': img_source, 'coo_1':df.iloc[int(eq_number) - 1, 1],  
    # 'coo_2':df.iloc[int(eq_number) - 1, 2], 'coo_3': df.iloc[int(eq_number) - 1, 3], 'coo_4': df.iloc[int(eq_number) - 1, 4]} 
    
    new_row = {'image_name': f, 'image_source': img_source, 'coo_1':"",  
    'coo_2':"", 'coo_3': "", 'coo_4': ""} 
    
    print(new_row)
    img_database = img_database.append(new_row, ignore_index = True) 

  img_database.to_csv("/home/ubuntu/MathSearch/ml-model/yolov5/ranking/img_database.csv") 

if __name__ == "__main__":
  '''
  Formatting for running this file:

  ranking/query/ - put querying images here
  ranking/target.json - images you want to query
  
  
  This should be created automatically via bash run_model.sh in the main folder
  ranking/database/exp/crops/equations - database of cropped images

  This should be created automatically via the pipeline but can be created using the manually_create_db() func above
  ranking/img_database.csv
  '''

  # manually_create_db()


  # vgg19_model = models.vgg19(pretrained=True)
  vgg19_model = models.efficientnet_b0(pretrained=True)
  feature_extrator = FeatureExtractor(vgg19_model)

  target = json.load(open("ranking/target.json"))['name']
  db = pd.read_csv("ranking/img_database.csv")

  similarity_scores = []
  for _, row in db.iterrows():
    similarity_scores.append(get_similarity("ranking/query/"+target, "ranking/dataset/exp/crops/equation/"+row["image_name"]))
    # similarity_scores.append(get_similarity("ranking/query/"+target, "ranking/database/"+row["image_name"]))

  top5 = pd.DataFrame(columns=db.columns)
  top5_index = sorted(range(len(similarity_scores)), key=lambda i: similarity_scores[i])[-5:]
  top5_index.reverse()

  print("Similarity scores", similarity_scores)
  
  for idx in top5_index:
    top5 = top5.append(db.iloc[idx])
  
  # print(similarity_scores)
  # print(top5_index)

    # top5.to_json('ranking/top5.json')
  top5.to_csv("ranking/top5.csv", index=False, header=False)
  print("ML Model Completed")
  # img_1_path = "image1.jpg"
  # img_2_path = "image2.jpg"

  # get_similarity(img_1_path, img_2_path)

  # print("1 1",np.dot(one, one)/(np.linalg.norm(one)*np.linalg.norm(one)))
  # print("1 2", np.dot(one, two)/(np.linalg.norm(one)*np.linalg.norm(two)))
  # print("2 2", np.dot(two, two)/(np.linalg.norm(two)*np.linalg.norm(two)))
  # print("done")
