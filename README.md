# University Python Course Projects

This repository contains a collection of projects developed during a university Python course. Each project explores different aspects of data processing, analysis, and computer vision, demonstrating a range of techniques and tools used in modern software development.

## Project Overviews

### 1. ORB Detector (orb_detector)

The ORB Detector project implements the ORB (Oriented FAST and Rotated BRIEF) feature detection algorithm, which is commonly used in computer vision for identifying and describing keypoints in images. This project focuses on:

- **Keypoint Detection**: Using the FAST algorithm to find distinctive features in images.
- **Harris Corner Measure**: Filtering keypoints based on their cornerness measure.
- **Image Pyramid Creation**: Detecting features at multiple scales to handle different image resolutions.

**Directory Structure:**
- `img/`: Contains image files used in the project.
- `reference_out/`: Stores reference output files.
- `test_images/`: Includes images used for testing.
- `tests/`: Contains test scripts for validating the ORB feature detector implementation.

### 2. Titanic Survival Analysis (titanic_death_analysis)

The Titanic Survival Analysis project involves exploring the Titanic dataset to understand passenger demographics, survival rates, and other characteristics. The project aims to analyze various factors that influenced survival during the disaster.

- **Data Processing**: Functions for loading, cleaning, and preprocessing the data.
- **Statistical Analysis**: Includes correlation analysis, outlier detection, and survival rate computations.
- **Feature Engineering**: Creation of new features for enhanced analysis.

**Directory Structure:**
- `data/`: Contains datasets and related encrypted/signature files.
- `tests/`: Includes test scripts to validate data processing functions.

### 3. Image Filtering Project

This project focuses on implementing image filtering techniques using convolution with various kernels. It supports both grayscale and RGB images, allowing for manual application of filters such as Gaussian blur and edge detection.

- **Convolution Operations**: Implementing 2D convolution for image processing.
- **Filter Application**: Applying different kernels to images to achieve various effects.
- **Manual Implementation**: Aimed at understanding the basics of convolution without advanced libraries.

**Directory Structure:**
- `filtering.py`: Contains core functions for image filtering.
- `test_filtering.py`: Includes tests for validating the image filtering functions.
- `demo.ipynb`: A Jupyter Notebook demonstrating the application of filters.

### 4. Bomberman-Inspired Game

The Bomberman-Inspired Game is developed using Python and the Pygame library. It features both single-player and multiplayer modes, offering a grid-based layout where players navigate through various obstacles, enemies, and destructible blocks. The objective is to strategically place bombs to eliminate enemies and clear paths through maze-like levels.

- **Multiplayer Mode**: Allows two players to compete by navigating the grid, planting bombs, and outmaneuvering each other.
- **Map Selection and Variations**: Includes different maps and supports custom map loading to enhance gameplay variety.
- **Enhanced AI**: Implements Depth-First Search (DFS) and Dijkstra's algorithms for smarter enemy behavior.

**Directory Structure:**
- `src/`: Contains the main game source code.
- `assets/`: Includes game assets like images and sounds.
- `tests/`: Holds test scripts for various game functionalities.

## Purpose and Context

These projects were developed as part of a university Python course, designed to introduce students to practical applications of Python in data analysis and computer vision. Each project emphasizes a different aspect of Python programming, from data preprocessing and statistical analysis to image processing and feature detection.

## How to Navigate the Repository

- Each project is organized into its own directory, containing all necessary scripts, data, and documentation.
- The README.md files within each directory provide detailed explanations and usage instructions for the specific project.


---

For more detailed information on each project, please refer to the README.md files located within their respective directories.
