import numpy as np


def linear_stretch(arr: np.ndarray, percentage: float) -> np.ndarray:
    """
    Applies a linear stretch to the histogram of arr (maintaining its shape).
    Returned array will have values in [0, 1].
    If percentage is close to 50 division by 0 may periodically occur.
    If percentage is larger than 50 returned values will be negative.
    It is recommended that percentage be in (0, 5].
    """
    lower, upper = np.percentile(arr.flatten(), [percentage, 100 - percentage])
    return np.clip((arr - lower) / (upper - lower), a_min=0, a_max=1)
