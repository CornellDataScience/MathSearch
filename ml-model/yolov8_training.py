from ultralytics import YOLO

# Load a model
model = YOLO('eqn-detect.yaml')  # build a new model from YAML
model = YOLO('yolov8m.pt')  # load a pretrained model (recommended for training)
model = YOLO('eqn-detect.yaml').load('yolov8m.pt')  # build from YAML and transfer weights

# Train the model
results = model.train(data='eqn-detect.yaml', epochs=100, imgsz=640, task=detect, verbose=True)