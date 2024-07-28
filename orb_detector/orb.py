"""
Module Description: This module contains functions for math.
"""

import math
from typing import List
from typing import Tuple
import cv2
import numpy as np

from orb_detector.utils import apply_gaussian_2d

PER_GROUP_COUNT = 9
MAX_PIXEL_VALUE = 255
FAST_CIRCLE_RADIUS = 3
FAST_ROW_OFFSETS = [-3, -3, -2, -1, 0, 1, 2, 3, 3, 3, 2, 1, 0, -1, -2, -3]
FAST_COL_OFFSETS = [0, 1, 2, 3, 3, 3, 2, 1, 0, -1, -2, -3, -3, -3, -2, -1]
FAST_FIRST_TEST_INDICES = [0, 4, 8, 12]
FAST_FIRST_TEST_THRESHOLD = 3
FAST_SECOND_TEST_THRESHOLD = 12


def create_pyramid(
        img_pyr: np.ndarray, n_pyr_layers: int, downscale_factor: float = 1.2
) -> List[np.ndarray]:
    """
    Creates multi-scale image pyramid.

    Parameters
    ----------
    img_pyr : np.ndarray
        Gray-scaled input image.
    n_pyr_layers : int
        Number of layers in the pyramid.
    downscale_factor: float
        Downscaling performed between successive pyramid layers.

    Returns
    -------
    pyr : List[np.ndarray]
        Pyramid of scaled images.
    """
    pyramid = [img_pyr]
    for _ in range(1, n_pyr_layers):
        # Calculate the size for the next level of the pyramid
        height, width = img_pyr.shape[:2]
        new_height = math.ceil(height / downscale_factor)
        new_width = math.ceil(width / downscale_factor)

        # Resize the image to the calculated size
        img_pyr = cv2.resize(img_pyr, (new_width, new_height))

        # Add the resized image to the pyramid
        pyramid.append(img_pyr)

    return pyramid


# not necessary to implement, see README
def get_first_test_mask(
        img_level: np.ndarray, threshold: int, border: int
) -> np.ndarray:
    """
    Returns the mask from the first FAST test (FAST_FIRST_TEST_INDICES).

    Parameters
    ----------
    img_level : np.ndarray
        Image at the given level of the image pyramid.
    threshold : int
        Intensity by which tested pixel should differ from the pixels on its Bresenham circle.
    border: int
        Number of rows/columns at the image border where no keypoints should be reported.

    Returns
    -------
    mask : np.ndarray
        Boolean mask with True values at pixels which pass the first FAST test.
    """
    img_level = img_level.astype(int)
    mask = np.zeros((img_level.shape[0], img_level.shape[1]))
    for row in range(border, img_level.shape[0] - border, 1):
        for col in range(border, img_level.shape[1] - border, 1):  # here we get a specific center pixel
            lighter_intensity_count, darker_intensity_count = 0, 0
            for i in FAST_FIRST_TEST_INDICES:  # going through first test indices
                center_pixel = img_level[row][col]
                pixel_cmp_center_to = img_level[row + FAST_ROW_OFFSETS[i]][col + FAST_COL_OFFSETS[i]]
                if center_pixel < pixel_cmp_center_to - threshold:
                    darker_intensity_count += 1
                elif center_pixel > pixel_cmp_center_to + threshold:
                    lighter_intensity_count += 1
            if lighter_intensity_count >= FAST_FIRST_TEST_THRESHOLD or darker_intensity_count >= FAST_FIRST_TEST_THRESHOLD:
                mask[row][col] = 1
    return mask


