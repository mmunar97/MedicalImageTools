import numpy

from typing import Tuple
from PIL import Image


def isocontour_segment_image(image: numpy.ndarray, upper_threshold: int,
                             lower_threshold) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """
    Detects the isocontour.

    Args:
        image: The original image, represented as a numpy array.
        threshold: An integer, representing the threshold for the image.

    Returns:
        A tuple of two images.
    """
    mask = (image >= lower_threshold) & (image <= upper_threshold)

    return mask, compute_printed_mask(image, mask)


def compute_printed_mask(image: numpy.ndarray, mask: numpy.ndarray) -> numpy.ndarray:
    """
    Writes each pixel marked in the mask into the original image.

    Args:
        image: The original image, represented as a numpy array.
        mask: The mask that contains the marked pixels, represented as a numpy array.

    Returns:
        An image, representing the modified original image.
    """
    original_image = Image.fromarray(image)

    color_image = Image.new("RGB", original_image.size)
    color_image.paste(original_image)

    temp_mask = numpy.transpose(mask)

    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if temp_mask[i, j]:
                color_image.putpixel((i, j), (20, 40, 80))

    return numpy.array(color_image)
