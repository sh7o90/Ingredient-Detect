import os
import torch

# PyTorch 2.6+ の weights_only=True デフォルト変更に対する互換パッチ
_original_torch_load = torch.load
def _patched_torch_load(*args, **kwargs):
    if "weights_only" not in kwargs:
        kwargs["weights_only"] = False
    return _original_torch_load(*args, **kwargs)

torch.load = _patched_torch_load

from ultralytics import YOLO

def detect_objects(image_path):
    pt_best = "mybest.pt"
    model = YOLO(pt_best)
    results = model.predict(image_path, name="../../tmp/", imgsz=320, exist_ok=True, save=True)
    return results


