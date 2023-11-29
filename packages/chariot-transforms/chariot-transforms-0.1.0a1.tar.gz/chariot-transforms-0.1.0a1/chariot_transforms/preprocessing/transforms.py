from collections.abc import Iterable
from typing import List, Tuple, Union

import numpy as np
import torch
import torchvision.transforms.functional as F
from PIL import Image, ImageOps
from torch.nn.functional import pad
from torchvision.transforms.functional import InterpolationMode

from chariot_transforms.base import Compose, ImageOnlyTransform, TransformBase
from chariot_transforms.preprocessing.clahe import equalize_adapthist
from chariot_transforms.preprocessing.histogram_tools import linear_stretch


class HistogramLinearStretch(ImageOnlyTransform):
    def __init__(self, percentage: float) -> None:
        self.percentage = percentage

    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        return torch.stack(
            [
                torch.tensor(linear_stretch(img[i].numpy(), self.percentage))
                for i in range(img.shape[0])
            ]
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, HistogramLinearStretch)
            and self.percentage == other.percentage
        )


class CLAHE(ImageOnlyTransform):
    def __init__(self, nbins: int = 256) -> None:
        self.nbins = nbins

    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        return torch.stack(
            [
                torch.tensor(
                    equalize_adapthist(
                        img[i].permute(1, 2, 0).numpy(), nbins=self.nbins
                    )  # need to put channels last because of `is_rgb_like` check in equalize_adapthisteq
                ).permute(2, 0, 1)
                for i in range(img.shape[0])
            ]
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CLAHE) and self.nbins == other.nbins


def get_height_width(img: Union[torch.Tensor, Image.Image]) -> Tuple[int, int]:
    if isinstance(img, torch.Tensor):
        if not len(img.shape) == 4:
            raise ValueError("img must be a rank 4 tensor")
        return tuple(img.shape[2:4])

    return (img.height, img.width)


class PreprocessingTransform(TransformBase):
    """These are the transforms which can be used as pre-processing transforms attribute of a model. It provides a common API
    for transforms which are used for reducing images to the size of a given NN and then transforming outputs (such as bounding boxes)
    back into the original image space.
    """

    @staticmethod
    def _validate_input(img):
        """here we allow PIL images as well as tensors for backwards compatibility"""
        if isinstance(img, Image.Image):
            return
        return TransformBase._validate_input(img)

    # convert_bbox and convert_coords can be public for pre-processing transforms since
    # they are used in model definitions to convert output but its best to keep them private for
    # augmentations
    def convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        return self._convert_bbox(bbox, img_h, img_w, invert)

    def convert_coords(self, coords, img_h, img_w, invert=False):
        return self._convert_coords(coords, img_h, img_w, invert)


class TrivialPreprocessingTransform(PreprocessingTransform):
    """Base class for transforms that act trivially on annotations."""

    def _convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        return bbox

    def _convert_mask(self, mask):
        return mask


class IdentityPreprocessingTransform(
    TrivialPreprocessingTransform, PreprocessingTransform
):
    """Transform used for models that do not need any image pre-processing.
    For all class methods the output is the input.
    """

    def _convert_img_tensor(self, img: torch.Tensor) -> torch.Tensor:
        return img

    def _convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        return bbox

    def _convert_coords(self, coords, img_h, img_w, invert=False):
        return coords

    def set_magnitude(self, magnitude: float) -> None:
        return

    def __eq__(self, other):
        return isinstance(other, IdentityPreprocessingTransform)

    def invert_torch_output(self, x, img_h, img_w):
        # We override base class method for speed since this is just
        # the identity transform.
        return x


