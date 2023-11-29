from abc import abstractmethod
from typing import List

import torch
import torchvision.transforms.functional as F
from PIL import Image


class TransformBase:
    """Base class for both pre-processing and augmentation transforms"""

    @staticmethod
    def _validate_input(img):
        if len(img.shape) != 4:
            raise ValueError("img must be a rank 4 tensor")

    def __call__(
        self,
        img: torch.Tensor,
        mask: Image.Image = None,
        bbox_dict: dict = None,
    ):
        """
        Parameters
        ----------
        img
            should be a rank 4 image tensor
        mask : Image.Image
            segmentation mask
        bbox_dict : dict
            dict with keys "bboxes" and "classes"

        Returns
        -------
        torch.Tensor or tuple
            If only img is passed then the return is the transformed image. Otherwise it is
            a tuple with the first item the transformed image and the other items
            the transformed annotations.
        """
        self._validate_input(img)
        ret = [self._convert_img_tensor(img)]
        if mask is not None:
            ret.append(self._convert_mask(mask))
        if bbox_dict is not None:
            new_bbox_dict = {"bboxes": [], "classes": []}
            for bbox, label in zip(bbox_dict["bboxes"], bbox_dict["classes"]):
                new_bbox = self._convert_bbox(bbox)
                if new_bbox is not None:
                    new_bbox_dict["bboxes"].append(new_bbox)
                    new_bbox_dict["classes"].append(label)

            ret.append(new_bbox_dict)

        return tuple(ret) if len(ret) > 1 else ret[0]

    @abstractmethod
    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError

    @abstractmethod
    def _convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        raise NotImplementedError

    @abstractmethod
    def _convert_coords(self, coords, img_h, img_w, invert=False):
        raise NotImplementedError

    def _convert_mask(self, mask):
        return F.to_pil_image(
            self._convert_img_tensor(F.to_tensor(mask).unsqueeze(0))[0]
        )


class ImageOnlyTransform(TransformBase):
    """Base class for transforms that do not change bounding boxes or masks, such as
    color jitters, histogram transforms, etc.
    """

    def _convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        return bbox

    def _convert_coords(self, coords, img_h, img_w, invert=False):
        return coords

    def _convert_mask(self, mask):
        return mask


class IdentityTransform(ImageOnlyTransform):
    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        return img


class Compose(TransformBase):
    """Composes several transforms together."""

    __serialization_attributes__ = ["transforms"]

    def __init__(self, transforms: List[TransformBase]):
        """
        Parameters
        ----------
        transforms : list
            list of transforms to compose
        """
        self.transforms = transforms

    def _convert_img_tensor(self, img):
        for t in self.transforms:
            img = t._convert_img_tensor(img)
        return img

    def _convert_mask(self, mask):
        for t in self.transforms:
            mask = t._convert_mask(mask)
        return mask

    def _convert_bbox(self, bbox):
        for t in self.transforms:
            bbox = t._convert_bbox(bbox)
            if bbox is None:
                return None
        return bbox

    def __repr__(self):
        format_string = self.__class__.__name__ + "("
        for t in self.transforms:
            format_string += "\n"
            format_string += "    {0}".format(t)
        format_string += "\n)"
        return format_string

    def __eq__(self, other: object) -> bool:
        if self.__class__ != other.__class__:
            return False
        if len(self.transforms) != len(other.transforms):
            return False
        for t1, t2 in zip(self.transforms, other.transforms):
            if t1 != t2:
                return False
        return True
