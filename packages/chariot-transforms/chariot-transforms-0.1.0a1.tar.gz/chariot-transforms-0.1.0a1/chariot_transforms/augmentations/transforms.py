""" Joint versions of some of the transformations in torchvision.transforms
These are used, for example, in segmentation tasks where the input image and
target (mask) both need to be transformed in the same way.
"""
import math
import numbers
import random
from typing import List, Optional, Tuple, Union

import numpy as np
import torch
from numpy import cos, sin, tan
from PIL import Image, ImageOps

try:
    import torchvision.transforms.v2.functional as F
    from torchvision.transforms.v2 import ColorJitter as _ColorJitter
    from torchvision.transforms.v2 import Grayscale as _Grayscale
except ModuleNotFoundError:
    import torchvision.transforms.functional as F
    from torchvision.transforms import (
        ColorJitter as _ColorJitter,
        Grayscale as _Grayscale,
    )

from chariot_transforms import bbox_ops
from chariot_transforms.base import (
    Compose,
    IdentityTransform,
    ImageOnlyTransform,
    TransformBase,
)
from chariot_transforms.preprocessing import (
    PreprocessingTransform,
    Resize,
    ResizePreserveAspect,
)

__all__ = [
    "AutoContrast",
    "Brightness",
    "Contrast",
    "Sharpness",
    "Invert",
    "Cutout",
    "Equalize",
    "Solarize",
    "Posterize",
    "Rotation",
    "RandomHorizontalFlip",
    "RandomVerticalFlip",
    "RandomCrop",
    "RandomRotation",
    "RandomPerspective",
    "RandomAffine",
    "ResizePreserveAspect",
    "RandomGrayscale",
    "ColorJitter",
    "Compose",
    "CenterCrop",
    "Resize",
    "RandomResize",
    "Grayscale",
    "PreprocessingTransform",
    "TranslateX",
    "TranslateY",
    "TransformBase",
    "Pad",
    "RandAugment",
]


def float_tensor_to_int_tensor(t: torch.Tensor) -> torch.Tensor:
    return (t * 255).to(torch.uint8)


def int_tensor_to_float_tensor(t: torch.Tensor) -> torch.Tensor:
    return t.to(torch.float32) / 255


def apply_along_classes(mask, fn):
    """
    Parameters
    ----------
    mask : Image.Image
    fn : callable

    Returns
    -------
    Image.Image
    """
    mask_array = np.array(mask)
    classes = [c for c in np.unique(mask_array) if c != 0]
    trans_mask = np.zeros((mask.height, mask.width), dtype=np.uint8)
    for c in classes:
        class_mask = np.zeros_like(mask_array, dtype=np.uint8)
        class_mask[mask_array == c] = 255

        trans_class_mask = np.array(fn(Image.fromarray(class_mask)))
        trans_class_mask[trans_class_mask < 255 // 2] = 0
        trans_class_mask[trans_class_mask >= 255 // 2] = c

        # pixels with different classes might go to the same pixel in
        # the resized image so we need to make sure we don't add these
        # classes together
        trans_mask[trans_class_mask != 0] = 0
        trans_mask += trans_class_mask

    return Image.fromarray(trans_mask)


def get_affine_matrix(
    center: Tuple[int, int],
    angle: float,
    translate: Tuple[int, int],
    scale: float,
    shear: Tuple[float, float],
):
    """
    Inverse of _get_inverse_affine_matrix from torchvision.transforms.functional

    Helper method to compute inverse matrix for affine transformation
    copied from torchvision.functional

    Computes transformation matrix: M = T * C * RSS * C^-1
    where T is translation matrix: [1, 0, tx | 0, 1, ty | 0, 0, 1]
          C is translation matrix to keep center: [1, 0, cx | 0, 1, cy | 0, 0, 1]
          RSS is rotation with scale and shear matrix
          RSS(a, s, (sx, sy)) =
          = R(a) * S(s) * SHy(sy) * SHx(sx)
          = [ s*cos(a - sy)/cos(sy), s*(-cos(a - sy)*tan(x)/cos(y) - sin(a)), 0 ]
            [ s*sin(a + sy)/cos(sy), s*(-sin(a - sy)*tan(x)/cos(y) + cos(a)), 0 ]
            [ 0                    , 0                                      , 1 ]

    where R is a rotation matrix, S is a scaling matrix, and SHx and SHy are the shears:
    SHx(s) = [1, -tan(s)] and SHy(s) = [1      , 0]
             [0, 1      ]              [-tan(s), 1]
    """

    if isinstance(shear, numbers.Number):
        shear = [shear, 0]

    if not isinstance(shear, (tuple, list)) and len(shear) == 2:
        raise ValueError(
            "Shear should be a single value or a tuple/list containing "
            + "two values. Got {}".format(shear)
        )

    rot = math.radians(angle)
    sx, sy = [math.radians(s) for s in shear]

    cx, cy = center
    tx, ty = translate

    # RSS without scaling
    a = cos(rot - sy) / cos(sy)
    b = -cos(rot - sy) * tan(sx) / cos(sy) - sin(rot)
    c = sin(rot - sy) / cos(sy)
    d = -sin(rot - sy) * tan(sx) / cos(sy) + cos(rot)

    # rotation matrix with scale and shear
    M = [a, b, 0, c, d, 0]
    M = [x * scale for x in M]

    # Apply inverse center translation
    M[2] += M[0] * (-cx) + M[1] * (-cy)
    M[5] += M[3] * (-cx) + M[4] * (-cy)

    # Apply translation and center translation
    M[2] += cx + tx
    M[5] += cy + ty
    M = M + [0, 0, 1]
    return np.array(M).reshape((3, -1))


class RandomTransform(TransformBase):
    """Base class for transforms that have a random component to them."""

    def set_random_params(self, img):
        """Randomly sets the transformation parameters

        Parameters
        ----------
        img : PIL.Image
        """
        raise NotImplementedError

    def __call__(self, img, *args, **kwargs):
        self.set_random_params(img)
        return super().__call__(img=img, *args, **kwargs)


class AutoContrast(ImageOnlyTransform):
    __serialization_attributes__ = []

    def _convert_img_tensor(self, img):
        return F.autocontrast(img)

    def set_magnitude(self, magnitude: float) -> None:
        return


class Brightness(ImageOnlyTransform):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float) -> None:
        """
        Parameters
        ----------
        magnitude
            magnitude of the brightness, with 0.0 giving a black image and 1.0
            giving the original image.

            (For _convert_img_tensor) How much to adjust the brightness. Can be any non negative number.
            0 gives a black image, 1 gives the original image while 2 increases the brightness
            by a factor of 2
        """
        self.magnitude = magnitude

    def _convert_img_tensor(self, img: Image) -> Image:
        return F.adjust_brightness(img, brightness_factor=self.magnitude)

    def set_magnitude(self, magnitude: float) -> None:
        self.magnitude = magnitude


class RandomBrightness(RandomTransform):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float) -> None:
        """
        Parameters
        ----------
        magnitude
            maximum magnitude of the brightness adjustment.

            Brightness adjusted by a factor between 1-magnitude and 1+magnitude.

            Required: magnitude must be >= 0.
        """
        if magnitude < 0:
            raise ValueError(
                "magnitude must be non-negative for brightness adjustment."
            )

        self.magnitude = magnitude

    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        return F.adjust_brightness(img, brightness_factor=self._magnitude)

    def set_magnitude(self, magnitude: float) -> None:
        self.magnitude = magnitude

    def set_random_params(self, img: Image) -> None:
        self._magnitude = np.random.uniform(
            low=max(0, 1 - self.magnitude), high=1 + self.magnitude
        )

    def _convert_bbox(self, bbox):
        return bbox

    def _convert_mask(self, mask):
        return mask


