from pybboxes import BoundingBox
import pybboxes as pbx
from typing import Union,List
from dataclasses import dataclass
import numpy as np
import torch
from PIL import Image

@dataclass
class Detection:
    bbox: BoundingBox
    cls: Union[str,int] = None
    constructors_of_supported_formats = {'yolo': BoundingBox.from_yolo,'coco':BoundingBox.from_coco,
                                         'voc':BoundingBox.from_voc,'fiftyone':BoundingBox.from_fiftyone,
                                         'albumentations':BoundingBox.from_albumentations}

    @classmethod
    def load_generic_mode(cls, bbox, image_size, from_type='yolo', to_type="coco", cl=None):
        bbox = pbx.convert_bbox(bbox, from_type=from_type, to_type=to_type, image_size=image_size)
        return cls(bbox, cl)
        
@dataclass
class ImageDetectionSample:
    image: Union[np.array, torch.Tensor, Image.Image]
    detections: List[Detection] = None





