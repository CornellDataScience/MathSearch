# ML Model Branch

## Design choice

We link the design choices in the follow google docs;
https://docs.google.com/document/d/1vf85MGTYNEiqmlLApEDHS9gEdpwMC6Jg1svBZvlxrbo/edit?usp=sharing

## Folders

- preprocessing/ - code for dataset augmentation, 
- files/ - code for VGG
- model/ - code for VGG and Siamese neural networks
- yolov5/ - all the code for yolov5
- archive/ - deprecated folders 

# Setup

### Requirements
Install requirements via `pip install -r requirements.txt` in the files/ directory.
### Finetuning

- #### Siamese w/ VGG 
    The dataset used to finetune VGG can be found here, in `training.zip`: https://huggingface.co/dyk34/Training-Data-MathSearch/tree/main.

    Change the `data_dir, training_dir, training_csv, testing_csv, testing_dir` variables in the `siamese.py` file.

    Run `python siamese.py`.

- #### Yolov5
    The dataset to finetune Yolov5 can also be found here: https://huggingface.co/dyk34/Training-Data-MathSearch/tree/main.


### Inference
- #### Siamese w/ VGG
To run VGG in Pytorch, load a Siamese Network with 
```
vgg19_model = models.vgg19()
net = SiameseNetwork(vgg19_model)
model.load_state_dict(torch.load('model.pt'))
```

and run `model(image1, image2)` to get the latent space distance between image1 and image2.


- ### Yolov5
To segment an image, run

`python segment/predict.py --weights {weights} --data  {img}`

# SWE
<img width="700" alt="full pipeline" src="https://github.com/CornellDataScience/MathSearch/assets/44758321/bcb8dff2-0e21-474f-9f19-915cda76262c">


## Frontend Public IP
### As time: 5/29 3:12PM
Everytime EC2 instance gets restarted, new IP and new SSH ip is be generated and need to be updated for config and domain redirection.

Public IP: `http://18.206.12.64`  
SSH: `ec2-18-206-12-64.compute-1.amazonaws.com`

## Nginx
location of nginx conf: `/etc/nginx/nginx.conf`  
be in `/home/ubuntu/MathSearch/ml-model/web`
```
gunicorn -b 127.0.0.1:8080 api:app
```

## Backend Environment:
- Option 1: `/opt/conda/bin`
- Option 2: `/home/ubuntu/MathSearch/ml-model/venv/bin`
- Option 3 (apply to SWE): packages all installed to default python, no need to activate any venv

## Access S3
To test connection, run below (notice the "-" on the second option). It should display directory in s3 buckets or cat the file.

option 1
```
aws s3 ls s3://mathsearch-intermediary
```
option 2
```
aws s3 cp s3://mathsearch-intermediary/test.txt -
```