class Contrast(ImageOnlyTransform):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float) -> None:
        """
        Parameters
        ----------
        mangitude
            How much to adjust the contrast. Can be any non negative number.
            0 gives a solid gray image, 1 gives the original image while
            2 increases the contrast by a factor of 2
        """
        self.magnitude = magnitude

    def _convert_img_tensor(self, img: torch.Tensor):
        return F.adjust_contrast(img, contrast_factor=self.magnitude)

    def set_magnitude(self, magnitude: float) -> None:
        self.magnitude = magnitude


class RandomContrast(RandomTransform):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float) -> None:
        """
        Parameters
        ----------
        magnitude
            maximum magnitude of the contrast adjustment.

            Contrast adjusted by a factor between 1-magnitude and 1+magnitude.

            Required: magnitude must be >= 0.
        """
        if magnitude < 0:
            raise ValueError(
                "magnitude must be non-negative for contrast adjustment."
            )

        self.magnitude = magnitude

    def _convert_img_tensor(self, img: torch.Tensor):
        return F.adjust_contrast(img, contrast_factor=self._magnitude)

    def set_magnitude(self, magnitude: float) -> None:
        self.magnitude = magnitude

    def set_random_params(self, img: Image) -> None:
        self._magnitude = np.random.uniform(
            low=max(0, 1 - self.magnitude), high=1 + self.magnitude
        )

    def _convert_bbox(self, bbox):
        return bbox

    def _convert_mask(self, mask):
        return mask


class Hue(ImageOnlyTransform):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float) -> None:
        """
        Parameters
        ----------
        mangitude
            How much to shift the hue channel. Should be in [-0.5, 0.5]. 0.5 and -0.5 give complete reversal
            of hue channel in HSV space in positive and negative direction respectively. 0 means no shift. Therefore,
            both -0.5 and 0.5 will give an image with complementary colors while 0 gives the original image.
        """
        self.magnitude = magnitude

    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        return F.adjust_hue(img, hue_factor=self.magnitude)

    def set_magnitude(self, magnitude: float) -> None:
        self.magnitude = magnitude


class Gamma(ImageOnlyTransform):
    __serialization_attributes__ = ["magnitude", "gain"]

    def __init__(self, magnitude: float, gain: float = None) -> None:
        """
        Parameters
        ----------
        mangitude
            Non negative real number, same as γ in the equation. gamma larger than 1 make the shadows
            darker, while gamma smaller than 1 make dark regions lighter.
        gain
            The constant multiplier.
        """
        self.magnitude = magnitude
        self.gain = gain

    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        if self.gain:
            return F.adjust_gamma(img, gamma=self.magnitude, gain=self.gain)
        else:
            return F.adjust_gamma(img, gamma=self.magnitude)

    def set_magnitude(self, magnitude: float) -> None:
        self.magnitude = magnitude


class Saturation(ImageOnlyTransform):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float) -> None:
        """
        Parameters
        ----------
        mangitude
            How much to adjust the saturation. 0 will give a black and white image, 1 will give the
            original image while 2 will enhance the saturation by a factor of 2.
        """
        self.magnitude = magnitude

    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        return F.adjust_saturation(img, saturation_factor=self.magnitude)

    def set_magnitude(self, magnitude: float) -> None:
        self.magnitude = magnitude


class Sharpness(ImageOnlyTransform):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float) -> None:
        """
        Parameters
        ----------
        mangitude
            magnitude of the sharpness, with 0.0 giving a blurred image, 1.0
            giving the original image, and 2.0 giving a sharpened image.
        """
        self.magnitude = magnitude

    def _convert_img_tensor(self, img: torch.Tensor):
        return F.adjust_sharpness(img, sharpness_factor=self.magnitude)

    def set_magnitude(self, magnitude: float) -> None:
        self.magnitude = magnitude


class RandomSharpness(RandomTransform):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float) -> None:
        """
        Parameters
        ----------
        magnitude
            maximum magnitude of the contrast adjustment.

            Contrast adjusted by a factor between 1-magnitude and 1+magnitude.

            Required: magnitude must be >= 0.
        """
        if magnitude < 0:
            raise ValueError(
                "magnitude for sharpness adjustment must be non-negative."
            )

        self.magnitude = magnitude

    def _convert_img_tensor(self, img: torch.Tensor):
        return F.adjust_sharpness(img, sharpness_factor=self._magnitude)

    def set_magnitude(self, magnitude: float) -> None:
        self.magnitude = magnitude

    def set_random_params(self, img: Image) -> None:
        self._magnitude = np.random.uniform(
            low=max(0, 1 - self.magnitude), high=1 + self.magnitude
        )

    def _convert_bbox(self, bbox):
        return bbox

    def _convert_mask(self, mask):
        return mask


class Equalize(ImageOnlyTransform):
    __serialization_attributes__ = []

    def _convert_img_tensor(self, img: torch.Tensor):
        return int_tensor_to_float_tensor(
            F.equalize(float_tensor_to_int_tensor(img))
        )

    def set_magnitude(self, magnitude: float) -> None:
        return


