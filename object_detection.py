import os
from ultralytics import YOLO

def detect_objects(image_path):
    pt_path = "yolov8n.pt"
    pt_best = "mybest.pt"
    model = YOLO(pt_path)
    model = YOLO(pt_best)
    results = model.predict(image_path, name="../../tmp/", imgsz=320, exist_ok=True, save=True)
    return results
