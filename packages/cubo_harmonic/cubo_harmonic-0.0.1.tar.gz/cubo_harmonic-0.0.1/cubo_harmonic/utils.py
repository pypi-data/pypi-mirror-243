import warnings
from typing import Dict, Optional, Union, List, Literal

import numpy as np
import torch
from opensr_test.lightglue import DISK, LightGlue, SuperPoint
from opensr_test.lightglue.utils import rbd
from opensr_test.utils import spectral_reducer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from skimage.registration import phase_cross_correlation

def spectral_reducer(
    X: torch.Tensor,
    method: Literal["mean", "median", "max", "min", "luminosity"] = "luminosity",
    rgb_bands: Optional[List[int]] = [0, 1, 2],
) -> torch.Tensor:
    """ Reduce the number of channels of a tensor from (C, H, W) to
    (H, W) using a given method.

    Args:
        X (torch.Tensor): The tensor to reduce.

        method (str, optional): The method used to reduce the number of
            channels. Must be one of "mean", "median", "max", "min",
            "luminosity". Defaults to "mean".

    Raises:
        ValueError: If the method is not valid.

    Returns:
        torch.Tensor: The reduced tensor.
    """
    if method == "mean":
        return X.mean(dim=0)
    elif method == "median":
        return X.median(dim=0).values
    elif method == "max":
        return X.max(dim=0).values
    elif method == "min":
        return X.min(dim=0).values
    elif method == "luminosity":
        return (
            0.2126*X[rgb_bands[0]] +
            0.7152*X[rgb_bands[1]] +
            0.0722*X[rgb_bands[2]]
        )
    else:
        raise ValueError(
            "Invalid method. Must be one of 'mean', 'median', 'max', 'min', 'luminosity'."
        )

def spatia_polynomial_fit(X: np.ndarray, y: np.ndarray, d: int) -> Pipeline:
    """Fit a polynomial of degree d to the points

    Args:
        X (np.ndarray): Array with the x coordinates or y coordinates of the points (image 1)
        y (np.ndarray): Array with the x coordinates or y coordinates of the points (image 2)
        d (int): Degree of the polynomial

    Returns:
        Pipeline: The fitted model
    """

    pipe_model = make_pipeline(
        PolynomialFeatures(degree=d, include_bias=False), LinearRegression()
    ).fit(X, y)

    return pipe_model

def spatial_get_matching_points(
    img01: torch.Tensor,
    img02: torch.Tensor,
    model: tuple,
    spectral_reducer_method: str,
    rgb_bands: List[int],
    device: str = "cpu",
) -> Dict[str, torch.Tensor]:
    """Predict the spatial error between two images

    Args:
        img01 (torch.Tensor): A torch.tensor with the image 1 (B, H, W)
        img02 (torch.Tensor): A torch.tensor with the ref image (B, H, W)
        model (tuple): A tuple with the feature extractor and the matcher
        device (str, optional): The device to use. Defaults to 'cpu'.

    Returns:
        Dict[str, torch.Tensor]: A dictionary with the points0,
            points1, matches01 and image size.
    """

    # unpack the model - send to device
    extractor, matcher = model
    extractor = extractor.to(device)
    matcher = matcher.to(device)

    # Send the data to the device
    img01 = spectral_reducer(
        X=img01.to(device),
        method=spectral_reducer_method,
        rgb_bands=rgb_bands
    )[None]

    img02 = spectral_reducer(
        X=img02.to(device),
        method=spectral_reducer_method,
        rgb_bands=rgb_bands
    )[None]

    # extract local features
    with torch.no_grad():
        # auto-resize the image, disable with resize=None
        feats0 = extractor.extract(img01, resize=None)
        if feats0["keypoints"].shape[1] == 0:
            warnings.warn("No keypoints found in image 1")
            return False

        feats1 = extractor.extract(img02, resize=None)
        if feats1["keypoints"].shape[1] == 0:
            warnings.warn("No keypoints found in image 2")
            return False

        # match the features
        matches01 = matcher({"image0": feats0, "image1": feats1})

    # remove batch dimension
    feats0, feats1, matches01 = [rbd(x) for x in [feats0, feats1, matches01]]

    matches = matches01["matches"]  # indices with shape (K,2)
    points0 = feats0["keypoints"][
        matches[..., 0]
    ]  # coordinates in image #0, shape (K,2)
    points1 = feats1["keypoints"][
        matches[..., 1]
    ]  # coordinates in image #1, shape (K,2)

    matching_points = {
        "points0": points0,
        "points1": points1,
        "matches01": matches01,
        "img_size": tuple(img01.shape[-2:]),
    }

    return matching_points