class Posterize(ImageOnlyTransform):
    __serialization_attributes__ = ["bits"]

    def __init__(self, bits: Union[int, float]) -> None:
        """
        Parameters
        ----------
        bits
            The number of bits to keep in each color channel.
            Should be between 1 and 8.
            Float values get converted to ints.

        Note: small values of bits have larger impact on the image than large values of bits
        because they result in more information being lost.
        """
        bits = int(bits)
        self.bits = bits

    def _convert_img_tensor(self, img):
        return int_tensor_to_float_tensor(
            F.posterize(float_tensor_to_int_tensor(img), self.bits)
        )


class RandomPosterize(RandomTransform):
    __serialization_attributes__ = ["bits"]

    def __init__(self, bits: Union[int, float]) -> None:
        """
        Parameters
        ----------
        bits
            The minimum number of bits to keep in each color channel.
            Should be between 1 and 8.
            Each random draw (for number of bits to keep) will be an integer
            between this number and 8.


        Note: small values of bits have larger impact on the image than large values of bits
        because they result in more information being lost.
        """
        self.bits = [i for i in range(1, 9) if i >= bits]
        if len(self.bits) == 0:
            raise ValueError(
                "The number of bits to keep should be between 1 and 8."
            )

    def set_random_params(self, img):
        self._bits = np.random.choice(self.bits)

    def convert_img(self, img):
        return ImageOps.posterize(img, self._bits)

    def _convert_img_tensor(self, img):
        return F.posterize(img, self._bits)

    def _convert_bbox(self, bbox):
        return bbox

    def _convert_mask(self, mask):
        return mask


class Solarize(ImageOnlyTransform):
    __serialization_attributes__ = ["threshold"]

    def __init__(self, threshold: Union[int, float]) -> None:
        """
        Parameters
        ----------
        threshold
            should be between 0 and 1. all values above this greyscale threshold
            are inverted.

        Note: smaller thresholds result in more pixels being inverted--a larger impact on the image.
        """
        self.threshold = threshold

    def _convert_img_tensor(self, img):
        # we need to add this because F.solarize with a threshold of 1 will send pixels with 1
        # to 0
        if self.threshold == 1:
            return img
        return F.solarize(img, self.threshold)


class RandomSolarize(RandomTransform):
    __serialization_attributes__ = ["threshold"]

    def __init__(self, threshold: Union[int, float]) -> None:
        """
        Parameters
        ----------
        threshold
            Minimum value for threshold for inversion.
            For each iteration, a random threshold will be chosen
            between this value and 256.
            All values above the this greyscale threshold are inverted.

            This value must be between 0 and 256.

        Note: smaller thresholds result in more pixels being inverted--a larger impact on the image.
        """
        if threshold < 0 or threshold > 1:
            raise ValueError("Solarizing threshold must be between 0 and 1.")
        self.threshold = threshold

    def set_random_params(self, img):
        self._threshold = np.random.uniform(low=self.threshold, high=1)

    def _convert_img_tensor(self, img):
        return F.solarize(img, self._threshold)

    def _convert_bbox(self, bbox):
        return bbox

    def _convert_mask(self, mask):
        return mask


class Invert(ImageOnlyTransform):
    __serialization_attributes__ = []

    def _convert_img_tensor(self, img):
        return F.invert(img)

    def set_magnitude(self, magnitude: float) -> None:
        return


