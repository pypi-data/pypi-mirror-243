import torch
from opensr_test.utils import hq_histogram_matching
from cubo_harmonic.utils import (
    spatial_model_fit, spatial_model_transform,
    spatial_get_matching_points
)
from opensr_test.lightglue import DISK, LightGlue, SuperPoint


def spatial_setup_model(
    features: str = "superpoint",
    matcher: str = "lightglue",
    max_num_keypoints: int = 2048,
    device: str = "cpu",
) -> tuple:
    """Setup the model for spatial check

    Args:
        features (str, optional): The feature extractor. Defaults to 'superpoint'.
        matcher (str, optional): The matcher. Defaults to 'lightglue'.
        max_num_keypoints (int, optional): The maximum number of keypoints. Defaults to 2048.
        device (str, optional): The device to use. Defaults to 'cpu'.

    Raises:
        ValueError: If the feature extractor or the matcher are not valid
        ValueError: If the device is not valid

    Returns:
        tuple: The feature extractor and the matcher models
    """

    # Local feature extractor
    if features == "superpoint":
        extractor = SuperPoint(max_num_keypoints=max_num_keypoints).eval().to(device)
    elif features == "disk":
        extractor = DISK(max_num_keypoints=max_num_keypoints).eval().to(device)
    else:
        raise ValueError(f"Unknown feature extractor {features}")

    # Local feature matcher
    if matcher == "lightglue":
        matcher = LightGlue(features=features).eval().to(device)
    else:
        raise ValueError(f"Unknown matcher {matcher}")

    return extractor, matcher


def spatial_error(
        x: torch.Tensor,
        y: torch.Tensor,
        model: tuple,
        n_points: int = 10,
        threshold_distance: float = 10**4,
        hmatch: bool = True,
):
    """ Returns the spatial error between two images

    Args:
        x (torch.Tensor): Tensor of shape (C, H, W)
        y (torch.Tensor): Tensor of shape (C, H, W)
        model (tuple): Tuple of (model, extractor)
        n_points (int, optional): The number of points to be used 
          for the spatial model. Defaults to 10.
        threshold_distance (float, optional): The threshold distance
          for the spatial model. Defaults to 10**4.

    Returns:
        float: The spatial error
    """

    # check image must be RGB
    if x.shape[0] != 3 or y.shape[0] != 3:
        raise ValueError("Image must be RGB")

    if hmatch:
        x = hq_histogram_matching(x, y)

        # Check device
        with torch.no_grad():
          model_device = next(model[0].parameters()).device
        
        # Convert to tensor
        x = x.clone().detach().to(model_device).to(torch.float32)
        y = y.clone().detach().to(model_device).to(torch.float32)

        # Obtain matching points
        matching_points = spatial_get_matching_points(
            img01=x,
            img02=y,
            model=model,
            spectral_reducer_method="luminosity",
            rgb_bands=[0, 1, 2],
        )

        # Spatial offset at pixel level
        spatial_offset = spatial_model_fit(
            matching_points=matching_points,
            n_points = n_points,
            threshold_distance = threshold_distance,
            verbose = True,
        )

    return spatial_offset


def spatial_affine_correction(
  x: torch.Tensor,
  y: torch.Tensor,
  model: tuple,
  summary: dict,
) -> torch.Tensor:
    """Shift affine correction

    Args:
        x (torch.Tensor): Tensor of shape (C, H, W)
        y (torch.Tensor): Tensor of shape (C, H, W)
        model (tuple): Tuple of (model, extractor)
        **kwargs: Keyword arguments for spatial_error

    Raises:
        ValueError: Scale factor must be integer

    Returns:
        torch.Tensor: Tensor of shape (C, H, W)
    """

    # Get the affine transformation and error
    offset = summary["offset"]

    # Get the scale factor
    scale_factor = y.shape[1] / x.shape[1]
    if scale_factor % 1 != 0:
        raise ValueError("Scale factor must be integer")

    # Apply the affine transformation
    spatial_offset = [int(x*scale_factor) for x in offset]

    # Spatial transform at subpixel level
    new_image = spatial_model_transform(
        lr_to_hr=x,
        hr=y,
        spatial_offset={"offset": spatial_offset},
    )

    return new_image