# Image Search Engine

## Overview

The Image Search Engine is a desktop application that allows users to search for images within a selected directory based on a given search phrase. It uses OpenAI's CLIP model for semantic search and PyQt6 for the graphical user interface.

![App Screenshot](screenshots/ImageSearchEngineSS.png)

## Features

- Select a directory containing images.
- Enter a search phrase to find relevant images.
- Displays the top N matching images with thumbnails.
- Adjustable number of search results via settings.
- Supports various image formats: PNG, JPG, JPEG, GIF, BMP.

## Installation

### Prerequisites

- Python 3.8+
- `pip` (Python package installer)

### Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

## Usage
1. **Selecting Directory:** Click on the "Browse" button to select a directory containing images.
2. **Entering Search Phrase:** Enter a search phrase in the provided input box.
3. **Searching:** Click on the "Search" button to find the top matching images.
4. **Adjusting Settings:** Click on the "Settings" button to adjust the number of results displayed. If you have a CUDA enabled GPU, you can toggle the use of it on or off (on by default).
5. **Finding a file in file manager:** For Mac OS and Windows, left click to open the file manager on your device and jump to the file.
for other OSs, right click and select "Copy" to copy the path from the results list.

## Tests

**Number of Images:** 100 - 1920x1080

### CPU

**Testing Specs:** Intel Core i5 3570 3.4Ghz

**Processing Time:** 11.62 Seconds

### GPU

**Testing Specs:** NVIDIA GeForce GTX 1050 Ti 4GB VRAM

**Processing Time:** 6.80 Seconds


## Acknowledgments
[openai / CLIP](https://github.com/openai/CLIP.git)