class Cutout(RandomTransform):
    """Implementation of the data augmentation discussed in this paper:
    https://arxiv.org/abs/1708.04552
    """

    __serialization_attributes__ = ["length"]

    def __init__(self, length: int) -> None:
        """
        Parameters
        ----------
        length
            side length of the square to cutout. the original paper finds the
            optimal value via a grid search. their results are:

            - 16 for CIFAR10, 8 for CIFAR100
            - 20 for SVHN
            - 24 for STL10 if not using data augmentation, and 32 if training
              with augmentation.
        """
        self.length = length

    def set_random_params(self, img):
        h, w = img.shape[2:]
        center = np.array(
            [
                random.randint(0, h - 1),
                random.randint(0, w - 1),
            ]
        )
        self.ymin, self.xmin = np.clip(
            center - [self.length // 2, self.length // 2], a_min=0, a_max=None
        )
        self.ymax, self.xmax = np.clip(
            center + [self.length // 2, self.length // 2],
            a_min=None,
            a_max=(h, w),
        )

    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        img = img.clone()

        img[0, :, self.ymin : self.ymax, self.xmin : self.xmax] = 0
        return img

    def _convert_mask(self, mask):
        return self.convert_img(mask)

    def _convert_bbox(self, bbox):
        cutout_bbox = [self.ymin, self.xmin, self.ymax, self.xmax]
        inter = bbox_ops.intersection(bbox, cutout_bbox)

        # If the bounding box does not overlap the cutout box, then just
        # return the bounding box.
        if inter == 0:
            return bbox

        area_bbox = bbox_ops.area(bbox)
        if inter == area_bbox:
            return None

        area_cutout = bbox_ops.area(cutout_bbox)
        if inter == area_cutout:
            return bbox

        if self.ymin <= bbox[0] and self.ymax >= bbox[2]:
            if self.xmin <= bbox[1]:
                return [bbox[0], self.xmax, bbox[2], bbox[3]]
            if self.xmax >= bbox[3]:
                return [bbox[0], bbox[1], bbox[2], self.xmin]

        if self.xmin <= bbox[1] and self.xmax >= bbox[3]:
            if self.ymin <= bbox[0]:
                return [self.ymax, bbox[1], bbox[2], bbox[3]]
            if self.ymax >= bbox[2]:
                return [bbox[0], bbox[1], self.ymin, bbox[3]]

        return bbox_ops.clean_bbox(bbox)


class Rotation(RandomTransform):
    __serialization_attributes__ = ["angle"]

    def __init__(self, angle: float, random_direction: bool = False) -> None:
        """
        Parameters
        ----------
        angle
            angle (in degrees) to rotate images by
        random_direction
            if True then will multiply angle by -1 with probability .5
        """
        self.angle = angle
        self.random_direction = random_direction

    def set_random_params(self, img):
        self._angle = self.angle
        if self.random_direction and random.random() < 0.5:
            self._angle = -self._angle

    def _convert_mask(self, mask):
        return self.convert_img(img=mask)

    def _convert_img_tensor(self, img):
        self._width = img.shape[-1]
        self._height = img.shape[-2]
        self._center = np.array([self._width / 2, self._height / 2])
        return F.rotate(img, self._angle)

    def _convert_bbox(self, bbox):
        ret = bbox_ops.rotate_bounding_box(self._angle, self._center, bbox)

        return bbox_ops.clean_bbox(ret, self._height, self._width, bbox)


class RandomVerticalFlip(RandomTransform):
    __serialization_attributes__ = ["p"]

    def __init__(self, p: float = 0.5):
        """
        Parameters
        ---------
        p : float
            probability of the image being flipped.
        self.p = p
        """
        self.p = p

    def set_random_params(self, img):
        self.flip = random.random() < self.p

    def _convert_mask(self, mask):
        return F.vflip(mask) if self.flip else mask

    def _convert_img_tensor(self, img):
        self.height = img.shape[2]
        return F.vflip(img) if self.flip else img

    def _convert_bbox(self, bbox):
        if self.flip:
            return [
                self.height - bbox[2],
                bbox[1],
                self.height - bbox[0],
                bbox[3],
            ]
        return bbox

    def __repr__(self):
        return self.__class__.__name__ + "(p={})".format(self.p)


class RandomHorizontalFlip(RandomTransform):
    """Horizontally flip the given PIL Images randomly with a given probability."""

    __serialization_attributes__ = ["p"]

    def __init__(self, p: float = 0.5):
        """
        Parameters
        ----------
        p : float
            probability of the image being flipped.
        """
        self.p = p

    def set_random_params(self, img):
        self.flip = random.random() < self.p

    def _convert_mask(self, mask):
        return F.hflip(mask) if self.flip else mask

    def _convert_img_tensor(self, img):
        # save the width since its needed for converting the bounding box
        self.width = img.shape[3]
        return F.hflip(img) if self.flip else img

    def _convert_bbox(self, bbox):
        if self.flip:
            return [
                bbox[0],
                self.width - bbox[3],
                bbox[2],
                self.width - bbox[1],
            ]
        return bbox

    def __repr__(self):
        return self.__class__.__name__ + "(p={})".format(self.p)


class RandomCrop(RandomTransform):
    """Crop the given PIL Images at a random location."""

    __serialization_attributes__ = ["size", "p"]

    def __init__(self, size, p: float = 1.0):
        """
        Parameters
        ----------
        size : sequence or int
            Desired output size of the crop. If size is an int instead of sequence
            like (h, w), a square crop (size, size) is made.
        p : float
          The probability of performing this operation at all
        """
        if isinstance(size, numbers.Number):
            self.size = (int(size), int(size))
        else:
            self.size = size
        self.p = p

    def set_random_params(self, img):
        h, w = img.shape[2:]
        self.th, self.tw = self.size

        # use relative sizes
        if isinstance(self.th, float):
            self.th = int(self.th * h)
        if isinstance(self.tw, float):
            self.tw = int(self.tw * w)

        if w == self.tw and h == self.th:
            self.i, self.j, self.th, self.tw = 0, 0, h, w
        if h - self.th >= 0 and w - self.tw >= 0:
            self.i = random.randint(0, h - self.th)
            self.j = random.randint(0, w - self.tw)
        else:
            self.tw = w
            self.th = h
            self.i = random.randint(0, h - self.th)
            self.j = random.randint(0, w - self.tw)

        self.do_transform = random.random() < self.p

    def _convert_img_tensor(self, img):
        if self.do_transform:
            return F.crop(img, self.i, self.j, self.th, self.tw)
        else:
            return img

    def _convert_mask(self, mask):
        if self.do_transform:
            return self.convert_img(img=mask)
        else:
            return mask

    def _convert_bbox(self, bbox):
        if self.do_transform:
            return bbox_ops.clean_bbox(
                [
                    bbox[0] - self.i,
                    bbox[1] - self.j,
                    bbox[2] - self.i,
                    bbox[3] - self.j,
                ],
                self.th,
                self.tw,
                bbox,
            )
        else:
            return bbox

    def __repr__(self):
        return self.__class__.__name__ + "(size={0})".format(self.size)


class RandomResize(RandomTransform):
    """Randomly rescale images jointly."""

    __serialization_attributes__ = [
        "scale_range_low",
        "scale_range_high",
        "p",
        "interpolation",
    ]

    def __init__(
        self,
        scale_range_low: float = 1,
        scale_range_high: float = 7,
        p: float = 0.5,
        interpolation: F.InterpolationMode = F.InterpolationMode.BILINEAR,
    ):
        """
        Parameters
        ----------
        scale_range_low : float
          The image will be resized to at a minimum of
          scale_range_low * L X scale_range_low * H
        scale_range_high : float
          The image will be resized to a maximum of
          scale_range_high * L X scale_range_high * H
        interpolation : PIL interpolation
          The kind of interpolation kernel to use.
        p : float
          The probability of doing a random resize.
        """
        self.scale_range_low = scale_range_low
        self.scale_range_high = scale_range_high
        self.interpolation = interpolation
        self.p = p

    def set_random_params(self, img):
        unif = random.uniform(0.0, 1.0)
        if unif < self.p:
            self.resize = random.uniform(
                self.scale_range_low, self.scale_range_high
            )
            self.size = (
                int(self.resize * img.shape[2]),
                int(self.resize * img.shape[3]),
            )
        else:
            self.resize = None
            self.size = None

    def _convert_img_tensor(self, img):
        if self.size:
            return F.resize(img, self.size, self.interpolation, antialias=True)
        return img

    def _convert_mask(self, mask):
        return self.convert_img(mask)

    def _convert_bbox(self, bbox):
        if self.size:
            return self.resize * np.array(bbox)
        return bbox

    def __repr__(self):
        return (
            self.__class__.__name__
            + "(low={0}, high={1}, interpolation={2}, p={3})".format(
                self.scale_range_low,
                self.scale_range_high,
                self.interpolation,
                self.p,
            )
        )


class RandomRotation(RandomTransform):
    """Rotate the images by a random angle."""

    __serialization_attributes__ = ["degrees"]

    def __init__(self, degrees: Union[float, List[float]]):
        """
        Parameters
        ----------
        degrees : sequence or float or int
            Range of degrees to select from. If degrees is a number instead of
            sequence like (min, max), the range of degrees will be (-degrees, +degrees).
        """
        if isinstance(degrees, numbers.Number):
            if degrees < 0:
                raise ValueError(
                    "If degrees is a single number, it must be positive."
                )
            self.degrees = (-degrees, degrees)
        else:
            if len(degrees) != 2:
                raise ValueError(
                    "If degrees is a sequence, it must be of len 2."
                )
            self.degrees = degrees

    def set_random_params(self, img):
        self.angle = np.random.uniform(
            low=self.degrees[0], high=self.degrees[1]
        )

    def _convert_mask(self, mask):
        return self.convert_img(img=mask)

    def _convert_img_tensor(self, img):
        self._width = img.shape[3]
        self._height = img.shape[2]
        self._center = np.array([self._width / 2, self._height / 2])
        return F.rotate(img, self.angle)

    def _convert_bbox(self, bbox):
        ret = bbox_ops.rotate_bounding_box(self.angle, self._center, bbox)

        return bbox_ops.clean_bbox(ret, self._height, self._width, bbox)

    def __repr__(self):
        format_string = self.__class__.__name__ + "(degrees={0}".format(
            self.degrees
        )
        format_string += ")"
        return format_string


class RandomPerspective(RandomTransform):
    """Performs Perspective transformation of the given PIL Images randomly
    with a given probability.
    """

    __serialization_attributes__ = ["distortion_scale", "p", "interpolation"]

    def __init__(
        self,
        distortion_scale: float = 0.5,
        p: float = 0.5,
        interpolation: F.InterpolationMode = F.InterpolationMode.BILINEAR,
    ):
        """
        Parameters
        ----------
        distortion_scale : float
            controls the degree of distortion and ranges from 0 to 1. Default value is 0.5.
        p : float
            probability of the image being perspectively transformed. Default value is 0.5
        interpolation : F.InterpolationMode
            interpolation method
        """
        self.p = p
        self.interpolation = interpolation
        self.distortion_scale = distortion_scale

    def set_random_params(self, img):
        self.apply_trans = True
        if random.random() >= self.p:
            self.apply_trans = False
        height, width = img.shape[2:]
        half_height = int(height / 2)
        half_width = int(width / 2)
        topleft = (
            random.randint(0, int(self.distortion_scale * half_width)),
            random.randint(0, int(self.distortion_scale * half_height)),
        )
        topright = (
            random.randint(
                width - int(self.distortion_scale * half_width) - 1, width - 1
            ),
            random.randint(0, int(self.distortion_scale * half_height)),
        )
        botright = (
            random.randint(
                width - int(self.distortion_scale * half_width) - 1, width - 1
            ),
            random.randint(
                height - int(self.distortion_scale * half_height) - 1,
                height - 1,
            ),
        )
        botleft = (
            random.randint(0, int(self.distortion_scale * half_width)),
            random.randint(
                height - int(self.distortion_scale * half_height) - 1,
                height - 1,
            ),
        )
        self.startpoints = [
            (0, 0),
            (width - 1, 0),
            (width - 1, height - 1),
            (0, height - 1),
        ]
        self.endpoints = [topleft, topright, botright, botleft]

    def _convert_img_tensor(self, img):
        if self.apply_trans:
            return F.perspective(
                img, self.startpoints, self.endpoints, self.interpolation
            )
        return img

    def _convert_mask(self, mask):
        if self.apply_trans:
            return apply_along_classes(
                mask,
                lambda x: F.perspective(
                    x, self.startpoints, self.endpoints, self.interpolation
                ),
            )
        return mask

    def _convert_bbox(self, bbox):
        # endpoints and startpoints arguments swapped since we need to get
        # the inverse of the transform
        a, b, c, d, e, f, g, h = self._get_perspective_coeffs(
            self.endpoints, self.startpoints
        )

        # transformation of a point (y, x)
        def trans(pt):
            # pt = [pt[1], pt[0]]
            s = g * pt[1] + h * pt[0] + 1
            return [
                (d * pt[1] + e * pt[0] + f) / s,
                (a * pt[1] + b * pt[0] + c) / s,
            ]

        # 4 corners
        points = [bbox[:2], bbox[2:], [bbox[0], bbox[3]], [bbox[2], bbox[1]]]
        new_points = np.array([trans(pt) for pt in points])
        minpts = new_points.min(0)
        maxpts = new_points.max(0)

        return np.array([minpts[0], minpts[1], maxpts[0], maxpts[1]])

    def __repr__(self):
        return self.__class__.__name__ + "(p={})".format(self.p)

    @staticmethod
    def _get_perspective_coeffs(startpoints, endpoints):
        """taken from torchvision.transforms.functional
        Helper function to get the coefficients (a, b, c, d, e, f, g, h) for the perspective transforms.

        In Perspective Transform each pixel (x, y) in the orignal image gets transformed as,
         (x, y) -> ( (ax + by + c) / (gx + hy + 1), (dx + ey + f) / (gx + hy + 1) )

        Parameters
        ----------
        startpoints : list
            List containing [top-left, top-right, bottom-right, bottom-left] of the orignal image,
        endpoints : list
            List containing [top-left, top-right, bottom-right, bottom-left] of the transformed
                       image
        Returns
        -------
            octuple (a, b, c, d, e, f, g, h) for transforming each pixel.
        """
        matrix = []

        for p1, p2 in zip(endpoints, startpoints):
            matrix.append(
                [p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]]
            )
            matrix.append(
                [0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]]
            )

        A = torch.tensor(matrix, dtype=torch.float)
        B = torch.tensor(startpoints, dtype=torch.float).view(8)
        # torch.lstq() is deprecated in 1.13.1
        # torch.lstq() solves minX|bx-a|
        # torch.linalg.lstsq() solves minX|ax-b|
        res = torch.linalg.lstsq(A, B)[0]
        return res.tolist()


