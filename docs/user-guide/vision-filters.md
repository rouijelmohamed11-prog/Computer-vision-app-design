# Full Vision Filter Reference

VisionStudioAI includes a comprehensive set of Computer Vision filters powered by OpenCV.

## Basic Image Processing

| Filter | Description | Use Case |
| :--- | :--- | :--- |
| **Grayscale** | Removes all color information. | Artistic look, neutral backgrounds. |
| **Blur** | Applies a Gaussian blur (5x5 kernel). | Softening backgrounds to make text pop. |
| **Sharpen** | Enhances edges using a 2D convolution kernel. | Clarifying blurry photos. |
| **Edges** | Uses the Canny algorithm to find outlines. | Technical or blueprint styles. |

## Advanced AI Features

### 1. Smart Background Removal
This tool first attempts to use a cloud-based AI API for perfect results. If no API key is present or the connection fails, it falls back to a **Local GrabCut** implementation.
*   **Local Logic**: Uses an iterative segmentation algorithm followed by **Gaussian Feathering** to smooth the edges of the subject.

### 2. Saliency-Based Smart Crop
Unlike a standard center crop, this tool identifies the "Saliency Map" (the most interesting part) of an image and crops the square around that focal point.

### 3. Face Detection
Uses the Haar Cascade classifier to identify faces. Once detected, it can automatically focus the design or apply specific portrait filters.

### 4. Palette Extraction (K-Means)
The AI quantizes the colors in the image and identifies the 5 most dominant ones. These are then loaded into your **Styles** panel so you can use them for shapes and text.

## Real-time Adjustments

You can fine-tune these parameters via sliders:
*   **Brightness**: Scale the intensity of the image.
*   **Contrast**: Adjust the difference between dark and light areas.
*   **Saturation**: Increase or decrease the vividness of colors.
