# IMPORTANT NOTES:
#     DO NOT MODIFY THIS FILE (please).
#
#     The functions in this file are an extract from scikit-image (v0.21.0), specifically:
#     skimage.exposure.equalize_adapthist
#     https://github.com/scikit-image/scikit-image/blob/v0.21.0/skimage/exposure/_adapthist.py
#
#
# The purpose of this file is to expose: skimage.exposure.equalize_adaphist without
# all the dependencies of skimage.  E.g.
#
#     from teddy.utils.skimage_clahe import equalize_adapthist
#
# should work as a drop-in replacement for:
#
#     from skimage.exposure import equalize_adapthist
#


# LICENSE (copied from equalize_adapthist in scikit-image)
# License: BSD-3-Clause
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# .
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE HOLDERS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import functools
import math
import numbers
import warnings
from warnings import warn

import numpy as np

__all__ = ["equalize_adapthist"]

# From: https://github.com/scikit-image/scikit-image/blob/v0.21.0/skimage/util/dtype.py#L20
_integer_types = (
    np.byte,
    np.ubyte,  # 8 bits
    np.short,
    np.ushort,  # 16 bits
    np.intc,
    np.uintc,  # 16 or 32 or 64 bits
    int,
    np.int_,
    np.uint,  # 32 or 64 bits
    np.longlong,
    np.ulonglong,
)  # 64 bits

_integer_ranges = {
    t: (np.iinfo(t).min, np.iinfo(t).max) for t in _integer_types
}

dtype_range = {
    bool: (False, True),
    np.bool_: (False, True),
    float: (-1, 1),
    np.float_: (-1, 1),
    np.float16: (-1, 1),
    np.float32: (-1, 1),
    np.float64: (-1, 1),
}

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    if hasattr(np, "bool8"):
        dtype_range[np.bool8] = (False, True)

dtype_range.update(_integer_ranges)

_supported_types = list(dtype_range.keys())


NR_OF_GRAY = 2**14  # number of grayscale levels to use in CLAHE algorithm

DTYPE_RANGE = dtype_range.copy()
DTYPE_RANGE.update((d.__name__, limits) for d, limits in dtype_range.items())
DTYPE_RANGE.update(
    {
        "uint10": (0, 2**10 - 1),
        "uint12": (0, 2**12 - 1),
        "uint14": (0, 2**14 - 1),
        "bool": dtype_range[bool],
        "float": dtype_range[np.float64],
    }
)


# From: https://github.com/scikit-image/scikit-image/blob/v0.21.0/skimage/_shared/utils.py#L533
def reshape_nd(arr, ndim, dim):
    if arr.ndim != 1:
        raise ValueError("arr must be a 1D array")
    new_shape = [1] * ndim
    new_shape[dim] = -1
    return np.reshape(arr, new_shape)


# From: https://github.com/scikit-image/scikit-image/blob/v0.21.0/skimage/_shared/utils.py#L508
def slice_at_axis(sl, axis):
    return (slice(None),) * axis + (sl,) + (...,)


# From: https://github.com/scikit-image/scikit-image/blob/v0.21.0/skimage/_shared/utils.py#L279
class channel_as_last_axis:
    def __init__(
        self,
        channel_arg_positions=(0,),
        channel_kwarg_names=(),
        multichannel_output=True,
    ):
        self.arg_positions = set(channel_arg_positions)
        self.kwarg_names = set(channel_kwarg_names)
        self.multichannel_output = multichannel_output

    def __call__(self, func):
        @functools.wraps(func)
        def fixed_func(*args, **kwargs):
            channel_axis = kwargs.get("channel_axis", None)

            if channel_axis is None:
                return func(*args, **kwargs)

            if np.isscalar(channel_axis):
                channel_axis = (channel_axis,)
            if len(channel_axis) > 1:
                raise ValueError(
                    "only a single channel axis is currently supported"
                )

            if channel_axis == (-1,) or channel_axis == -1:
                return func(*args, **kwargs)

            if self.arg_positions:
                new_args = []
                for pos, arg in enumerate(args):
                    if pos in self.arg_positions:
                        new_args.append(np.moveaxis(arg, channel_axis[0], -1))
                    else:
                        new_args.append(arg)
                new_args = tuple(new_args)
            else:
                new_args = args

            for name in self.kwarg_names:
                kwargs[name] = np.moveaxis(kwargs[name], channel_axis[0], -1)

            # now that we have moved the channels axis to the last position,
            # change the channel_axis argument to -1
            kwargs["channel_axis"] = -1

            # Call the function with the fixed arguments
            out = func(*new_args, **kwargs)
            if self.multichannel_output:
                out = np.moveaxis(out, -1, channel_axis[0])
            return out

        return fixed_func