class TranslateX(RandomTransform):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float) -> None:
        """Translates an image horizontally (with the translation being to
        the left or right chosen randomly)

        Parameters
        ----------
        magnitude
            number between [0, 1] giving the maximum proportion of the image width to translate
        """
        if magnitude < 0 or magnitude > 1:
            raise ValueError("Translation proportions must be in [0, 1].")

        self.magnitude = magnitude

    def set_random_params(self, img):
        self._magnitude = np.random.uniform(
            low=-1 * self.magnitude, high=self.magnitude
        )

    def _convert_img_tensor(self, img):
        self._width = img.shape[3]
        self._translation = self._magnitude * self._width

        return F.affine(
            img, angle=0, translate=(self._translation, 0), scale=1, shear=0
        )

    def _convert_bbox(self, bbox):
        return bbox_ops.clean_bbox(
            [
                bbox[0],
                bbox[1] + self._translation,
                bbox[2],
                bbox[3] + self._translation,
            ],
            np.infty,
            self._width,
            bbox,
        )

    def _convert_mask(self, mask):
        return self.convert_img(mask)


class TranslateY(RandomTransform):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float) -> None:
        """Translates an image vertically (with the translation being to
        up or down chosen randomly)

        Parameters
        ----------
        magnitude
            number between [0, 1] giving the maximum proportion of the image height to translate
        """
        if magnitude < 0 or magnitude > 1:
            raise ValueError("Translation proportions must be in [0, 1].")

        self.magnitude = magnitude

    def set_random_params(self, img):
        self._magnitude = np.random.uniform(
            low=-1 * self.magnitude, high=self.magnitude
        )

    def _convert_img_tensor(self, img):
        self._height = img.shape[2]
        self._translation = self._magnitude * self._height

        return F.affine(
            img, angle=0, translate=(0, self._translation), scale=1, shear=0
        )

    def _convert_bbox(self, bbox):
        return bbox_ops.clean_bbox(
            [
                bbox[0] + self._translation,
                bbox[1],
                bbox[2] + self._translation,
                bbox[3],
            ],
            self._height,
            np.infty,
            bbox,
        )

    def _convert_mask(self, mask):
        return self.convert_img(mask)