def spatial_model_fit(
    matching_points: Dict[str, torch.Tensor],
    n_points: Optional[int] = 10,
    threshold_distance: Optional[int] = 5,
    verbose: Optional[bool] = True
) -> Union[np.ndarray, dict]:
    """Get a model that minimizes the spatial error between two images

    Args:
        matching_points (Dict[str, torch.Tensor]): A dictionary with the points0,
            points1 and image size.
        n_points (Optional[int], optional): The minimum number of points. Defaults
            to 10.
        threshold_distance (Optional[int], optional): The maximum distance between
            the points. Defaults to 5 pixels.
        verbose (Optional[bool], optional): If True, print the error. Defaults to
            False.
        scale (Optional[int], optional): The scale factor to use. Defaults to 1.

    Returns:
        np.ndarray: The spatial error between the two images
    """

    points0 = matching_points["points0"]
    points1 = matching_points["points1"]

    # if the distance between the points is higher than 5 pixels,
    # it is considered a bad match
    dist = torch.sqrt(torch.sum((points0 - points1) ** 2, dim=1))
    thres = dist < threshold_distance
    p0 = points0[thres]
    p1 = points1[thres]

    # if not enough points, return 0
    if p0.shape[0] < n_points:
        warnings.warn("Not enough points to fit the model")
        return False

    # from torch.Tensor to numpy array
    p0 = p0.detach().cpu().numpy()
    p1 = p1.detach().cpu().numpy()

    # Fit a polynomial of degree 2 to the points
    X_img0 = p0[:, 0].reshape(-1, 1)
    X_img1 = p1[:, 0].reshape(-1, 1)
    model_x = spatia_polynomial_fit(X_img0, X_img1, 1)

    y_img0 = p0[:, 1].reshape(-1, 1)
    y_img1 = p1[:, 1].reshape(-1, 1)
    model_y = spatia_polynomial_fit(y_img0, y_img1, 1)

    # display error
    xoffset = np.round(model_x.predict(np.array(0).reshape(-1, 1)))
    yoffset = np.round(model_y.predict(np.array(0).reshape(-1, 1)))

    xhat = X_img0 + xoffset
    yhat = y_img0 + yoffset

    # full error
    full_error1 = np.sqrt((xhat - X_img1) ** 2 + (yhat - y_img1) ** 2)
    full_error2 = np.sqrt((X_img0 - X_img1) ** 2 + (y_img0 - y_img1) ** 2)

    if verbose:
        print(f"Initial [RMSE]: %.04f" % np.mean(full_error2))
        print(f"Final [RMSE]: %.04f" % np.mean(full_error1))

    to_export = {
        "offset": (int(xoffset), int(yoffset)),
        "error": (np.mean(full_error2), np.mean(full_error1)),
    }

    return to_export


def spatial_model_transform_pixel(
    image1: torch.Tensor,
    spatial_offset: tuple,
) -> torch.Tensor:
    """ Transform the image according to the spatial offset

    Args:
        image1 (torch.Tensor): The image 1 with shape (B, H, W)
        spatial_offset (tuple): The spatial offset estimated by the
            spatial_model_fit function.
    Returns:
        torch.Tensor: The transformed image
    """
    x_offs, y_offs = spatial_offset["offset"]
    if (x_offs + y_offs) == 0:
        return image1

    # get max offset
    moffs = np.max(np.abs([x_offs, y_offs]))


    # Add padding according to the offset
    image_pad = torch.nn.functional.pad(
        image1, (moffs, moffs, moffs, moffs), mode="constant", value=0
    )

    if x_offs < 0:
        image_pad = image_pad[:, :, (moffs + x_offs) :]
    elif x_offs > 0:
        image_pad = image_pad[:, :, (moffs - x_offs) :]

    if y_offs < 0:
        image_pad = image_pad[:, (moffs - y_offs) :, :]
    elif y_offs > 0:
        image_pad = image_pad[:, (moffs + y_offs) :, :]

    # remove padding
    final_image = image_pad[:, 0:image1.shape[1], 0:image1.shape[2]]

    return final_image

def spatial_model_transform(
    lr_to_hr: torch.Tensor,
    hr: torch.Tensor,
    spatial_offset: tuple
) -> torch.Tensor:
    """ Transform the image according to the spatial offset

    Args:
        lr_to_hr (torch.Tensor): The low resolution image
        hr (torch.Tensor): The high resolution image
        spatial_offset (tuple): The spatial offset estimated by the
            spatial_model_fit function.
    Returns:
        torch.Tensor: The transformed image
    """
    offset_image = spatial_model_transform_pixel(
        image1=lr_to_hr,
        spatial_offset=spatial_offset
    )
    hr_masked = hr * (offset_image != 0)

    # to numpy
    offset_image = offset_image.detach().cpu().numpy()
    hr_masked = hr_masked.detach().cpu().numpy()

    # Subpixel refinement
    shift, error, diffphase = phase_cross_correlation(
        offset_image.mean(0), hr_masked.mean(0), upsample_factor=100
    )
    print("Offset a sub-pixel: ", shift)
    return spatial_model_transform_pixel(
        image1=torch.from_numpy(offset_image).float(),
        spatial_offset={"offset": list(np.int16(np.round(shift)))}
    )