class Resize(PreprocessingTransform):
    """Resize the input PIL Images to a given size or specified min/max size.

    This class method is able to resize torch tensors directly (on CPU or GPU)
    via its convert_img_pt method. Note that because of the way PIL and PyTorch
    resize, they may not always agree, i.e. if t is a Resize object then
    ToTensor()(t.convert_img(img)) and t.convert_img_pt(ToTensor()(img))
    will likely be different.
    """

    def __init__(
        self,
        size: Union[List[int], int] = None,
        min_size: int = None,
        max_size: int = None,
        interpolation: InterpolationMode = InterpolationMode.BILINEAR,
    ) -> None:
        """
        Parameters
        ----------
        size : sequence or int
            Desired output size. If size is a sequence like
            (h, w), output size will be matched to this. If size is an int,
            smaller edge of the image will be matched to this number.
            i.e, if height > width, then image will be rescaled to
            (size * height / width, size)
        min_size : int
            Desired minimum size of single dimension (height or width) of an image.
        max_size : int
            Desired maximum size of single dimension (height or width) of an image.
        interpolation : int
            Desired interpolation. Default is ``InterpolationMode.BILINEAR``


        Note: Exactly one of size or (min_size and max_size) must be set.
        If size is set, every image will be resized to match the specified size.
        If (instead) min_size and max_size are set, each input image will be resized so that
        either the resized_min_size matches the specified min_size or the
        resized_max_size matches the specified max_size, whichever results in the resized image
        having smaller area.  It is not guaranteed that the resized image will satisfy both
        (weak) constraints: i.e. that resized_max_size <= max_size and resized_min_size <= min_size.
        """

        assert bool(min_size) == bool(
            max_size
        ), "If you set one of min_size or max_size, you must set both (and be positive integers)."
        assert bool(size) != bool(
            min_size
        ), "You must set either size or (min_size and max_size)."
        if size is not None:
            assert isinstance(size, int) or (
                isinstance(size, Iterable) and len(size) == 2
            )
        else:
            assert min_size > 0, "min_size must be a positive integer"
            assert max_size >= min_size, "max_size must be at least min_size"

        self.size = size
        self.interpolation = interpolation
        self.min_size = min_size
        self.max_size = max_size

    def get_new_size(self, img_shape: Tuple[int, int]) -> Tuple[int, int]:
        """
        Parameters
        ----------
        img_shape
            tuple of the form (height, width)

        Returns
        -------
        Tuple[int, int]
            the height and width of the resized image
        """
        if self.size is not None:
            if isinstance(self.size, int):
                return (
                    (self.size * img_shape[0] / img_shape[1], self.size)
                    if img_shape[0] > img_shape[1]
                    else (self.size, self.size * img_shape[1] / img_shape[0])
                )
            return self.size
        else:
            # both self.min_size and self.max_size are set...
            # determine current min/max lengths.
            current_min_side_length = min(img_shape)
            current_max_side_length = max(img_shape)

            # compute possible resizing ratios (scales)
            tight_min_ratio = self.min_size / current_min_side_length
            tight_max_ratio = self.max_size / current_max_side_length

            # best ratio is the smaller of the two
            ratio = min(tight_min_ratio, tight_max_ratio)

            return (int(img_shape[0] * ratio), int(img_shape[1] * ratio))

    def _calc_resize(self, img_shape):
        new_size = self.get_new_size(img_shape)
        size = (np.array(new_size, dtype=int)).astype(float)
        return size[0] / img_shape[0], size[1] / img_shape[1]

    def _convert_img_tensor(self, img: Union[torch.Tensor, Image.Image]):
        # set resize for converting bounding boxes
        self.orig_size = get_height_width(img)
        size = (
            self.size
            if self.size is not None
            else self.get_new_size(self.orig_size)
        )
        return F.resize(img, size, self.interpolation, antialias=True)

    def _convert_mask(self, mask, invert=False):
        if invert:
            raise ValueError("inversion not supported")
        return super()._convert_mask(mask)

    def _convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        """Converts a bounding box. If invert is False then transforms the
        bounding box from an img_h x img_w image to the bounding box for the
        resized self.new_h x self.new_w image. If invert is True then it will do the
        conversion in the opposite direction.

        Parameters
        ----------
        bbox : list
            of the form [ymin, xmin, ymax, xmax]
        img_h : int
            if None then will use self.img_h
        img_w : int
            if None then will use self.img_w
        invert : bool
            whether or not to return the inverse operation

        Returns
        -------
        list
            list of integers of the transformed bounding box.
        """

        if not hasattr(self, "orig_size") and not (img_h and img_w):
            raise Exception(
                "Must call convert_img before convert_bbox or pass img_h and img_w"
            )
        orig_size = (img_h, img_w) if (img_h and img_w) else self.orig_size
        resize = self._calc_resize(orig_size)
        exp = -1 if invert else 1
        return [
            resize[0] ** exp,
            resize[1] ** exp,
            resize[0] ** exp,
            resize[1] ** exp,
        ] * np.array(bbox)

    def _convert_coords(self, coords, img_h, img_w, invert=False):
        """Converts coordinates. If invert is False then transforms the
        coordinates from an img_h x img_w image to the coordinates for the
        resized new_h x new_w image. If invert is True then it will do the
        conversion in the opposite direction.

        Parameters
        ----------
        coords : np.ndarray
            of shape N(x...)x2 of the form [[y_0, x_0], [y_1, x_1], ...]
        img_h : int
        img_w : int
        invert : bool
            whether or not to return the inverse operation

        Returns
        -------
        np.ndarray
            array of the transformed coordinates.
        """
        exp = -1 if invert else 1
        resize = np.array(self._calc_resize((img_h, img_w))) ** exp
        new_coords = np.array(coords) * resize
        return new_coords

    def __repr__(self):
        if self.size is not None:
            return (
                self.__class__.__name__
                + "(size={0}, interpolation={1})".format(
                    self.size, self.interpolation
                )
            )
        else:
            return (
                self.__class__.__name__
                + "(min_size={0}, max_size={1}, interpolation={2})".format(
                    self.min_size, self.max_size, self.interpolation
                )
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.size == other.size
            and self.interpolation == other.interpolation
            and self.min_size == other.min_size
            and self.max_size == other.max_size
        )


