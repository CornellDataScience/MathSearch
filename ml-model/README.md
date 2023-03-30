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

- #### VGG 
    The dataset used to finetune VGG can be found here, in `training.zip`: https://huggingface.co/dyk34/Training-Data-MathSearch/tree/main.

    Change the `data_dir, training_dir, training_csv, testing_csv, testing_dir` variables in the `siamese.py` file.

    Run `python siamese.py`.

- #### Yolov5
    The dataset to finetune Yolov5 can also be found here: https://huggingface.co/dyk34/Training-Data-MathSearch/tree/main.


### Inference
- #### VGG
To run VGG in Pytorch, load a Siamese Network with 
```
vgg19_model = models.vgg19()
net = SiameseNetwork(vgg19_model)
model.load_state_dict(torch.load('model.pt'))
```

and run `model(image1, image2)` to get the latent space distance between image1 and image2.


- #### Yolov5
To segment an image, run

`python segment/predict.py --weights {weights} --data  {img}`