# not necessary to implement, see README
def get_second_test_mask(
        img_level: np.ndarray,
        first_test_mask: np.ndarray,
        threshold: int,
) -> np.ndarray:
    """
    Returns the mask from the second FAST test (FAST_FIRST_TEST_INDICES).
    HINT: test only at those points which already passed the first test (first_test_mask).

    Parameters
    ----------
    img_level : np.ndarray
        Image at the given level of the image pyramid.
    first_test_mask: np.ndarray
        Boolean mask for the first test, which was created by get_first_test_mask().
    threshold : int
        Intensity by which tested pixel should differ from the pixels on its Bresenham circle.

    Returns
    -------
    mask : np.ndarray
        Boolean mask with True values at pixels which pass the second FAST test.
    """
    img_level = img_level.astype(int)
    mask = np.zeros((img_level.shape[0], img_level.shape[1]))
    for row in range(first_test_mask.shape[0]):
        for col in range(first_test_mask.shape[1]):  # here we get a specific center pixel
            if first_test_mask[row][col] != 1:
                continue

            lighter_intensity_count, darker_intensity_count = 0, 0
            for i, j in zip(FAST_ROW_OFFSETS, FAST_COL_OFFSETS):  # going through first test indices
                center_pixel = img_level[row][col]
                pixel_cmp_center_to = img_level[row + i][col + j]
                if center_pixel < pixel_cmp_center_to - threshold:
                    darker_intensity_count += 1
                elif center_pixel > pixel_cmp_center_to + threshold:
                    lighter_intensity_count += 1
            if lighter_intensity_count >= FAST_SECOND_TEST_THRESHOLD or darker_intensity_count >= FAST_SECOND_TEST_THRESHOLD:
                mask[row][col] = 1
            else:
                mask[row][col] = 0
    return mask


def calculate_kp_scores(
        img_level: np.ndarray,
        keypoints: List[Tuple[int, int]],
) -> List[int]:
    """
    Calculates FAST score for initial keypoints.

    Parameters
    ----------
    img_level : np.ndarray
        Image at the given level of the image pyramid.
    keypoints: List[Tuple[int, int]]
        Tentative keypoints detected by FAST algorithm.

    Returns
    -------
    scores : List[int]
        Scores for the tentative keypoints.
    """
    img_level = img_level.astype(int)
    scores = []
    for keypoint_row, keypoint_col in keypoints:  # iterating through all key points
        array_groups_lowest_diffs = []  # array for storing the lowest values of groups for the keypoint
        center_pixel = img_level[keypoint_row][keypoint_col]
        for group_offset in range(len(FAST_COL_OFFSETS)):  # iterating through all 16 groups we can get in an array
            group_lowest_diff = MAX_PIXEL_VALUE
            offset_row_arr = np.roll(FAST_ROW_OFFSETS, group_offset)
            offset_col_arr = np.roll(FAST_COL_OFFSETS, group_offset)
            for i in range(PER_GROUP_COUNT):  # iterating though 9 elements which create a group
                current_pixel_cmp_to = img_level[keypoint_row + offset_row_arr[i]][keypoint_col + offset_col_arr[i]]
                if np.abs(center_pixel - current_pixel_cmp_to) < group_lowest_diff:
                    group_lowest_diff = np.abs(center_pixel - current_pixel_cmp_to)
            array_groups_lowest_diffs.append(group_lowest_diff)
        scores.append(int(max(array_groups_lowest_diffs)))
    return scores


def detect_keypoints(
        img_level: np.ndarray,
        threshold: int,
        border: int = 0,
) -> Tuple[List[Tuple[int, int]], List[int]]:
    """
    Creates the initial keypoints list.

    Scans the image at the given pyramid level and detects the unfiltered FAST keypoints,
    which are upscaled according to the current level index.

    Parameters
    ----------
    img_level : np.ndarray
        Image at the given level of the image pyramid.
    threshold : int
        Intensity by which tested pixel should differ from the pixels on its Bresenham circle.
    border: int
        Number of rows/columns at the image border where no keypoints should be reported.

    Returns
    -------
    keypoints : List[Tuple[int, int]]
        Initial FAST keypoints as tuples of (row_idx, col_idx).
    scores: List[int]
        Corresponding scores calculate with calculate_kp_scores().
    """
    border = max(border, FAST_CIRCLE_RADIUS)
    keypoints, scores = [], []
    first_test_mask = get_first_test_mask(img_level, threshold, border)
    second_test_mask = get_second_test_mask(img_level, first_test_mask, threshold)
    for row in range(second_test_mask.shape[0]):
        for col in range(second_test_mask.shape[1]):
            if second_test_mask[row][col] == 1:
                keypoints.append((row, col))
    scores = calculate_kp_scores(img_level, keypoints)
    return keypoints, scores


