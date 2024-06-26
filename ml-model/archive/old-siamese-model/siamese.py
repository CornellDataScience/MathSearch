import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import torchvision.utils
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import models


def imshow(img, text=None, should_save=False):
    npimg = img.numpy()
    plt.axis("off")
    if text:
        plt.text(
            75,
            8,
            text,
            style="italic",
            fontweight="bold",
            bbox={"facecolor": "white", "alpha": 0.8, "pad": 10},
        )
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()


def show_plot(iteration, loss):
    plt.plot(iteration, loss)
    plt.show()


class SiameseNetwork(nn.Module):
  def __init__(self, model):
    super(SiameseNetwork, self).__init__()
		# Extract VGG-16 Feature Layers
    self.features = list(model.features)
    self.features = nn.Sequential(*self.features)
		# Extract VGG-16 Average Pooling Layer
    self.pooling = model.avgpool
		# Convert the image into one-dimensional vector
    self.flatten = nn.Flatten()
		# Extract the first part of fully-connected layer from VGG16
    self.fc = model.classifier[0]
  
  def forward_once(self, x):
        # Forward pass 
        out = self.features(x)
        out = self.pooling(out)
        out = self.flatten(out)
        out = self.fc(out) 
        return out

  def forward(self, input1, input2):
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)
        return output1, output2


# from https://github.com/seanbenhur/siamese_net/blob/master/siamese-net/train.py
# and https://towardsdatascience.com/a-friendly-introduction-to-siamese-networks-85ab17522942
class ContrastiveLoss(torch.nn.Module):

    def __init__(self, margin=1.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, x0, x1, y):
        # euclidian distance
        diff = x0 - x1
        dist_sq = torch.sum(torch.pow(diff, 2), 1)
        dist = torch.sqrt(dist_sq)

        mdist = self.margin - dist
        dist = torch.clamp(mdist, min=0.0)
        loss = y * dist_sq + (1 - y) * torch.pow(dist, 2)
        loss = torch.sum(loss) / 2.0 / x0.size()[0]
        return loss


# preprocessing and loading the dataset
class SiameseDataset:
    def __init__(self, training_csv=None, training_dir=None, transform=None):
        # used to prepare the labels and images path
        self.train_df = pd.read_csv(training_csv)
        # self.train_df = pd.read_csv(training_csv)
        # self.train_df.columns = ["image1", "image2", "label"]
        self.train_dir = training_dir
        self.transform = transform

    def __getitem__(self, index):

        # getting the image path
        image1_path = os.path.join(self.train_dir, self.train_df.iat[index, 0])
        image2_path = os.path.join(self.train_dir, self.train_df.iat[index, 1])

        # Loading the image
        img0 = Image.open(image1_path).convert(mode='RGB')
        img1 = Image.open(image2_path).convert(mode='RGB')
        # img0 = img0.convert("L")
        # img1 = img1.convert("L")

        # Apply image transformations
        if self.transform is not None:
            img0 = self.transform(img0)
            img1 = self.transform(img1)

        return (
            img0,
            img1,
            torch.from_numpy(
                np.array([int(self.train_df.iat[index, 2])], dtype=np.float32)
            ),
        )

    def __len__(self):
        return len(self.train_df)

class ContrastiveLoss(nn.Module):
    "Contrastive loss function"

    def __init__(self, margin=2.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, output1, output2, label):
        euclidean_distance = F.pairwise_distance(output1, output2)
        loss_contrastive = torch.mean(
            (1 - label) * torch.pow(euclidean_distance, 2)
            + (label)
            * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2)
        )

        return loss_contrastive

