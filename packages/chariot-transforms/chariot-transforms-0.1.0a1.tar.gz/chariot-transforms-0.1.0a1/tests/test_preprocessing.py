import numpy as np
import pytest
import torch
import torchvision.transforms.functional as F
from PIL import Image

from chariot_transforms.preprocessing import (
    CLAHE,
    HistogramLinearStretch,
    PreprocessingCompose,
    Resize,
    ResizePreserveAspect,
)
from chariot_transforms.preprocessing.clahe import equalize_adapthist
from chariot_transforms.preprocessing.histogram_tools import linear_stretch


@pytest.fixture
def img() -> torch.Tensor:
    return torch.randint(0, 256, (1, 3, 50, 150), dtype=torch.uint8) / 255


@pytest.fixture
def pil_img() -> Image.Image:
    rng = np.random.RandomState(2023)
    return Image.fromarray(
        rng.randint(0, 255, size=(500, 200, 3), dtype=np.uint8)
    )


@pytest.fixture
def mask() -> Image.Image:
    rng = np.random.RandomState(2023)
    return Image.fromarray(rng.randint(0, 255, size=(50, 150), dtype=np.uint8))


@pytest.fixture
def img_arr() -> np.ndarray:
    rng = np.random.RandomState(2023)
    return rng.randint(0, 256, (50, 50, 3), dtype=np.uint8)


def test_resize_regression(pil_img: Image.Image):
    """Test commutativity of resize and PIL -> tensor conversion which
    will ensure backwards compatibility for when we replace PIL transforms
    with tensor transforms. Some testing has shown that these operations are not
    close enough and downstream detections/classifications can vary depending
    on which one is used.
    """
    new_shape = (300, 600)
    img_tensor = F.to_tensor(pil_img).unsqueeze(0)

    resizer = Resize(new_shape)
    out_tensor = resizer(img_tensor)
    # this is what we had for PIL images before
    out_pil = resizer(pil_img)

    torch.testing.assert_close(
        out_tensor[0], F.to_tensor(out_pil), atol=0.004, rtol=0.004
    )


def test_resize_preserve_aspect_regression(pil_img: Image.Image):
    """Test commutativity of resize and PIL -> tensor conversion which
    will ensure backwards compatibility for when we replace PIL transforms
    with tensor transforms. Some testing has shown that these operations are not
    close enough and downstream detections/classifications can vary depending
    on which one is used.
    """

    new_shape = (300, 600)
    img_tensor = F.to_tensor(pil_img).unsqueeze(0)

    resizer = ResizePreserveAspect(*new_shape)
    out_tensor = resizer(img_tensor)
    out_pil = resizer(pil_img)

    torch.testing.assert_close(
        out_tensor[0], F.to_tensor(out_pil), atol=0.004, rtol=0.004
    )


def test_histogram_linear_stretch(img: torch.Tensor):
    ls = HistogramLinearStretch(4)
    out = ls(img)
    assert out.shape == img.shape
    assert out.min() >= 0
    assert out.max() <= 1
    assert not torch.equal(out, img)


def test_clahe(img: torch.Tensor):
    clahe = CLAHE()
    out = clahe(img)
    assert out.shape == img.shape
    assert out.min() >= 0
    assert out.max() <= 1
    assert not torch.equal(out, img)


def test_clahe_dtype(img_arr: np.ndarray):
    """Check that we get the same CLAHE normalized output for uint8 image arrays as
    float arrays
    """
    out1 = equalize_adapthist(img_arr)
    out2 = equalize_adapthist(img_arr.astype(np.float32) / 255.0)

    np.testing.assert_almost_equal(out1, out2, decimal=6)


def test_linear_stretch_dtype(img_arr: np.ndarray):
    """Check that we get the same linear stretch normalized output for uint8 image arrays as
    float arrays
    """
    out1 = linear_stretch(img_arr, 0.6)
    out2 = linear_stretch(img_arr.astype(np.float32) / 255.0, 0.6)

    np.testing.assert_almost_equal(out1, out2, decimal=6)


def test_resize_tensor_shape_error(img):
    resize = Resize((60, 30))
    with pytest.raises(ValueError) as exc_info:
        resize(img[0])

    assert "img must be a rank 4 tensor" in str(exc_info)


def test_resize_shapes(img: torch.Tensor):
    for s in [(60, 60), (200, 500)]:
        for cls in [Resize, ResizePreserveAspect]:
            resizer = cls(s) if cls == Resize else cls(*s)
            out_tensor = resizer(img)

            # Image.size is (width, height)
            assert out_tensor.shape[2:4] == s


def test_variable_shapes(img: torch.Tensor):
    for min_size, max_size in [
        (20, 30),
        (25, 75),
        (35, 200),
        (65, 100),
        (100, 250),
        (175, 300),
    ]:
        resizer = Resize(min_size=min_size, max_size=max_size)
        out_tensor = resizer(img)

        # Same checks on Tensor output
        assert (min(out_tensor.shape[2:4]) == min_size) or (
            max(out_tensor.shape[2:4]) == max_size
        ), "min_size: {0}, max_size: {1}".format(min_size, max_size)
        assert (
            max(out_tensor.shape[2:4]) <= max_size
        ), f"maximum output size too large, min_size: {min_size}, max_size: {max_size}"