def pad_image(image: np.array, kernel_size: int) -> np.array:
    """
    This function performs zero padding using the number of
    padding layers supplied as argument and return the padded
    image.
    """
    padding_height = kernel_size - 1
    padding_width = kernel_size - 1
    pad_left = int(np.ceil(padding_width / 2))
    # pad_right = int(np.floor(padding_width / 2))
    pad_up = int(np.ceil(padding_height / 2))
    # pad_down = int(np.floor(padding_height / 2))
    padded_img = np.zeros((image.shape[0] + padding_height, image.shape[1] + padding_width))
    padded_img[pad_up:pad_up + image.shape[0], pad_left:pad_left + image.shape[1]] = image
    # padded_img = np.pad(image, [(pad_up, pad_down), (pad_left, pad_right)], mode='constant')
    return padded_img


def calculate_sum(image: np.array, kernel: np.array):
    """
        This function performs sum over an image and kernel.
        """
    sum_convolve = 0
    for i in range(image.shape[0]):  # height
        for j in range(image.shape[0]):  # width
            sum_convolve += image[i][j] * kernel[i][j]
    # if sum_convolve > 255:
    #     sum_convolve = 255
    # elif sum_convolve < 0:
    #     sum_convolve = 0
    return sum_convolve


def apply_filter(image: np.array, kernel: np.array) -> np.array:
    """
    This function performs convolution over an image.
    """
    # A given image has to have either 2 (grayscale) or 3 (RGB) dimensions
    assert image.ndim in [2, 3]
    # A given filter has to be 2-dimensional and square
    assert kernel.ndim == 2
    assert kernel.shape[0] == kernel.shape[1]

    if image.ndim == 2:  # Grayscale image
        image_height, image_width = image.shape
        # padded_image = pad_image(image.copy(), kernel.shape[0])
        padded_image = image.copy()
        convolved = np.zeros((image_height - 2, image_width - 2), dtype=image.dtype)

        for i in range(image_height - 2):
            for j in range(image_width - 2):
                convolved[i, j] = calculate_sum(padded_image[i:i + kernel.shape[0], j:j + kernel.shape[0]], kernel)
        convolved = pad_image(convolved.copy(), kernel.shape[0])
    else:
        raise ValueError("Input dimensions are not valid for convolution.")
    return convolved


def get_x_derivative(img_for_x: np.ndarray) -> np.ndarray:
    """
    Calculates x-derivative by applying separable Sobel filter.
    HINT: np.pad()

    Parameters
    ----------
    img_for_x : np.ndarray
        Gray-scaled input image.

    Returns
    -------
    result : np.ndarray
        X-derivative of the input image.
    """
    kernel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]]
    )
    img_for_x = img_for_x.astype(int)
    # convolved = convolve2d(img, kernel_x, mode='same', boundary='fill', fillvalue=0)

    result = apply_filter(img_for_x, kernel_x)
    return result


def get_y_derivative(img_for_y: np.ndarray) -> np.ndarray:
    """
    Calculates y-derivative by applying separable Sobel filter.
    HINT: np.pad()

    Parameters
    ----------
    img_for_y : np.ndarray
        Gray-scaled input image.

    Returns
    -------
    result : np.ndarray
        Y-derivative of the input image.
    """
    kernel_y = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]]
    )
    img_for_y = img_for_y.astype(int)
    result = apply_filter(img_for_y, kernel_y)
    return result


def get_harris_response(img_harris: np.ndarray) -> np.ndarray:
    """
    Calculates the Harris response.

    Calculates ixx, ixy and iyy from x and y-derivatives with Gaussian
    windowing (utils.apply_gaussian_2d(data=..., sigma=1.0). Then, uses the
    computed matrices to calculate the determinant and trace of the second-
    moment matrix. From it, calculates the final Harris response.

    Parameters
    ----------
    img_harris : np.ndarray
        Gray-scaled input image.

    Returns
    -------
    harris_response : np.ndarray
        Harris response of the input image.
    """
    dx, dy = get_x_derivative(img_harris), get_y_derivative(img_harris)
    dx, dy = dx.astype(float) / 255.0, dy.astype(float) / 255.0
    ixx = dx * dx
    ixy = dx * dy
    iyy = dy * dy
    ixx = apply_gaussian_2d(data=ixx, sigma=1.0)
    ixy = apply_gaussian_2d(data=ixy, sigma=1.0)
    iyy = apply_gaussian_2d(data=iyy, sigma=1.0)
    det = ixx * iyy - ixy * ixy
    trace = ixx + iyy
    trace_sqrt = trace * trace
    harris_response = det - 0.05 * trace_sqrt
    return harris_response