if __name__ == "__main__":
    df = pd.DataFrame(columns=['image1', 'image2', 'label'])
    df_test = pd.DataFrame(columns=['image1', 'image2', 'label'])
    data_dir = "training_data/Training-Data-MathSearch/output"
    c = 0
    for f in os.listdir(data_dir):

        if c > 20: 
                df.to_csv("train_data.csv", index=False, header=False)
                df_test.to_csv("test_data.csv", index=False, header=False)
                break
        
        r1 = os.path.join(data_dir, random.choice(os.listdir(data_dir))) # random directory
            
        r0 = random.choice(os.listdir(os.path.join(data_dir, f, "transformed")))
        r0 = os.path.join(data_dir, f, "transformed", r0)

        if c % 10 != 0:
            # image transform with random original
            df.loc[len(df.index)] = [r0, os.path.join(r1, 'original_file.jpeg'), 0] 
            
            # image transform with its own original
            df.loc[len(df.index)] = [r0, os.path.join(data_dir, f,"original_file.jpeg"), 1]
            c += 1
        
        if c % 10 == 0:
            # image transform with random original
            df_test.loc[len(df.index)] = [r0, os.path.join(r1, 'original_file.jpeg'), 0] 
            
            # image transform with its own original
            df_test.loc[len(df.index)] = [r0, os.path.join(data_dir, f,"original_file.jpeg"), 1]
            c += 1

    # raise AssertionError

    training_dir = ""
    training_csv = "train_data.csv"
    testing_csv = "test_data.csv"
    testing_dir = ""
    vgg19_model = models.vgg19(pretrained=True)

    net = SiameseNetwork(vgg19_model)
    #   net = SiameseNetwork()
    criterion = ContrastiveLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=1e-3, weight_decay=0.0005)

    # Load the the dataset from raw image folders
    siamese_dataset = SiameseDataset(
        training_csv,
        training_dir,
        # transform=transforms.ToTensor(),
        transforms.Compose(
            [transforms.Resize((105, 105)), transforms.ToTensor()]
        ),
    )

    # Viewing the sample of images and to check whether its loading properly
    vis_dataloader = DataLoader(siamese_dataset, shuffle=True, batch_size=8)
    dataiter = iter(vis_dataloader)



    train_dataloader = DataLoader(siamese_dataset,
                            shuffle=True,
                            num_workers=8,
                            batch_size=32) 

    test_dataset = SiameseDataset(training_csv=testing_csv,training_dir=training_dir,
                                            transform=transforms.Compose([transforms.Resize((105,105)),
                                                                            transforms.ToTensor()
                                                                            ])
                                            )

    test_dataloader = DataLoader(test_dataset,num_workers=6,batch_size=1,shuffle=True)

    #train the model
    def train():
        loss=[] 
        counter=[]
        iteration_number = 0

        k = 0
        for epoch in range(1, 2):
            for i, data in enumerate(test_dataloader,0):
                k += 1
                if k % 10 == 0: print(k)
            # for i, data in enumerate(train_dataloader,0):
                img0, img1 , label = data
                # img0, img1 , label = img0.cuda(), img1.cuda() , label.cuda()
                optimizer.zero_grad()
                output1,output2 = net(img0,img1)
                loss_contrastive = criterion(output1,output2,label)
                loss_contrastive.backward()
                optimizer.step()    
            print("Epoch {}\n Current loss {}\n".format(epoch,loss_contrastive.item()))
            iteration_number += 10
            counter.append(iteration_number)
            loss.append(loss_contrastive.item())
        show_plot(counter, loss)   
        return net


    #set the device to cuda
    device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')

    #   device = torch.device('cpu')
    model = train()
    torch.save(model.state_dict(), "model.pt")
    print("Model Saved Successfully") 


    #test the network
    count=0
    for i, data in enumerate(test_dataloader,0): 
        x0, x1 , label = data
        concat = torch.cat((x0,x1),0)
        output1,output2 = model(x0.to(device),x1.to(device))

        eucledian_distance = F.pairwise_distance(output1, output2)
        
        if label==torch.FloatTensor([[0]]):
            label="Original Pair Of Signature"
        else:
            label="Forged Pair Of Signature"
        
        imshow(torchvision.utils.make_grid(concat))
        print("Predicted Eucledian Distance:-",eucledian_distance.item())
        print("Actual Label:-",label)
        count=count+1
        if count ==10:
            break