def dtype_limits(image, clip_negative=False):
    imin, imax = dtype_range[image.dtype.type]
    if clip_negative:
        imin = 0
    return imin, imax


def _dtype_itemsize(itemsize, *dtypes):
    return next(dt for dt in dtypes if np.dtype(dt).itemsize >= itemsize)


def _dtype_bits(kind, bits, itemsize=1):
    s = next(
        i
        for i in (itemsize,) + (2, 4, 8)
        if bits < (i * 8) or (bits == (i * 8) and kind == "u")
    )

    return np.dtype(kind + str(s))


def _scale(a, n, m, copy=True):
    kind = a.dtype.kind
    if n > m and a.max() < 2**m:
        mnew = int(np.ceil(m / 2) * 2)
        if mnew > m:
            dtype = f"int{mnew}"
        else:
            dtype = f"uint{mnew}"
        n = int(np.ceil(n / 2) * 2)
        warn(
            f"Downcasting {a.dtype} to {dtype} without scaling because max "
            f"value {a.max()} fits in {dtype}",
            stacklevel=3,
        )
        return a.astype(_dtype_bits(kind, m))
    elif n == m:
        return a.copy() if copy else a
    elif n > m:
        # downscale with precision loss
        if copy:
            b = np.empty(a.shape, _dtype_bits(kind, m))
            np.floor_divide(
                a, 2 ** (n - m), out=b, dtype=a.dtype, casting="unsafe"
            )
            return b
        else:
            a //= 2 ** (n - m)
            return a
    elif m % n == 0:
        # exact upscale to a multiple of `n` bits
        if copy:
            b = np.empty(a.shape, _dtype_bits(kind, m))
            np.multiply(a, (2**m - 1) // (2**n - 1), out=b, dtype=b.dtype)
            return b
        else:
            a = a.astype(_dtype_bits(kind, m, a.dtype.itemsize), copy=False)
            a *= (2**m - 1) // (2**n - 1)
            return a
    else:
        # upscale to a multiple of `n` bits,
        # then downscale with precision loss
        o = (m // n + 1) * n
        if copy:
            b = np.empty(a.shape, _dtype_bits(kind, o))
            np.multiply(a, (2**o - 1) // (2**n - 1), out=b, dtype=b.dtype)
            b //= 2 ** (o - m)
            return b
        else:
            a = a.astype(_dtype_bits(kind, o, a.dtype.itemsize), copy=False)
            a *= (2**o - 1) // (2**n - 1)
            a //= 2 ** (o - m)
            return a


# From: https://github.com/scikit-image/scikit-image/blob/v0.21.0/skimage/util/dtype.py#L188
def _convert(image, dtype, force_copy=False, uniform=False):
    image = np.asarray(image)
    dtypeobj_in = image.dtype
    if dtype is np.floating:
        dtypeobj_out = np.dtype("float64")
    else:
        dtypeobj_out = np.dtype(dtype)
    dtype_in = dtypeobj_in.type
    dtype_out = dtypeobj_out.type
    kind_in = dtypeobj_in.kind
    kind_out = dtypeobj_out.kind
    itemsize_in = dtypeobj_in.itemsize
    itemsize_out = dtypeobj_out.itemsize

    if np.issubdtype(dtype_in, np.obj2sctype(dtype)):
        if force_copy:
            image = image.copy()
        return image

    if not (dtype_in in _supported_types and dtype_out in _supported_types):
        raise ValueError(
            f"Cannot convert from {dtypeobj_in} to " f"{dtypeobj_out}."
        )

    if kind_in in "ui":
        imin_in = np.iinfo(dtype_in).min
        imax_in = np.iinfo(dtype_in).max
    if kind_out in "ui":
        imin_out = np.iinfo(dtype_out).min
        imax_out = np.iinfo(dtype_out).max

    # any -> binary
    if kind_out == "b":
        return image > dtype_in(dtype_range[dtype_in][1] / 2)

    # binary -> any
    if kind_in == "b":
        result = image.astype(dtype_out)
        if kind_out != "f":
            result *= dtype_out(dtype_range[dtype_out][1])
        return result

    # float -> any
    if kind_in == "f":
        if kind_out == "f":
            # float -> float
            return image.astype(dtype_out)

        if np.min(image) < -1.0 or np.max(image) > 1.0:
            raise ValueError("Images of type float must be between -1 and 1.")
        # floating point -> integer
        # use float type that can represent output integer type
        computation_type = _dtype_itemsize(
            itemsize_out, dtype_in, np.float32, np.float64
        )

        if not uniform:
            if kind_out == "u":
                image_out = np.multiply(
                    image, imax_out, dtype=computation_type
                )
            else:
                image_out = np.multiply(
                    image, (imax_out - imin_out) / 2, dtype=computation_type
                )
                image_out -= 1.0 / 2.0
            np.rint(image_out, out=image_out)
            np.clip(image_out, imin_out, imax_out, out=image_out)
        elif kind_out == "u":
            image_out = np.multiply(
                image, imax_out + 1, dtype=computation_type
            )
            np.clip(image_out, 0, imax_out, out=image_out)
        else:
            image_out = np.multiply(
                image,
                (imax_out - imin_out + 1.0) / 2.0,
                dtype=computation_type,
            )
            np.floor(image_out, out=image_out)
            np.clip(image_out, imin_out, imax_out, out=image_out)
        return image_out.astype(dtype_out)

    # signed/unsigned int -> float
    if kind_out == "f":
        # use float type that can exactly represent input integers
        computation_type = _dtype_itemsize(
            itemsize_in, dtype_out, np.float32, np.float64
        )

        if kind_in == "u":
            # using np.divide or np.multiply doesn't copy the data
            # until the computation time
            image = np.multiply(image, 1.0 / imax_in, dtype=computation_type)
            # DirectX uses this conversion also for signed ints
            # if imin_in:
            #     np.maximum(image, -1.0, out=image)
        elif kind_in == "i":
            # From DirectX conversions:
            # The most negative value maps to -1.0f
            # Every other value is converted to a float (call it c)
            # and then result = c * (1.0f / (2⁽ⁿ⁻¹⁾-1)).

            image = np.multiply(image, 1.0 / imax_in, dtype=computation_type)
            np.maximum(image, -1.0, out=image)

        else:
            image = np.add(image, 0.5, dtype=computation_type)
            image *= 2 / (imax_in - imin_in)

        return np.asarray(image, dtype_out)

    # unsigned int -> signed/unsigned int
    if kind_in == "u":
        if kind_out == "i":
            # unsigned int -> signed int
            image = _scale(image, 8 * itemsize_in, 8 * itemsize_out - 1)
            return image.view(dtype_out)
        else:
            # unsigned int -> unsigned int
            return _scale(image, 8 * itemsize_in, 8 * itemsize_out)

    # signed int -> unsigned int
    if kind_out == "u":
        image = _scale(image, 8 * itemsize_in - 1, 8 * itemsize_out)
        result = np.empty(image.shape, dtype_out)
        np.maximum(image, 0, out=result, dtype=image.dtype, casting="unsafe")
        return result

    # signed int -> signed int
    if itemsize_in > itemsize_out:
        return _scale(image, 8 * itemsize_in - 1, 8 * itemsize_out - 1)

    image = image.astype(_dtype_bits("i", itemsize_out * 8))
    image -= imin_in
    image = _scale(image, 8 * itemsize_in, 8 * itemsize_out, copy=False)
    image += imin_out
    return image.astype(dtype_out)


def _prepare_colorarray(arr, force_copy=False, *, channel_axis=-1):
    """Check the shape of the array and convert it to
    floating point representation.
    """
    arr = np.asanyarray(arr)

    if arr.shape[channel_axis] != 3:
        msg = (
            f"the input array must have size 3 along `channel_axis`, "
            f"got {arr.shape}"
        )
        raise ValueError(msg)

    float_dtype = _supported_float_type(arr.dtype)
    if float_dtype == np.float32:
        _func = img_as_float32
    else:
        _func = img_as_float64
    return _func(arr, force_copy=force_copy)


def _validate_channel_axis(channel_axis, ndim):
    if not isinstance(channel_axis, int):
        raise TypeError("channel_axis must be an integer")
    if channel_axis < -ndim or channel_axis >= ndim:
        raise np.AxisError("channel_axis exceeds array dimensions")


def img_as_float32(image, force_copy=False):
    return _convert(image, np.float32, force_copy)


def img_as_float64(image, force_copy=False):
    return _convert(image, np.float64, force_copy)


def img_as_float(image, force_copy=False):
    return _convert(image, np.floating, force_copy)


def img_as_uint(image, force_copy=False):
    return _convert(image, np.uint16, force_copy)


def img_as_int(image, force_copy=False):
    return _convert(image, np.int16, force_copy)


@channel_as_last_axis()
def rgb2hsv(rgb, *, channel_axis=-1):
    input_is_one_pixel = rgb.ndim == 1
    if input_is_one_pixel:
        rgb = rgb[np.newaxis, ...]

    arr = _prepare_colorarray(rgb, channel_axis=-1)
    out = np.empty_like(arr)

    # -- V channel
    out_v = arr.max(-1)

    # -- S channel
    delta = arr.ptp(-1)
    # Ignore warning for zero divided by zero
    old_settings = np.seterr(invalid="ignore")
    out_s = delta / out_v
    out_s[delta == 0.0] = 0.0

    # -- H channel
    # red is max
    idx = arr[..., 0] == out_v
    out[idx, 0] = (arr[idx, 1] - arr[idx, 2]) / delta[idx]

    # green is max
    idx = arr[..., 1] == out_v
    out[idx, 0] = 2.0 + (arr[idx, 2] - arr[idx, 0]) / delta[idx]

    # blue is max
    idx = arr[..., 2] == out_v
    out[idx, 0] = 4.0 + (arr[idx, 0] - arr[idx, 1]) / delta[idx]
    out_h = (out[..., 0] / 6.0) % 1.0
    out_h[delta == 0.0] = 0.0

    np.seterr(**old_settings)

    # -- output
    out[..., 0] = out_h
    out[..., 1] = out_s
    out[..., 2] = out_v

    # # remove NaN
    out[np.isnan(out)] = 0

    if input_is_one_pixel:
        out = np.squeeze(out, axis=0)

    return out


@channel_as_last_axis()
def hsv2rgb(hsv, *, channel_axis=-1):
    arr = _prepare_colorarray(hsv, channel_axis=-1)

    hi = np.floor(arr[..., 0] * 6)
    f = arr[..., 0] * 6 - hi
    p = arr[..., 2] * (1 - arr[..., 1])
    q = arr[..., 2] * (1 - f * arr[..., 1])
    t = arr[..., 2] * (1 - (1 - f) * arr[..., 1])
    v = arr[..., 2]

    hi = np.stack([hi, hi, hi], axis=-1).astype(np.uint8) % 6
    out = np.choose(
        hi,
        np.stack(
            [
                np.stack((v, t, p), axis=-1),
                np.stack((q, v, p), axis=-1),
                np.stack((p, v, t), axis=-1),
                np.stack((p, q, v), axis=-1),
                np.stack((t, p, v), axis=-1),
                np.stack((v, p, q), axis=-1),
            ]
        ),
    )
    return out


# From: https://github.com/scikit-image/scikit-image/blob/v0.21.0/skimage/_shared/utils.py#L697
new_float_type = {
    # preserved types
    np.float32().dtype.char: np.float32,
    np.float64().dtype.char: np.float64,
    np.complex64().dtype.char: np.complex64,
    np.complex128().dtype.char: np.complex128,
    # altered types
    np.float16().dtype.char: np.float32,
    "g": np.float64,  # np.float128 ; doesn't exist on windows
    "G": np.complex128,  # np.complex256 ; doesn't exist on windows
}


# From: https://github.com/scikit-image/scikit-image/blob/v0.21.0/skimage/_shared/utils.py#L710
def _supported_float_type(input_dtype, allow_complex=False):
    if isinstance(input_dtype, tuple):
        return np.result_type(*(_supported_float_type(d) for d in input_dtype))
    input_dtype = np.dtype(input_dtype)
    if not allow_complex and input_dtype.kind == "c":
        raise ValueError("complex valued input is not supported")
    return new_float_type.get(input_dtype.char, np.float64)


# From: https://github.com/scikit-image/scikit-image/blob/v0.21.0/skimage/color/adapt_rgb.py#L12
def is_rgb_like(image, channel_axis=-1):
    """Return True if the image *looks* like it's RGB.

    This function should not be public because it is only intended to be used
    for functions that don't accept volumes as input, since checking an image's
    shape is fragile.
    """
    return (image.ndim == 3) and (image.shape[channel_axis] in (3, 4))


# From: https://github.com/scikit-image/scikit-image/blob/v0.21.0/skimage/color/adapt_rgb.py#L22
def adapt_rgb(apply_to_rgb):
    def decorator(image_filter):
        @functools.wraps(image_filter)
        def image_filter_adapted(image, *args, **kwargs):
            if is_rgb_like(image):
                return apply_to_rgb(image_filter, image, *args, **kwargs)
            else:
                return image_filter(image, *args, **kwargs)

        return image_filter_adapted

    return decorator


def hsv_value(image_filter, image, *args, **kwargs):
    # Slice the first three channels so that we remove any alpha channels.
    hsv = rgb2hsv(image[:, :, :3])
    value = hsv[:, :, 2].copy()
    value = image_filter(value, *args, **kwargs)
    hsv[:, :, 2] = _convert(value, hsv.dtype)
    return hsv2rgb(hsv)


def _output_dtype(dtype_or_range, image_dtype):
    if type(dtype_or_range) in [list, tuple, np.ndarray]:
        # pair of values: always return float.
        return _supported_float_type(image_dtype)
    if type(dtype_or_range) == type:
        # already a type: return it
        return dtype_or_range
    if dtype_or_range in DTYPE_RANGE:
        # string key in DTYPE_RANGE dictionary
        try:
            # if it's a canonical numpy dtype, convert
            return np.dtype(dtype_or_range).type
        except TypeError:  # uint10, uint12, uint14
            # otherwise, return uint16
            return np.uint16
    else:
        raise ValueError(
            "Incorrect value for out_range, should be a valid image data "
            f"type or a pair of values, got {dtype_or_range}."
        )


def intensity_range(image, range_values="image", clip_negative=False):
    if range_values == "dtype":
        range_values = image.dtype.type

    if range_values == "image":
        i_min = np.min(image)
        i_max = np.max(image)
    elif range_values in DTYPE_RANGE:
        i_min, i_max = DTYPE_RANGE[range_values]
        if clip_negative:
            i_min = 0
    else:
        i_min, i_max = range_values
    return i_min, i_max


def rescale_intensity(image, in_range="image", out_range="dtype"):
    if out_range in ["dtype", "image"]:
        out_dtype = _output_dtype(image.dtype.type, image.dtype)
    else:
        out_dtype = _output_dtype(out_range, image.dtype)

    imin, imax = map(float, intensity_range(image, in_range))
    omin, omax = map(
        float, intensity_range(image, out_range, clip_negative=(imin >= 0))
    )

    image = np.clip(image, imin, imax)

    if imin != imax:
        image = (image - imin) / (imax - imin)
        return (image * (omax - omin) + omin).astype(out_dtype)
    else:
        return np.clip(image, omin, omax).astype(out_dtype)


def _clahe(image, kernel_size, clip_limit, nbins):
    ndim = image.ndim
    dtype = image.dtype

    pad_start_per_dim = [k // 2 for k in kernel_size]

    pad_end_per_dim = [
        (k - s % k) % k + int(np.ceil(k / 2.0))
        for k, s in zip(kernel_size, image.shape)
    ]

    image = np.pad(
        image,
        [[p_i, p_f] for p_i, p_f in zip(pad_start_per_dim, pad_end_per_dim)],
        mode="reflect",
    )

    bin_size = 1 + NR_OF_GRAY // nbins
    lut = np.arange(NR_OF_GRAY, dtype=np.min_scalar_type(NR_OF_GRAY))
    lut //= bin_size

    image = lut[image]

    ns_hist = [int(s / k) - 1 for s, k in zip(image.shape, kernel_size)]
    hist_blocks_shape = np.array([ns_hist, kernel_size]).T.flatten()
    hist_blocks_axis_order = np.array(
        [np.arange(0, ndim * 2, 2), np.arange(1, ndim * 2, 2)]
    ).flatten()
    hist_slices = [
        slice(k // 2, k // 2 + n * k) for k, n in zip(kernel_size, ns_hist)
    ]
    hist_blocks = image[tuple(hist_slices)].reshape(hist_blocks_shape)
    hist_blocks = np.transpose(hist_blocks, axes=hist_blocks_axis_order)
    hist_block_assembled_shape = hist_blocks.shape
    hist_blocks = hist_blocks.reshape((math.prod(ns_hist), -1))

    # Calculate actual clip limit
    kernel_elements = math.prod(kernel_size)
    if clip_limit > 0.0:
        clim = int(np.clip(clip_limit * kernel_elements, 1, None))
    else:
        # largest possible value, i.e., do not clip (AHE)
        clim = kernel_elements

    hist = np.apply_along_axis(np.bincount, -1, hist_blocks, minlength=nbins)
    hist = np.apply_along_axis(clip_histogram, -1, hist, clip_limit=clim)
    hist = map_histogram(hist, 0, NR_OF_GRAY - 1, kernel_elements)
    hist = hist.reshape(hist_block_assembled_shape[:ndim] + (-1,))

    # duplicate leading mappings in each dim
    map_array = np.pad(
        hist, [[1, 1] for _ in range(ndim)] + [[0, 0]], mode="edge"
    )

    ns_proc = [int(s / k) for s, k in zip(image.shape, kernel_size)]
    blocks_shape = np.array([ns_proc, kernel_size]).T.flatten()
    blocks_axis_order = np.array(
        [np.arange(0, ndim * 2, 2), np.arange(1, ndim * 2, 2)]
    ).flatten()
    blocks = image.reshape(blocks_shape)
    blocks = np.transpose(blocks, axes=blocks_axis_order)
    blocks_flattened_shape = blocks.shape
    blocks = np.reshape(
        blocks, (math.prod(ns_proc), math.prod(blocks.shape[ndim:]))
    )

    # calculate interpolation coefficients
    coeffs = np.meshgrid(
        *tuple([np.arange(k) / k for k in kernel_size[::-1]]), indexing="ij"
    )
    coeffs = [np.transpose(c).flatten() for c in coeffs]
    inv_coeffs = [1 - c for dim, c in enumerate(coeffs)]

    result = np.zeros(blocks.shape, dtype=np.float32)
    for iedge, edge in enumerate(np.ndindex(*([2] * ndim))):
        edge_maps = map_array[
            tuple([slice(e, e + n) for e, n in zip(edge, ns_proc)])
        ]
        edge_maps = edge_maps.reshape((math.prod(ns_proc), -1))

        # apply map
        edge_mapped = np.take_along_axis(edge_maps, blocks, axis=-1)

        # interpolate
        edge_coeffs = np.prod(
            [[inv_coeffs, coeffs][e][d] for d, e in enumerate(edge[::-1])], 0
        )

        result += (edge_mapped * edge_coeffs).astype(result.dtype)

    result = result.astype(dtype)

    # rebuild result image from blocks
    result = result.reshape(blocks_flattened_shape)
    blocks_axis_rebuild_order = np.array(
        [np.arange(0, ndim), np.arange(ndim, ndim * 2)]
    ).T.flatten()
    result = np.transpose(result, axes=blocks_axis_rebuild_order)
    result = result.reshape(image.shape)

    # undo padding
    unpad_slices = tuple(
        [
            slice(p_i, s - p_f)
            for p_i, p_f, s in zip(
                pad_start_per_dim, pad_end_per_dim, image.shape
            )
        ]
    )
    result = result[unpad_slices]

    return result


@adapt_rgb(hsv_value)
def equalize_adapthist(image, kernel_size=None, clip_limit=0.01, nbins=256):
    float_dtype = _supported_float_type(image.dtype)
    image = img_as_uint(image)
    image = np.round(
        rescale_intensity(image, out_range=(0, NR_OF_GRAY - 1))
    ).astype(np.min_scalar_type(NR_OF_GRAY))

    if kernel_size is None:
        kernel_size = tuple([max(s // 8, 1) for s in image.shape])
    elif isinstance(kernel_size, numbers.Number):
        kernel_size = (kernel_size,) * image.ndim
    elif len(kernel_size) != image.ndim:
        raise ValueError(f"Incorrect value of `kernel_size`: {kernel_size}")

    kernel_size = [int(k) for k in kernel_size]

    image = _clahe(image, kernel_size, clip_limit, nbins)
    image = image.astype(float_dtype, copy=False)
    return rescale_intensity(image)


def clip_histogram(hist, clip_limit):
    # calculate total number of excess pixels
    excess_mask = hist > clip_limit
    excess = hist[excess_mask]
    n_excess = excess.sum() - excess.size * clip_limit
    hist[excess_mask] = clip_limit

    # Second part: clip histogram and redistribute excess pixels in each bin
    bin_incr = n_excess // hist.size  # average binincrement
    upper = clip_limit - bin_incr  # Bins larger than upper set to cliplimit

    low_mask = hist < upper
    n_excess -= hist[low_mask].size * bin_incr
    hist[low_mask] += bin_incr

    mid_mask = np.logical_and(hist >= upper, hist < clip_limit)
    mid = hist[mid_mask]
    n_excess += mid.sum() - mid.size * clip_limit
    hist[mid_mask] = clip_limit

    while n_excess > 0:  # Redistribute remaining excess
        prev_n_excess = n_excess
        for index in range(hist.size):
            under_mask = hist < clip_limit
            step_size = max(1, np.count_nonzero(under_mask) // n_excess)
            under_mask = under_mask[index::step_size]
            hist[index::step_size][under_mask] += 1
            n_excess -= np.count_nonzero(under_mask)
            if n_excess <= 0:
                break
        if prev_n_excess == n_excess:
            break

    return hist


def map_histogram(hist, min_val, max_val, n_pixels):
    out = np.cumsum(hist, axis=-1).astype(float)
    out *= (max_val - min_val) / n_pixels
    out += min_val
    np.clip(out, a_min=None, a_max=max_val, out=out)

    return out.astype(int)