class RandomAffine(RandomTransform):
    """Random affine transformation of the images keeping center invariant"""

    __serialization_attributes__ = [
        "degrees",
        "translate",
        "scale",
        "shear",
        "interpolation",
        "fill",
    ]

    def __init__(
        self,
        degrees: Union[float, List[float], Tuple[float, float]],
        translate: List[float] = None,
        scale: Tuple[float, float] = None,
        shear: Union[float, List[float]] = None,
        interpolation: F.InterpolationMode = F.InterpolationMode.NEAREST,
        fill: Union[int, tuple] = 0,
    ):
        """
        Parameters
        ----------
        degrees : sequence or float or int)
            Range of degrees to select from. If degrees is a number instead of
            sequence like (min, max), the range of degrees will be (-degrees, +degrees).
            Set to 0 to deactivate rotations.
        translate : tuple
            tuple of maximum absolute fraction for horizontal
            and vertical translations. For example translate=(a, b), then horizontal shift
            is randomly sampled in the range -img_width * a < dx < img_width * a and vertical shift is
            randomly sampled in the range -img_height * b < dy < img_height * b. Will not translate by default.
        scale : tuple
            scaling factor interval, e.g (a, b), then scale is
            randomly sampled from the range a <= scale <= b. Will keep original scale by default.
        shear : sequence or float or int
            Range of degrees to select from.
            If shear is a number, a shear parallel to the x axis in the range (-shear, +shear)
            will be apllied. Else if shear is a tuple or list of 2 values a shear parallel to the x axis in the
            range (shear[0], shear[1]) will be applied. Else if shear is a tuple or list of 4 values,
            a x-axis shear in (shear[0], shear[1]) and y-axis shear in (shear[2], shear[3]) will be applied.
            Will not apply shear by default
        interpolation (F.InterpolationMode): Desired interpolation enum defined by
            :class:`torchvision.transforms.F.InterpolationMode`. Default is ``F.InterpolationMode.NEAREST``.
            If input is Tensor, only ``F.InterpolationMode.NEAREST``, ``F.InterpolationMode.BILINEAR`` are supported.
            For backward compatibility integer values (e.g. ``PIL.Image[.Resampling].NEAREST``) are still accepted,
            but deprecated since Teddy 0.64.3 and will be removed soon! Please use F.InterpolationMode enum.
        fill (sequence or number): Pixel fill value for the area outside the transformed
            image. Default is ``0``. If given a number, the value is used for all bands respectively.
        """
        if isinstance(degrees, numbers.Number):
            if degrees < 0:
                raise ValueError(
                    "If degrees is a single number, it must be positive."
                )
            self.degrees = (-degrees, degrees)
        else:
            assert (
                isinstance(degrees, (tuple, list)) and len(degrees) == 2
            ), "degrees should be a list or tuple and it must be of length 2."
            self.degrees = degrees

        if translate is not None:
            assert (
                isinstance(translate, (tuple, list)) and len(translate) == 2
            ), "translate should be a list or tuple and it must be of length 2."
            for t in translate:
                if not (0.0 <= t <= 1.0):
                    raise ValueError(
                        "translation values should be between 0 and 1"
                    )
        self.translate = translate

        self.scale = scale
        if scale is not None:
            assert (
                isinstance(scale, (tuple, list)) and len(scale) == 2
            ), "scale should be a list or tuple and it must be of length 2."
            for s in scale:
                if s <= 0:
                    raise ValueError("scale values should be positive")
        self.scale_ranges = scale

        self.shear = shear
        if shear is not None:
            if isinstance(shear, numbers.Number):
                if shear < 0:
                    raise ValueError(
                        "If shear is a single number, it must be positive."
                    )
                self.shears = (-shear, shear)
            else:
                assert isinstance(shear, (tuple, list)) and (
                    len(shear) == 2 or len(shear) == 4
                ), "shear should be a list or tuple and it must be of length 2 or 4."
                # X-Axis shear with [min, max]
                if len(shear) == 2:
                    self.shears = [shear[0], shear[1], 0.0, 0.0]
                elif len(shear) == 4:
                    self.shears = [s for s in shear]
        else:
            self.shears = shear

        self.resample = False
        self.interpolation = interpolation
        self.fill = fill

    def set_random_params(self, img):
        height, width = img.shape[2:]
        angle = random.uniform(self.degrees[0], self.degrees[1])
        if self.translate is not None:
            max_dx = self.translate[0] * width
            max_dy = self.translate[1] * height
            translations = (
                np.round(random.uniform(-max_dx, max_dx)),
                np.round(random.uniform(-max_dy, max_dy)),
            )
        else:
            translations = (0, 0)

        if self.scale_ranges is not None:
            scale = random.uniform(self.scale_ranges[0], self.scale_ranges[1])
        else:
            scale = 1.0

        if self.shears is not None:
            if len(self.shears) == 2:
                shear = [random.uniform(self.shears[0], self.shears[1]), 0.0]
            elif len(self.shears) == 4:
                shear = [
                    random.uniform(self.shears[0], self.shears[1]),
                    random.uniform(self.shears[2], self.shears[3]),
                ]
        else:
            shear = 0.0

        self.angle = angle
        self.translations = translations
        self.scale = scale
        self.shear = shear

        center = (width * 0.5 + 0.5, height * 0.5 + 0.5)

        self.matrix = get_affine_matrix(
            center, angle, translations, scale, shear
        )

    def _convert_img_tensor(self, img):
        self._width = img.shape[3]
        self._height = img.shape[2]
        return F.affine(
            img,
            angle=self.angle,
            translate=self.translations,
            scale=self.scale,
            shear=self.shear,
            interpolation=(
                self.interpolation
                if not self.resample
                else F._interpolation_modes_from_int(self.resample)
            ),
            fill=self.fill,
        )

    def _convert_bbox(self, bbox):
        ret = bbox_ops.apply_affine_matrix_to_bbox(self.matrix, bbox)

        return bbox_ops.clean_bbox(ret, self._height, self._width, bbox)

    def _convert_mask(self, mask):
        return self.convert_img(mask)

    def __repr__(self):
        s = "{name}(degrees={degrees}"
        if self.translate is not None:
            s += ", translate={translate}"
        if self.scale_ranges is not None:
            s += ", scale={scale_ranges}"
        if self.shears is not None:
            s += ", shear={shears}"
        if self.interpolation:
            s += ", interpolation={interpolation}"
        if self.resample > 0:
            s += ", resample={resample}"
        if self.fillcolor:
            s += ", fillcolor={fillcolor}"
        if self.fill != 0:
            s += ", fill={fill}"
        s += ")"
        d = dict(self.__dict__)
        d["resample"] = str(d["resample"])
        d["interpolation"] = str(d["interpolation"])
        return s.format(name=self.__class__.__name__, **d)