class ResizePreserveAspect(PreprocessingTransform):
    """Class for resizing an image and bounding boxes to (new_h, new_w)
    by preserving aspect ratio and padding as necessary.

    This class method is able to resize torch tensors directly (on CPU or GPU)
    via its convert_img_pt method. Note that because of the way PIL and PyTorch
    resize, they may not always agree, i.e. if t is a ResizePreserveAspect
    object then ToTensor()(t.convert_img(img)) and
    t.convert_img_pt(ToTensor()(img)) will likely be different.
    """

    def __init__(
        self,
        new_h: int,
        new_w: int,
        fill: Union[int, Tuple[int, int, int]] = 0,
    ):
        """
        Parameters
        ----------
        new_h : int
            height to resize to
        new_w : int
            width to resize to
        fill : int or Tuple[int, int, int]
            the fill color to use for the padding
        """
        self.new_h = new_h
        self.new_w = new_w
        self.fill = fill

    def _convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        """Converts a bounding box. If invert is False then transforms the
        bounding box from an img_h x img_w image to the bounding box for the
        resized self.new_h x self.new_w image. If invert is True then it will do the
        conversion in the opposite direction.

        Parameters
        ----------
        bbox : list
            of the form [ymin, xmin, ymax, xmax]
        img_h : int
            if None then will use self.img_h
        img_w : int
            if None then will use self.img_w
        invert : bool
            whether or not to return the inverse operation

        Returns
        -------
        list
            list of integers of the transformed bounding box.
        """

        img_w = img_w or self.img_w
        img_h = img_h or self.img_h

        new_w = self.new_w
        new_h = self.new_h

        if img_w / img_h <= new_w / new_h:
            # padding was added to increase width
            act_w = int(img_w / img_h * new_h)  # image width without padding
            x_offset = (new_w - act_w) // 2
            x_scale = act_w / img_w

            y_offset = 0
            y_scale = new_h / img_h
        else:
            # padding was added to increase height
            act_h = int(img_h / img_w * new_w)  # image height without padding
            y_offset = (new_h - act_h) // 2
            y_scale = act_h / img_h

            x_offset = 0
            x_scale = new_w / img_w

        if invert:
            return [
                (bbox[0] - y_offset) / y_scale,
                (bbox[1] - x_offset) / x_scale,
                (bbox[2] - y_offset) / y_scale,
                (bbox[3] - x_offset) / x_scale,
            ]
        return [
            y_scale * bbox[0] + y_offset,
            x_scale * bbox[1] + x_offset,
            y_scale * bbox[2] + y_offset,
            x_scale * bbox[3] + x_offset,
        ]

    def _convert_coords(self, coords, img_h, img_w, invert=False):
        """Converts coordinates. If invert is False then transforms the
        coordinates from an img_h x img_w image to the coordinates for the
        resized new_h x new_w image. If invert is True then it will do the
        conversion in the opposite direction.

        Parameters
        ----------
        coords : np.ndarray
            of shape N(x...)x2 of the form [[y_0, x_0], [y_1, x_1], ...]
        img_h : int
        img_w : int
        invert : bool
            whether or not to return the inverse operation

        Returns
        -------
        np.ndarray
            array of the transformed coordinates.
        """

        new_w = self.new_w
        new_h = self.new_h

        if img_w / img_h <= new_w / new_h:
            # padding was added to increase width
            act_w = int(img_w / img_h * new_h)  # image width without padding
            x_offset = (new_w - act_w) // 2
            x_scale = act_w / img_w

            y_offset = 0
            y_scale = new_h / img_h
        else:
            # padding was added to increase height
            act_h = int(img_h / img_w * new_w)  # image height without padding
            y_offset = (new_h - act_h) // 2
            y_scale = act_h / img_h

            x_offset = 0
            x_scale = new_w / img_w

        new_coords = np.zeros(coords.shape, dtype=coords.dtype)
        if invert:
            new_coords[..., 0] = (coords[..., 0] - y_offset) / y_scale
            new_coords[..., 1] = (coords[..., 1] - x_offset) / x_scale
        else:
            new_coords[..., 0] = coords[..., 0] * y_scale + y_offset
            new_coords[..., 1] = coords[..., 1] * x_scale + x_offset

        return new_coords

    def _convert_pil(self, img: Image.Image) -> Image.Image:
        w, h = img.size
        self.img_w, self.img_h = w, h

        if w / h <= self.new_w / self.new_h:
            act_w = int(w / h * self.new_h)
            new_img = img.resize((act_w, self.new_h), Image.BILINEAR)
            border = self.new_w - act_w
            # add border // 2 on the left and border - border // 2 on the right
            new_img = ImageOps.expand(
                new_img, (border // 2, 0, border - border // 2, 0), self.fill
            )
        else:
            act_h = int(h / w * self.new_w)
            new_img = img.resize((self.new_w, act_h), Image.BILINEAR)
            border = self.new_h - act_h
            # add border // 2 on the top and border - border // 2 on the bottom
            new_img = ImageOps.expand(
                new_img, (0, border // 2, 0, border - border // 2), self.fill
            )
        return new_img

    def _convert_img_tensor(self, img: Union[torch.Tensor, Image.Image]):
        if isinstance(img, Image.Image):
            return self._convert_pil(img)

        h, w = get_height_width(img)
        self.img_h, self.img_w = h, w

        if w / h <= self.new_w / self.new_h:
            act_w = int(w / h * self.new_h)
            new_img = F.resize(
                img,
                (self.new_h, act_w),
                interpolation=InterpolationMode.BILINEAR,
                antialias=True,
            )
            border = self.new_w - act_w
            # add border // 2 on the left and border - border // 2 on the right
            new_img = pad(
                new_img, (border // 2, border - border // 2), value=self.fill
            )
        else:
            act_h = int(h / w * self.new_w)
            new_img = F.resize(
                img,
                (act_h, self.new_w),
                interpolation=InterpolationMode.BILINEAR,
                antialias=True,
            )
            border = self.new_h - act_h
            # add border // 2 on the top and border - border // 2 on the bottom
            new_img = pad(
                new_img,
                (0, 0, border // 2, border - border // 2),
                value=self.fill,
            )
        return new_img

    def _convert_mask(self, mask, invert=False):
        if invert:
            raise ValueError("Inversion not supported")
        return super()._convert_mask(mask)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.new_h == other.new_h
            and self.new_w == other.new_w
        )


class PreprocessingCompose(Compose):
    def __init__(self, transforms: List[PreprocessingTransform]):
        super().__init__(transforms)
        self.resize_component = None
        for t in transforms:
            if isinstance(t, RESIZE_TRANSFORMS):
                if self.resize_component is not None:
                    raise ValueError(
                        "PreprocessingCompose cannot contain more than one resize transform"
                    )
                self.resize_component = t


RESIZE_TRANSFORMS = (
    Resize,
    ResizePreserveAspect,
    IdentityPreprocessingTransform,
)
