# Image Filtering Project

This project implements image filtering using convolution with various kernels. The filtering supports both grayscale and RGB images, applying filters independently to each channel for RGB images. The primary goal is to understand and implement the convolution operation manually, without relying on advanced libraries like SciPy.

## Files and Directories

- **filtering.py**: This module contains functions for image filtering, including:
  - `pad_image`: Pads the input image with zeros based on the kernel size.
  - `calculate_sum`: Computes the sum of element-wise multiplication of a kernel and a segment of the image.
  - `apply_filter`: Applies the convolution filter to the input image.

- **tests/test_filtering.py**: Contains test cases for the image filtering functions using `pytest`, including:
  - Identity filter
  - Gaussian blur
  - Edge detection
  - Roberts cross operator

- **demo.ipynb**: A Jupyter Notebook demonstrating the application of various filters on sample images.

## Project Overview

The goal of this project is to manually implement 2D convolution for image processing, supporting various image types and kernels. The project demonstrates an understanding of fundamental image processing techniques and the efficient use of NumPy for array manipulation.

## Key Features

- **Grayscale and RGB Support**: Handles both grayscale and RGB images by applying the filter to each channel independently.
- **Zero Padding**: Ensures the output image size matches the input image size by adding zeros around the borders of the image.
- **Custom Kernels**: Allows the use of different kernel sizes and types, such as identity, Gaussian blur, edge detection, and Roberts cross.

## Usage

To apply a filter, you need to load the image, define the kernel, and call the `apply_filter` function:

```python
import numpy as np
from filtering import apply_filter

# Example usage for a grayscale image
image = np.array([...])  # Load your image as a numpy array
kernel = np.array([...])  # Define your kernel
filtered_image = apply_filter(image, kernel)
```