def filter_keypoints(
        img_filter: np.ndarray, keypoints: List[Tuple[int, int]], n_max_level: int
) -> List[Tuple[int, int]]:
    """
    Filters keypoints by Harris response.

    Iterates the detected keypoints for the given level. Sorts those keypoints
    by their Harris response in the descending order. Then, takes only the
    n_max_level top keypoints.

     Parameters
    ----------
    img_filter : np.ndarray
        Gray-scaled input image.
    keypoints : List[Tuple[int, int]]
        Initial FAST keypoints.
    n_max_level : int
        Maximal number of keypoints for a single pyramid level.

    Returns
    -------
    filtered_keypoints : List[Tuple[int, int]]
        Filtered FAST keypoints.
    """
    keypoints_and_harris = []

    harris_response = get_harris_response(img_filter)
    for keypoint in keypoints:
        keypoint_row, keypoint_col = keypoint
        keypoints_and_harris.append((keypoint, harris_response[keypoint_row][keypoint_col]))

    sorted_keypoints_harris = sorted(keypoints_and_harris, key=lambda x: x[1], reverse=True)
    filtered_keypoints = [keypoint[0] for keypoint in sorted_keypoints_harris[:n_max_level]]
    return filtered_keypoints


def fast(
        img_fast: np.ndarray,
        threshold: int = 20,
        n_pyr_levels: int = 8,
        downscale_factor: float = 1.2,
        n_max_features: int = 500,
        border: int = 0,
) -> List[List[Tuple[int, int]]]:
    """
    Applies the modified FAST detector.

    Parameters
    ----------
    img_fast : np.ndarray
        Gray-scaled input image.
    threshold: int
        Absolute intensity threshold for FAST detector.
    n_pyr_levels : int
        Number of layers in the image pyramid.
    downscale_factor: float
        Downscaling performed between successive pyramid layers.
    n_max_features : int
        Total maximal number of keypoints.
    """
    pyr = create_pyramid(img_fast, n_pyr_levels, downscale_factor)
    keypoints_pyr = []
    # Adapt Nmax for each level
    factor = 1.0 / downscale_factor
    n_max_level, n_sum_levels = [], 0
    n_per_level = n_max_features * (1 - factor) / (1 - factor ** n_pyr_levels)
    for level in range(n_pyr_levels):
        n_max_level.append(int(n_per_level))
        n_sum_levels += n_max_level[-1]
        n_per_level *= factor
    n_max_level[-1] = max(n_max_features - n_sum_levels, 0)
    for level, img_level in enumerate(pyr):
        keypoints, scores = detect_keypoints(img_level, threshold, border=border)
        idxs = np.argsort(scores)[::-1]
        keypoints = np.asarray(keypoints)[idxs][: 2 * n_max_level[level]].tolist()
        keypoints = filter_keypoints(img_level, keypoints, n_max_level[level])
        upscale_factor = downscale_factor ** level
        keypoints = [
            (int(x * upscale_factor), int(y * upscale_factor)) for (x, y) in keypoints
        ]
        keypoints_pyr.append(keypoints)
    return keypoints_pyr


if __name__ == '__main__':
    img = cv2.imread('tests/test_images/corners.jpg', cv2.IMREAD_GRAYSCALE)
    res,score = detect_keypoints(img, 20, 3)
    # result = get_x_derivative(img)
    # result2 = get_y_derivative(img)
    result3 = filter_keypoints(img,res, 3)
    # keypoints, scores = detect_keypoints(img, 20, border=20)
