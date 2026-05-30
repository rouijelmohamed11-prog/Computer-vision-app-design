import cv2
import numpy as np

def resize_image(image_np, width, height):
    return cv2.resize(image_np, (width, height), interpolation=cv2.INTER_AREA)

def crop_image(image_np, x, y, w, h):
    return image_np[y:y+h, x:x+w]

def blend_images(base_np, overlay_np, alpha=0.5):
    """Blends overlay into base with alpha."""
    # Ensure same size
    overlay_res = cv2.resize(overlay_np, (base_np.shape[1], base_np.shape[0]))
    return cv2.addWeighted(base_np, 1 - alpha, overlay_res, alpha, 0)
