import cv2
import numpy as np
from PIL import Image, ImageEnhance

def apply_grayscale(image_np):
    return cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

def apply_blur(image_np, ksize=5):
    return cv2.GaussianBlur(image_np, (ksize, ksize), 0)

def apply_sharpen(image_np):
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    return cv2.filter2D(image_np, -1, kernel)

def apply_edges(image_np):
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 100, 200)

def apply_brightness(image_np, factor):
    # factor 1.0 is original
    img = Image.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def apply_contrast(image_np, factor):
    # factor 1.0 is original
    img = Image.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def apply_saturation(image_np, factor):
    img = Image.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def detect_faces(image_np):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(image_np, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(image_np, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
    return image_np

def extract_color_palette(image_np, num_colors=5):
    # Resize for speed
    img = cv2.resize(image_np, (100, 100), interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img.reshape(-1, 3)
    
    # Use simple K-Means or just top frequent colors
    # For a quick "AI-feel", we'll use a simple top-N approach after quantization
    from collections import Counter
    # Quantize
    pixels = (pixels // 32) * 32
    counts = Counter(map(tuple, pixels))
    top_colors = counts.most_common(num_colors)
    return [tuple(map(int, color)) for color, count in top_colors]

import requests

# API Key for remove.bg
REMOVE_BG_API_KEY = "6LNBxuegakBdQgpP6YffDZs4"

def apply_remove_background(image_np):
    """
    Attempts to remove background using remove.bg API.
    Falls back to a local GrabCut implementation with edge smoothing.
    """
    # 1. Try API first for high quality
    if REMOVE_BG_API_KEY and REMOVE_BG_API_KEY != "YOUR_API_KEY":
        try:
            print("Attempting AI Background Removal (API)...")
            is_success, buffer = cv2.imencode(".png", image_np)
            if is_success:
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': buffer.tobytes()},
                    data={'size': 'auto'},
                    headers={'X-Api-Key': REMOVE_BG_API_KEY},
                    timeout=7 # Faster fallback
                )
                if response.status_code == requests.codes.ok:
                    nparr = np.frombuffer(response.content, np.uint8)
                    res_img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
                    if res_img is not None:
                        print("AI removal successful.")
                        return res_img
        except Exception as e:
            print(f"AI removal failed ({e}), falling back to local model.")

    # 2. Local Fallback (Improved GrabCut with Smoothing)
    print("Using local background removal (GrabCut + Smoothing)...")
    try:
        h, w = image_np.shape[:2]
        mask = np.zeros((h, w), np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        
        # Heuristic: Start with a slightly larger inner rectangle
        rect = (int(w*0.02), int(h*0.02), int(w*0.96), int(h*0.96))
        
        # Iterative GrabCut
        cv2.grabCut(image_np, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        
        # Post-process mask: 0 and 2 are background, 1 and 3 are foreground
        mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
        
        # Edge Smoothing (Feathering)
        mask_float = mask2.astype(float) * 255
        smooth_mask = cv2.GaussianBlur(mask_float, (7, 7), 0)
        
        # Add alpha channel
        res_img = cv2.cvtColor(image_np, cv2.COLOR_BGR2BGRA)
        res_img[:, :, 3] = smooth_mask.astype(np.uint8)
        
        print("Smooth local removal complete.")
        return res_img
    except Exception as e:
        print(f"Local removal failed: {e}")
        return cv2.cvtColor(image_np, cv2.COLOR_BGR2BGRA)

def apply_threshold(image_np):
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

def apply_stroke(image_np):
    # Edge detection based stroke
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    # Dilate edges to make them thicker
    kernel = np.ones((2, 2), np.uint8)
    stroke = cv2.dilate(edges, kernel, iterations=1)
    # Combine original with stroke
    mask = stroke > 0
    image_np[mask] = [0, 0, 0] # Make edges black
    return image_np

def center_crop(image_np):
    """Crops the image to a square centered on the middle of the image."""
    h, w = image_np.shape[:2]
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    return image_np[start_y:start_y+min_dim, start_x:start_x+min_dim]
