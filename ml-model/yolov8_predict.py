from ultralytics import YOLO
import os

# Load a model
model = YOLO('runs/detect/train/weights/best.pt')  # load custom equation model
print("Loaded YOLO model!")
img_directory = 'datasets/eqn-images-dataset/images/train'

# Predict with the model
img_lst = [os.path.join(img_directory, img) for img in os.listdir(img_directory)] 
results = model(img_lst)
print("Ran YOLO model on img_dir!")

# process results, save cropped images
for r in results:
  r.save_crop('cropped_data/')
print("Saved crops!")

