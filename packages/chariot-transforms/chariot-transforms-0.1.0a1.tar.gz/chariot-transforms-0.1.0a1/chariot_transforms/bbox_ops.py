from typing import Optional, Union

import numpy as np


def area(bbox):
    return (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])


def intersection(bbox1, bbox2):
    lt = np.max([bbox1[:2], bbox2[:2]], axis=0)
    rb = np.min([bbox1[2:], bbox2[2:]], axis=0)

    wh = np.clip(rb - lt, 0, None)
    return wh[0] * wh[1]


def iou(bbox1, bbox2):
    inter = intersection(bbox1, bbox2)
    return inter / (area(bbox1) + area(bbox2) - inter)


# transformed bounding boxes that have a ratio of new area to old area
# less than this threshold will be dropped.
DROP_BBOX_AREA_RATIO_THRES = 0.1


def clean_bbox(
    bbox: list,
    img_height: int = np.infty,
    img_width: int = np.infty,
    og_bbox: Optional[list] = None,
) -> Union[list, None]:
    """Cleans a transformed bounding box by clipping the x-coordinate
    components to be between 0 and img_width and clipping the y-coordinate
    components to be between 0 and img_height. It also checks if the bounding
    box has length or width less than or equal to 1, in which case it will
    return None. If `og_bbox` is passed then None will be returned if the ratio
    of the area of `bbox` to the area of `og_bbox` is less than DROP_BBOX_AREA_RATIO_THRES

    Parameters
    ----------
    bbox
        bounding box, of form [ymin, xmin, ymax, xmax], to clean
    img_height
        height of image the bounding box corresponds to
    img_width
        width of image the bounding box corresponds to
    og_bbox
        (optional) original bounding box that `bbox` was gotten from via a
        transformation

    Returns
    -------
    cleaned bounding box, as a list of length four, or None if the bounding
    box is not sufficiently large.
    """
    bbox = np.clip(
        bbox,
        [0] * 4,
        [img_height - 1, img_width - 1, img_height - 1, img_width - 1],
    )

    if bbox[2] - bbox[0] <= 1 or bbox[3] - bbox[1] <= 1:
        return None

    if og_bbox is not None:
        if area(bbox) / area(og_bbox) < DROP_BBOX_AREA_RATIO_THRES:
            return None

    return bbox


def rotate_bounding_box(angle: float, center: list, bbox: list) -> list:
    """
    Parameters
    ----------
    angle
        angle, in degrees, to rotate
    center
        (x, y) point around which to rotate
    bbox
        bounding box, of form [ymin, xmin, ymax, xmax], to rotate

    Returns
    -------
    rotated bounding box, as a list of length four.
    """
    center = np.array(center)
    angle_rad = np.pi * angle / 180

    rot_matrix = np.array(
        [
            [np.cos(angle_rad), np.sin(angle_rad)],
            [-np.sin(angle_rad), np.cos(angle_rad)],
        ]
    )

    points = np.array(
        [
            [bbox[1], bbox[1], bbox[3], bbox[3]],
            [bbox[0], bbox[2], bbox[0], bbox[2]],
        ]
    )
    new_points = rot_matrix @ (
        points - center.reshape(2, -1)
    ) + center.reshape(2, -1)

    minpts = new_points.min(1)
    maxpts = new_points.max(1)

    return [minpts[1], minpts[0], maxpts[1], maxpts[0]]


def apply_affine_matrix_to_bbox(matrix: np.ndarray, bbox: list) -> list:
    """Transforms a bounding box via an affine matrix

    Parameters
    ----------
    matrix
        3x3 affine matrix acting on the plane
    bbox
        list of length four of the form [y_min, x_min, y_max, x_max]

    Returns
    -------
    transformed bounding box
    """
    points = np.array(
        [
            [bbox[1], bbox[1], bbox[3], bbox[3]],
            [bbox[0], bbox[2], bbox[0], bbox[2]],
            [1.0, 1.0, 1.0, 1.0],
        ]
    )

    new_points = (matrix @ points)[:2]

    minpts = new_points.min(1)
    maxpts = new_points.max(1)

    return [minpts[1], minpts[0], maxpts[1], maxpts[0]]
