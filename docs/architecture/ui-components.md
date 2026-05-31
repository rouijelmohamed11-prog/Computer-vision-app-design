# UI Component Architecture

The VisionStudioAI interface is built using PyQt5, following a modular component-based approach.

## 1. The Design Canvas (`ui/canvas.py`)

The `DesignCanvas` is a custom widget where all the rendering happens.

### Coordinate Systems
The canvas uses two coordinate systems:
*   **Widget Coordinates**: Local pixels of the PyQt widget.
*   **Canvas Coordinates**: Logical coordinates of the design (e.g., 0 to 5000).

The canvas handles the translation between these using a `QTransform`, allowing for smooth **Panning** and **Zooming**.

### Rendering Loop
The canvas uses the `QPainter` API to render elements in their Z-order. It utilizes:
*   **Antialiasing**: For smooth edges on text and shapes.
*   **Smooth Pixmap Transform**: To keep images looking crisp even when scaled.

## 2. Property Panel (`ui/properties.py`)

The **Inspector** on the right side of the screen is the `PropertyPanel`. It is dynamic and changes based on what is selected.

### Dynamic Sections
*   **Transform**: Always visible for x, y, width, height, and rotation.
*   **Text Section**: Appears only when a `TextElement` is selected.
*   **Image Section**: Appears for `ImageElement`, providing access to the **Vision Pipeline**.

## 3. Layers Panel (`ui/layers.py`)

The `LayersPanel` provides a vertical list of all elements on the canvas.
*   **Visibility**: Toggle elements on and off.
*   **Ordering**: Drag and drop (or use buttons) to change which elements appear on top.

## 4. Toolbar (`ui/toolbar.py`)

The toolbar provides quick access to creation tools:
*   **Selector**: Default tool for moving and resizing.
*   **Text Tool**: Click to add new typography.
*   **Shape Tools**: Add rectangles, circles, and lines.
*   **Import**: Open a file dialog to add local images.

## 5. Styling Engine (`ui/styles.py`)

The application's "Dark Modern" look is defined via **QSS (Qt Style Sheets)**. The `GLOBAL_STYLE` variable contains the CSS-like definitions for colors, borders, and effects, ensuring a consistent design language across all windows and dialogs.
