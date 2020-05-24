import cv2
import numpy

from typing import Tuple


def watershed_segment_image(image: numpy.ndarray, threshold: int) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """
    Segments the image using the watershed method.

    This code has been adapted from the openCV official documentation:
        https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html

    Args:
        image: An image, represented as a numpy array.
        threshold: An integer, representing the threshold for the image.

    Returns:
        A tuple of two images.
    """
    norm_image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    norm_image = norm_image.astype(numpy.uint8)

    color_image = cv2.cvtColor(norm_image, cv2.COLOR_GRAY2RGB)

    _, thresh = cv2.threshold(norm_image, threshold, 255, cv2.THRESH_BINARY)

    kernel = numpy.ones((3, 3), numpy.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    sure_fg = numpy.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    markers = cv2.watershed(color_image, markers)

    color_image[markers == -1] = [255, 0, 0]

    return color_image, None