class ColorJitter(ImageOnlyTransform):
    __serialization_attributes__ = [
        "brightness",
        "contrast",
        "saturation",
        "hue",
    ]

    def __init__(
        self,
        brightness: Union[float, Tuple[float, float]] = 0,
        contrast: Union[float, Tuple[float, float]] = 0,
        saturation: Union[float, Tuple[float, float]] = 0,
        hue: Union[float, Tuple[float, float]] = 0,
    ):
        self.brightness = brightness
        self.contrast = contrast
        self.saturation = saturation
        self.hue = hue
        self.transform = _ColorJitter(
            brightness=brightness,
            contrast=contrast,
            saturation=saturation,
            hue=hue,
        )

    def _convert_img_tensor(self, img):
        return self.transform(img)


class Grayscale(ImageOnlyTransform):
    __serialization_attributes__ = ["num_output_channels"]

    def __init__(self, num_output_channels: int = 1):
        self.num_output_channels = num_output_channels
        self.transform = _Grayscale(num_output_channels=num_output_channels)

    def _convert_img_tensor(self, img):
        return self.transform(img)


class ComposeRandomTransforms(RandomTransform, Compose):
    """Composes several transforms together."""

    def set_random_params(self, img):
        for t in self.transforms:
            if isinstance(t, RandomTransform):
                t.set_random_params(img)


class CenterCrop(TransformBase):
    """Crops the given PIL Images at the center."""

    __serialization_attributes__ = ["size"]

    def __init__(self, size: Union[int, List[int]]):
        """
        Parameters
        ----------
        size : sequence or int
            Desired output size of the crop. If size is an int instead of sequence
            like (h, w), a square crop (size, size) is made.
        """
        if isinstance(size, numbers.Number):
            self.size = (int(size), int(size))
        else:
            self.size = size

    def _convert_mask(self, mask):
        return self.convert_img(mask)

    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        # set the center_pt for the call to _convert_bbox
        h, w = img.shape[2:]
        self.center_pt = np.array([h / 2, w / 2])
        return F.center_crop(img, self.size)

    def _convert_bbox(self, bbox):
        pt1 = bbox[:2] - (self.center_pt - np.array(self.size) / 2)

        pt2 = bbox[2:] - (self.center_pt - np.array(self.size) / 2)

        ret = np.concatenate([pt1, pt2])
        return bbox_ops.clean_bbox(ret, self.size[0], self.size[1], bbox)

    def __repr__(self):
        return self.__class__.__name__ + "(size={0})".format(self.size)


class RandomGrayscale(RandomTransform):
    __serialization_attributes__ = ["p"]

    def __init__(self, p: float = 0.5):
        """
        Parameters
        ----------
        p : float
            The probability of converting to Grayscale
        """

        self.p = p

    def set_random_params(self, img):
        self.transform = IdentityTransform()
        if random.random() < self.p:
            self.transform = Grayscale(num_output_channels=3)

    def _convert_img_tensor(self, img):
        return self.transform(img)

    def _convert_mask(self, mask):
        return mask

    def _convert_bbox(self, bbox):
        return bbox

    def __repr__(self):
        return self.__class__.__name__ + "(p={})".format(self.p)


class _Shear(RandomTransform):
    def __init__(
        self, shear: Tuple[float, float], random_direction: bool = False
    ) -> None:
        """
        Parameters
        ----------
        shear : Tuple[float, float]
            Represents the maximum amount of shear to the image.
            The angle is non-zero in the first component for horizontal shear.
            The angle is non-zero in the second component for vertical shear.

            Note: Angles are randomly chosen up to the shear amount.
            If random_direction is True, then the angle is up to +- shear.

        random_direction : bool = False
            A boolean flag to indicate that randomly chosen shear amounts should
            be positive or negative.
        """
        self.shear = shear
        self.random_direction = random_direction

    def set_random_params(self, img):
        if self.random_direction:
            self._shear = (
                np.random.uniform(low=-1 * self.shear[0], high=self.shear[0]),
                np.random.uniform(low=-1 * self.shear[1], high=self.shear[1]),
            )
        else:
            self._shear = (
                np.random.uniform(low=0, high=self.shear[0]),
                np.random.uniform(low=0, high=self.shear[1]),
            )

    def _convert_bbox(self, bbox):
        ret = bbox_ops.apply_affine_matrix_to_bbox(self._matrix, bbox)
        return bbox_ops.clean_bbox(ret, self._height, self._width, bbox)

    def _convert_mask(self, mask):
        return self.convert_img(mask)

    def _convert_img_tensor(self, img):
        self._height, self._width = img.shape[2:]
        center = (self._width * 0.5 + 0.5, self._height * 0.5 + 0.5)
        self._matrix = get_affine_matrix(center, 0, (0, 0), 1.0, self._shear)
        return F.affine(
            img, angle=0, translate=(0, 0), scale=1, shear=self._shear
        )


class HorizontalShear(_Shear):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float):
        self.magnitude = magnitude
        super().__init__(
            (math.degrees(math.atan(magnitude)), 0), random_direction=True
        )


