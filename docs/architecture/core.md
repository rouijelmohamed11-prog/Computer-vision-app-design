# Core Engine

The Core Engine is the central state manager for the VisionStudioAI application.

## DesignEngine

The `DesignEngine` class (found in `core/engine.py`) is responsible for:
- Maintaining the list of all `CanvasElement` objects.
- Handling the selection state (single and multi-select).
- Managing the Z-index of elements to ensure correct rendering order.
- Emitting signals when the state changes so the UI can update.

### Key Methods

- `add_element(element)`: Appends a new element and sorts by Z-index.
- `remove_element(element)`: Removes an element and cleans up selection.
- `select_element(element, multi=False)`: Updates the current selection.
- `move_element_up/down()`: Adjusts the layering of elements.

## Canvas Objects

All elements on the canvas inherit from a base `CanvasElement` class in `core/objects.py`. This ensures a consistent interface for the engine and the renderer.

### Element Types
- `TextElement`: Stores text, font size, color, and font family.
- `ImageElement`: Stores the path to the original image and a cached pixmap for fast rendering.
- `ShapeElement`: Defines geometric properties and fill colors.

## History Management

The `HistoryManager` (`core/history.py`) tracks every change made to the `DesignEngine`. It saves snapshots of the engine's state, allowing users to undo and redo actions seamlessly.
