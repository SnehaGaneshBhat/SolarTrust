from ultralytics import YOLO
import os, glob, json

# Load YOLO model (pretrained)
model = YOLO("yolov8s.pt")  # downloads automatically

# Pick your test images
IMAGE_DIR = "data/test"
OUT_DIR = "outputs/predictions"
os.makedirs(OUT_DIR, exist_ok=True)

results = []
for img_path in glob.glob(os.path.join(IMAGE_DIR, "*.*")):
    r = model.predict(img_path, conf=0.25, iou=0.45, verbose=False)[0]
    boxes = []
    for i in range(len(r.boxes)):
        xyxy = r.boxes.xyxy[i].tolist()   # box coordinates
        conf = float(r.boxes.conf[i].item())  # confidence
        boxes.append({"xyxy": xyxy, "conf": conf})
    results.append({"image": os.path.basename(img_path), "boxes": boxes})

# Save predictions
with open(os.path.join(OUT_DIR, "predictions.json"), "w") as f:
    json.dump(results, f, indent=2)