class VerticalShear(_Shear):
    __serialization_attributes__ = ["magnitude"]

    def __init__(self, magnitude: float):
        self.magnitude = magnitude
        super().__init__(
            (0, math.degrees(math.atan(magnitude))), random_direction=True
        )


class Pad(TransformBase):
    """Wrapper for torchvision.transformations.Pad"""

    __serialization_attributes__ = ["padding", "fill", "padding_mode"]

    def __init__(
        self,
        padding: Union[
            int, List[int], Tuple[int, int], Tuple[int, int, int, int]
        ],
        fill: Union[int, Tuple[int, int, int]] = 0,
        padding_mode: str = "constant",
    ) -> None:
        """
        Parameters
        ----------
        padding
            Padding on each border. If a single int is provided this is used to pad all borders.
            If tuple of length 2 is provided this is the padding on left/right and top/bottom
            respectively. If a tuple of length 4 is provided this is the padding for the
            left, top, right and bottom borders respectively.
        fill
            Pixel fill value for constant fill. Default is 0. If a tuple of length 3, it is used
            to fill R, G, B channels respectively. This value is only used when the padding_mode
            is constant
        padding_mode
            Type of padding. Should be: constant, edge, reflect or symmetric.
            Default is constant. Mode symmetric is not yet supported for Tensor inputs.

            - constant: pads with a constant value, this value is specified with fill

            - edge: pads with the last value at the edge of the image

            - reflect: pads with reflection of image without repeating the last value on the edge

                For example, padding [1, 2, 3, 4] with 2 elements on both sides in reflect mode
                will result in [3, 2, 1, 2, 3, 4, 3, 2]

            - symmetric: pads with reflection of image repeating the last value on the edge

                For example, padding [1, 2, 3, 4] with 2 elements on both sides in symmetric mode
                will result in [2, 1, 1, 2, 3, 4, 4, 3]
        """
        self.padding = padding
        self.fill = fill
        self.padding_mode = padding_mode

    def _convert_mask(self, mask):
        return self.convert_img(img=mask)

    def _convert_img_tensor(self, img):
        return F.pad(
            img,
            padding=self.padding,
            fill=self.fill,
            padding_mode=self.padding_mode,
        )

    def _convert_bbox(self, bbox):
        if self.padding_mode not in ["constant", "edge"]:
            raise RuntimeError(
                "Bounding box conversion for Pad transform is only supported when the "
                "padding mode is 'constant' or 'edge'."
            )

        if isinstance(self.padding, int):
            horizontal_shift = self.padding
            vertical_shift = self.padding
        else:  # case of tuple of length 2 or 4
            horizontal_shift, vertical_shift = self.padding[:2]

        return [
            bbox[0] + vertical_shift,
            bbox[1] + horizontal_shift,
            bbox[2] + vertical_shift,
            bbox[3] + horizontal_shift,
        ]


class RandAugment(RandomTransform):
    """Implementation of RandAugment (https://arxiv.org/abs/1909.13719)

    Attributes
    ----------
    augmentations : list[tuple]
        list of tuples of the form `(cls, (m_min, m_max))` where cls is the
        class of an augmentation, and m_min and m_max are lower and upper bounds,
        respectively, on the magnitude of the transformation. note that some
        transforms have no magnitude (e.g. AutoContrast, IdentityTransform)
        but bounds are included for uniformity.
    """

    # list of tuples of the form
    # (augmentation name, augmentation, (lower bound on magnitude, upper bound on magnitude)).
    augmentations = [
        ("AutoContrast", lambda x: AutoContrast(), (0.0, 1.0)),
        ("Brightness", RandomBrightness, (0.1, 0.9)),
        # ("Color", RandomColor, (0.1, 0.9)),
        ("Contrast", RandomContrast, (0.1, 0.9)),
        ("Equalize", lambda x: Equalize(), (0.0, 1.0)),
        ("HorizontalShear", HorizontalShear, (0, 0.3)),
        ("Identity", lambda x: IdentityTransform(), (0.0, 1.0)),
        ("Invert", lambda x: Invert(), (0.0, 1.0)),
        ("Posterize", RandomPosterize, (8, 4)),
        ("Rotation", RandomRotation, (0.0, 30.0)),
        ("Sharpness", RandomSharpness, (0.1, 0.9)),
        ("Solarize", RandomSolarize, (1.0, 0.0)),
        ("TranslateX", TranslateX, (0.0, 1.0)),
        ("TranslateY", TranslateY, (0.0, 1.0)),
        ("VerticalShear", VerticalShear, (0.0, 0.3)),
    ]

    def __init__(
        self,
        n: int,
        m: Optional[int] = None,
        augs_to_use: Optional[List[str]] = None,
        augs_to_remove: Optional[List[str]] = None,
    ) -> None:
        """
        Parameters
        ----------
        n
            number of transforms to randomly draw
        m
            magnitude of the transforms. This should be between 0 and 10 if
            specified. If this is None then this is chosen randomly every
            time (this is used e.g. in FixMatch)
        augs_to_use
            list of augmentation names to use. If None then use all except for
            those in augs_to_remove
        augs_to_remove
            optional list of augmentations to not use.
        """
        self.n = n
        self.m = m
        self.augs_to_use = augs_to_use
        self.augs_to_remove = augs_to_remove

        if augs_to_use is not None:
            self.augmentations = [
                a for a in self.augmentations if a[0] in augs_to_use
            ]

        if augs_to_remove is not None:
            self.augmentations = [
                a for a in self.augmentations if a[0] not in augs_to_remove
            ]

        if m is not None:
            if m > 10 or m < 0:
                raise ValueError("m must be between 0 and 10 (inclusive)")
            self.transforms = [
                t(b[0] + self.m / 10 * (b[1] - b[0]))
                for (_, t, b) in self.augmentations
            ]

    def set_random_params(self, img):
        """Sets self.transform to the random transform"""
        if self.m is not None:
            transforms = random.choices(self.transforms, k=self.n)
        else:
            transforms = [
                t(random.uniform(b[0], b[1]))
                for (_, t, b) in random.choices(self.augmentations, k=self.n)
            ]

        for t in transforms:
            if isinstance(t, RandomTransform):
                t.set_random_params(img)

        self._transform = ComposeRandomTransforms(transforms)

    def _convert_img_tensor(self, *args, **kwargs):
        return self._transform._convert_img_tensor(*args, **kwargs)

    def _convert_bbox(self, bbox):
        return self._transform._convert_bbox(bbox)

    def _convert_mask(self, mask):
        return self._transform._convert_mask(mask)
