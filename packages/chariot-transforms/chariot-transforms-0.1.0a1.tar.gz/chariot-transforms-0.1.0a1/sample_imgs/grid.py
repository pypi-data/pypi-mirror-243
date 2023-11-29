"""
This script makes a grid for each augmentation in RandAugment. The first row
is with the lowest magnitude, the second is with a small magnitude, and the third
is with the highest magnitude. The resulting images will be in the `sample_imgs/augmentations` folder
"""


import os
from pathlib import Path

from PIL import Image
from torchvision.transforms.functional import to_pil_image, to_tensor
from torchvision.utils import make_grid

from chariot_transforms.augmentations.transforms import RandAugment

augmentations = RandAugment.augmentations

base_path = Path(__file__).parent
img = to_tensor(Image.open(base_path / "guy_with_car.jpg")).unsqueeze(0)

out_path = base_path / "augmentations"
os.makedirs(out_path, exist_ok=True)

bbox_dict = {
    "bboxes": [[64, 218, 250, 304], [87, 18, 271, 269]],
    "classes": ["person", "car"],
}


def get_percentile(high, low, p):
    return low + (high - low) * p


def draw_bounding_box_on_tensor(img, channel, ymin, xmin, ymax, xmax):
    img = img.clone()

    ymin = int(ymin)
    xmin = int(xmin)
    ymax = int(ymax)
    xmax = int(xmax)

    img[:, channel, ymin, xmin:xmax] = 1
    img[:, channel, ymax, xmin:xmax] = 1
    img[:, channel, ymin:ymax, xmin] = 1
    img[:, channel, ymin:ymax, xmax] = 1
    return img


def draw_bbox_dict_on_img(img, bbox_dict):
    class_to_channel = {"person": 0, "car": 1}
    for bbox, label in zip(bbox_dict["bboxes"], bbox_dict["classes"]):
        ymin, xmin, ymax, xmax = bbox
        img = draw_bounding_box_on_tensor(
            img, class_to_channel[label], ymin, xmin, ymax, xmax
        )
    return img


def apply_transform_and_draw_bbox(img, transform):
    trans_img, trans_bbox_dict = transform(img, bbox_dict=bbox_dict)
    trans_img_with_bboxes = draw_bbox_dict_on_img(trans_img, trans_bbox_dict)
    return trans_img_with_bboxes


n_iters = 10
for name, constr, (low, high) in augmentations:
    grid_imgs = []
    low_trans = constr(low)
    mid_trans = constr(get_percentile(high, low, 0.05))
    high_trans = constr(high)

    for t in [low_trans, mid_trans, high_trans]:
        for _ in range(n_iters):
            grid_imgs.append(apply_transform_and_draw_bbox(img, t)[0])

    grid = make_grid(grid_imgs, n_iters)
    to_pil_image(grid).save(out_path / f"{name}.png")
