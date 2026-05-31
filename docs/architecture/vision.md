# Vision Pipeline

The Vision Pipeline handles all heavy-duty image processing using the OpenCV library.

## Processing Workflow

When a filter or adjustment is applied in the UI:
1.  The `ImageElement` provides its raw image data.
2.  The data is converted into a NumPy array (BGR format).
3.  The relevant function in `vision/filters.py` or `vision/image_tools.py` is called.
4.  The processed array is converted back into a `QPixmap` for rendering on the canvas.

## Key Features

### Threaded Processing
To keep the UI responsive, heavy operations like "Background Removal" or "Face Detection" are executed in a separate `FilterWorker` thread. This prevents the application from freezing during complex calculations.

### Palette Extraction Algorithm
The palette extraction tool uses K-Means clustering (via OpenCV) to find the most dominant colors in an image. It then filters these colors to ensure a diverse and aesthetically pleasing palette is returned to the user.

### Smart Cropping
Uses edge detection and saliency mapping to identify the "center of interest" in an image, allowing for automated crops that don't cut off important subjects.
