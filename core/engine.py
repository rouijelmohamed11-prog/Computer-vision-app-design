from PyQt5.QtCore import QObject, pyqtSignal
from .objects import CanvasElement

class DesignEngine(QObject):
    elements_changed = pyqtSignal()
    selection_changed = pyqtSignal(list) # Emits the list of selected elements

    def __init__(self):
        super().__init__()
        self.elements = []
        self._selected_elements = []
        self.current_tool = None

    def add_element(self, element: CanvasElement):
        self.elements.append(element)
        element.changed.connect(self.elements_changed.emit)
        self.elements.sort(key=lambda x: x.z_index)
        self.elements_changed.emit()

    def remove_element(self, element: CanvasElement):
        if element in self.elements:
            self.elements.remove(element)
            if element in self._selected_elements:
                self._selected_elements.remove(element)
            self.elements_changed.emit()

    def select_element(self, element: CanvasElement, multi=False):
        if not multi:
            for el in self._selected_elements:
                el.selected = False
            self._selected_elements = []
        
        if element:
            if element not in self._selected_elements:
                element.selected = True
                self._selected_elements.append(element)
            elif multi:
                element.selected = False
                self._selected_elements.remove(element)
        
        self.selection_changed.emit(self._selected_elements)
        self.elements_changed.emit()

    @property
    def selected_element(self):
        # Return the primary (last selected) element for inspector
        return self._selected_elements[-1] if self._selected_elements else None

    @property
    def selected_elements(self):
        return self._selected_elements

    def clear_selection(self):
        for el in self._selected_elements:
            el.selected = False
        self._selected_elements = []
        self.selection_changed.emit([])
        self.elements_changed.emit()

    def move_element_up(self, element: CanvasElement):
        idx = self.elements.index(element)
        if idx < len(self.elements) - 1:
            self.elements[idx], self.elements[idx+1] = self.elements[idx+1], self.elements[idx]
            self.elements_changed.emit()

    def move_element_down(self, element: CanvasElement):
        idx = self.elements.index(element)
        if idx > 0:
            self.elements[idx], self.elements[idx-1] = self.elements[idx-1], self.elements[idx]
            self.elements_changed.emit()

    def bring_to_front(self, element: CanvasElement):
        if element in self.elements:
            self.elements.remove(element)
            self.elements.append(element)
            self.elements_changed.emit()

    def send_to_back(self, element: CanvasElement):
        if element in self.elements:
            self.elements.remove(element)
            self.elements.insert(0, element)
            self.elements_changed.emit()

    def delete_selected(self):
        for el in list(self._selected_elements):
            self.remove_element(el)
        self.clear_selection()

    def to_dict(self):
        # Convert elements to a list of dicts
        data = []
        for el in self.elements:
            el_data = {
                "type": el.__class__.__name__,
                "x": el.x,
                "y": el.y,
                "width": el.width,
                "height": el.height,
                "z_index": el.z_index,
                "visible": el.visible
            }
            if isinstance(el, TextElement):
                el_data.update({
                    "text": el.text,
                    "font_size": el.font_size,
                    "color": el.color.name()
                })
            elif isinstance(el, ShapeElement):
                el_data.update({
                    "shape_type": el.shape_type,
                    "color": el.color.name()
                })
            elif isinstance(el, ImageElement):
                el_data.update({
                    "image_path": el.image_path,
                    "opacity": el.opacity
                })
            elif isinstance(el, LineElement):
                el_data.update({
                    "color": el.color.name(),
                    "thickness": el.thickness
                })
            data.append(el_data)
        return data

    def from_dict(self, data):
        from PyQt5.QtGui import QColor, QPixmap
        from .objects import TextElement, ShapeElement, ImageElement, LineElement
        
        self.elements.clear()
        for el_data in data:
            el_type = el_data["type"]
            x, y = el_data["x"], el_data["y"]
            
            if el_type == "TextElement":
                el = TextElement(el_data["text"], x, y, el_data["font_size"], QColor(el_data["color"]))
            elif el_type == "ShapeElement":
                el = ShapeElement(el_data["shape_type"], x, y, QColor(el_data["color"]))
            elif el_type == "ImageElement":
                el = ImageElement(el_data["image_path"], x, y)
                el.opacity = el_data["opacity"]
                el.original_pixmap = QPixmap(el.image_path)
            elif el_type == "LineElement":
                el = LineElement(x, y, el_data["width"], el_data["height"], QColor(el_data["color"]), el_data["thickness"])
            
            if el_type != "LineElement": # Width/Height already set in constructor for Line
                el.width = el_data["width"]
                el.height = el_data["height"]
            el.z_index = el_data["z_index"]
            el.visible = el_data["visible"]
            self.add_element(el)
        
        self.elements_changed.emit()