def test_shapes_with_mask(img: torch.Tensor, mask: Image.Image):
    for s in [(60, 60), (200, 500)]:
        for cls in [Resize, ResizePreserveAspect]:
            resizer = cls(s) if cls == Resize else cls(*s)
            out_tensor, out_mask = resizer(img, mask=mask)

            # Confirm masks are resized correctly.
            assert out_tensor.shape[2:4] == (s[0], s[1])
            assert out_mask.size == (s[1], s[0])


def test_preprocessing_compose():
    assert PreprocessingCompose(
        [Resize((60, 60)), CLAHE()]
    ).resize_component == Resize((60, 60))

    assert PreprocessingCompose(
        [HistogramLinearStretch(0.5), ResizePreserveAspect(12, 20), CLAHE()]
    ).resize_component == ResizePreserveAspect(12, 20)

    assert PreprocessingCompose([CLAHE()]).resize_component is None

    with pytest.raises(ValueError) as exc_info:
        PreprocessingCompose(
            [Resize((60, 60)), CLAHE(), ResizePreserveAspect(12, 20)]
        )
    assert "cannot contain more than one resize transform" in str(exc_info)


def test___eq__():
    """Test equality of transforms"""
    r1 = Resize((60, 60))
    r2 = Resize((60, 60))
    r3 = Resize((60, 70))

    rpa1 = ResizePreserveAspect(60, 60)
    rpa2 = ResizePreserveAspect(60, 60)
    rpa3 = ResizePreserveAspect(10, 70)

    c1 = CLAHE()
    c2 = CLAHE(nbins=256)
    c3 = CLAHE(nbins=128)

    ls1 = HistogramLinearStretch(0.5)
    ls2 = HistogramLinearStretch(0.5)
    ls3 = HistogramLinearStretch(0.1)

    assert r1 == r2
    assert r1 != r3

    assert rpa1 == rpa2
    assert rpa1 != rpa3

    assert c1 == c2
    assert c1 != c3

    assert ls1 == ls2
    assert ls1 != ls3

    assert r1 != rpa1
    assert r1 != c1
    assert r1 != ls1
    assert rpa1 != c1
    assert rpa1 != ls1
    assert c1 != ls1


def test_multiple_channels():
    """Test that the pre-processing transformations work with
    more than 3 channel imagery
    """
    n_channels = 3
    img = torch.randint(0, 256, (n_channels, 50, 150), dtype=torch.uint8) / 255
    img = img.unsqueeze(0)

    # these transforms
    for transform, expected_shape in [
        (Resize((60, 60)), (60, 60)),
        (ResizePreserveAspect(new_h=40, new_w=60), (40, 60)),
        (HistogramLinearStretch(3), (50, 150)),
    ]:
        out = transform(img)
        assert out.shape == (1, n_channels, *expected_shape)

        # check that the resize transforms operate channel-wise
        if isinstance(transform, (Resize, ResizePreserveAspect)):
            for c in range(n_channels):
                torch.testing.assert_close(
                    transform(img[:, c : c + 1, :, :]), out[:, c : c + 1, :, :]
                )


def test_batching():
    imgs = torch.rand(2, 3, 50, 150)

    for transform in [
        Resize((60, 60)),
        ResizePreserveAspect(new_h=40, new_w=60),
        HistogramLinearStretch(3),
        CLAHE(),
    ]:
        out = transform(imgs)
        # check that the resize transforms operate channel-wise
        for i in range(2):
            torch.testing.assert_close(
                transform(imgs[i : i + 1]), out[i : i + 1]
            )


def test_clahe_regression():
    """Regression test for CLAHE transform. guy_with_car_clahe.png was generated via
    ```
    from PIL import Image
    from chariot_transforms.preprocessing.transforms import IdentityPILTransform

    img = Image.open("tests/guy_with_car.jpg")
    clahe = IdentityPILTransform(histogram_equalization=True)
    clahe(img).save("tests/guy_with_car_clahe.png")
    ```
    """
    img = Image.open("tests/guy_with_car.jpg")
    img_tensor = F.to_tensor(img).unsqueeze(0)
    clahe = CLAHE()
    clahe_img_tensor = clahe(img_tensor)

    expected_img = Image.open("tests/guy_with_car_clahe.png")
    expected_img_tensor = F.to_tensor(expected_img).unsqueeze(0)

    assert (clahe_img_tensor - expected_img_tensor).abs().max().item() < 4e-3


def test_histogram_linear_stretch_regression():
    """Regression test for CLAHE transform. guy_with_car_clahe.png was generated via
    ```
    from PIL import Image
    from chariot_transforms.preprocessing.transforms import IdentityPILTransform

    img = Image.open("tests/guy_with_car.jpg")
    linear_stretch = IdentityPILTransform(histogram_linear_stretch=4)
    linear_stretch(img).save("tests/guy_with_car_linear_stretch.png")
    ```
    """
    img = Image.open("tests/guy_with_car.jpg")
    img_tensor = F.to_tensor(img).unsqueeze(0)
    linear_stretch = HistogramLinearStretch(4)
    linear_stretch_img_tensor = linear_stretch(img_tensor)

    expected_img = Image.open("tests/guy_with_car_linear_stretch.png")
    expected_img_tensor = F.to_tensor(expected_img).unsqueeze(0)

    assert (
        linear_stretch_img_tensor - expected_img_tensor
    ).abs().max().item() < 4e-3
