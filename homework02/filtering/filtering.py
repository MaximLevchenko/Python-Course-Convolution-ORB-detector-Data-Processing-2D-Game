"""
Module Description: This module contains functions for image filtering.
"""
import numpy as np
# import cv2
# from PIL import Image


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
    padded_img = np.zeros((image.shape[0]+padding_height, image.shape[1]+padding_width))
    padded_img[pad_up:pad_up+image.shape[0], pad_left:pad_left+image.shape[1]] = image
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
    if sum_convolve > 255:
        sum_convolve = 255
    elif sum_convolve < 0:
        sum_convolve = 0
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
        padded_image = pad_image(image.copy(), kernel.shape[0])
        convolved = np.zeros((image_height, image_width), dtype=image.dtype)

        for i in range(image_height):
            for j in range(image_width):
                # tmp = padded_image[i:i + kernel.shape[0], j:j + kernel.shape[0]]
                # tmp_kernel = tmp * kernel.sum()
                convolved[i, j] = calculate_sum(padded_image[i:i + kernel.shape[0], j:j + kernel.shape[0]], kernel)

    elif image.ndim == 3:  # RGB image
        channels = [apply_filter(image[:, :, c], kernel) for c in range(image.shape[2])]
        array_after_convolve = np.dstack(channels)
        return array_after_convolve
        # print(array_after_convolve)
    else:
        raise ValueError("Input dimensions are not valid for convolution.")
    return convolved


if __name__ == '__main__':
    print('')
    # image = cv2.imread('../tests/lenna.png')
    # image_np = np.array(image)
    # image_should_be_three_d = np.asarray(Image.open('../tests/lenna.png'), dtype=np.uint8)
    # image_should_be_two_d = np.average(image_should_be_three_d.astype(float), weights=[0.299, 0.587, 0.114],
    #                                    axis=2).astype(np.uint8)
    # image_main = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255]],
    #                        [[128, 128, 128], [64, 64, 64], [192, 192, 192]],
    #                        [[255, 255, 255], [0, 0, 0], [128, 128, 128]]])
    # kernel_main = np.array([
    #     [-1, -1, -1],
    #     [-1, 8, -1],
    #     [-1, -1, -1]]
    # )
    # kernel_main = np.array([
    #     [2, 0],
    #     [1, 0]], dtype=np.uint8)
    #
    # result = apply_filter(image_should_be_two_d, kernel_main)
