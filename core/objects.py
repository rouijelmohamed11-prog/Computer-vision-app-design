from PyQt5.QtCore import QObject, pyqtSignal, QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QColor, QImage, QFont
import uuid

class CanvasElement(QObject):
    changed = pyqtSignal()
    
    def __init__(self, x=0, y=0, width=100, height=100, z_index=0, parent=None):
        super().__init__()
        self.id = str(uuid.uuid4())
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._rotation = 0 # degrees
        self._opacity = 1.0
        self.z_index = z_index
        self.selected = False
        self.visible = True
        self.parent = parent
        self.name = self.__class__.__name__.replace('Element', '')

    @property
    def rotation(self): return self._rotation
    @rotation.setter
    def rotation(self, value):
        self._rotation = value % 360
        self.changed.emit()

    @property
    def opacity(self): return self._opacity
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.changed.emit()

    @property
    def x(self): 
        if self.parent: return self._x + self.parent.x
        return self._x
    @x.setter
    def x(self, value):
        if self.parent: self._x = value - self.parent.x
        else: self._x = value
        self.changed.emit()

    @property
    def y(self): 
        if self.parent: return self._y + self.parent.y
        return self._y
    @y.setter
    def y(self, value):
        if self.parent: self._y = value - self.parent.y
        else: self._y = value
        self.changed.emit()

    @property
    def width(self): return self._width
    @width.setter
    def width(self, value):
        self._width = value
        self.changed.emit()

    @property
    def height(self): return self._height
    @height.setter
    def height(self, value):
        self._height = value
        self.changed.emit()

    def get_rect(self):
        return QRect(int(self._x), int(self._y), int(self.width), int(self.height))

    def contains(self, point: QPoint):
        # We need to account for parent coordinates for hit testing
        # For simplicity, convert point to local coordinates
        local_point = point
        if self.parent:
            local_point = QPoint(point.x() - int(self.parent.x), point.y() - int(self.parent.y))
        return self.get_rect().contains(local_point)

    def clone(self):
        new_obj = CanvasElement(self._x, self._y, self.width, self.height, self.z_index, self.parent)
        new_obj.id = self.id
        new_obj.visible = self.visible
        new_obj.opacity = self.opacity
        return new_obj

class GroupElement(CanvasElement):
    def __init__(self, x=0, y=0, z_index=0):
        super().__init__(x, y, 0, 0, z_index)
        self.children = []

    def add_child(self, element):
        element.parent = self
        self.children.append(element)
        self.changed.emit()

    def get_rect(self):
        if not self.children: return QRect(int(self._x), int(self._y), 0, 0)
        # Calculate bounding box of all children
        rects = [el.get_rect() for el in self.children]
        x1 = min(r.left() for r in rects)
        y1 = min(r.top() for r in rects)
        x2 = max(r.right() for r in rects)
        y2 = max(r.bottom() for r in rects)
        return QRect(x1, y1, x2-x1, y2-y1)

    def clone(self):
        new_obj = GroupElement(self._x, self._y, self.z_index)
        new_obj.children = [child.clone() for child in self.children]
        for child in new_obj.children: child.parent = new_obj
        return new_obj

class TextElement(CanvasElement):
    def __init__(self, text="Text", x=0, y=0, font_size=20, color=QColor(0, 0, 0)):
        super().__init__(x, y, 200, 50)
        self._text = text
        self._font_size = font_size
        self._color = color
        self._font_family = "Arial"

    def clone(self):
        new_obj = TextElement(self.text, self.x, self.y, self.font_size, self.color)
        new_obj.id = self.id
        new_obj._font_family = self._font_family
        new_obj.opacity = self.opacity
        return new_obj

    @property
    def text(self): return self._text
    @text.setter
    def text(self, value):
        self._text = value
        self.changed.emit()

    @property
    def font_size(self): return self._font_size
    @font_size.setter
    def font_size(self, value):
        self._font_size = value
        self.changed.emit()

    @property
    def color(self): return self._color
    @color.setter
    def color(self, value):
        self._color = value
        self.changed.emit()

class ImageElement(CanvasElement):
    def __init__(self, image_path, x=0, y=0):
        super().__init__(x, y, 200, 200)
        self.image_path = image_path
        self.original_pixmap = None 
        self.base_pixmap = None # Stores state after filters, before live adjustments
        self._cached_pixmap = None # Performance cache
        self.opacity = 1.0
        self.filters = [] 

    @CanvasElement.width.setter
    def width(self, value):
        self._width = value
        self._cached_pixmap = None # Invalidate cache
        self.changed.emit()

    @CanvasElement.height.setter
    def height(self, value):
        self._height = value
        self._cached_pixmap = None # Invalidate cache
        self.changed.emit()

    def clone(self):
        new_obj = ImageElement(self.image_path, self.x, self.y)
        new_obj.id = self.id
        new_obj.width = self.width
        new_obj.height = self.height
        new_obj.opacity = self.opacity
        new_obj.filters = list(self.filters)
        new_obj.original_pixmap = self.original_pixmap
        new_obj.base_pixmap = self.base_pixmap
        return new_obj

class ShapeElement(CanvasElement):
    def __init__(self, shape_type="rectangle", x=0, y=0, color=QColor(200, 200, 200)):
        super().__init__(x, y, 100, 100)
        self.shape_type = shape_type 
        self._color = color

    def clone(self):
        new_obj = ShapeElement(self.shape_type, self.x, self.y, self.color)
        new_obj.id = self.id
        new_obj.width = self.width
        new_obj.height = self.height
        new_obj.opacity = self.opacity
        return new_obj

    @property
    def color(self): return self._color
    @color.setter
    def color(self, value):
        self._color = value
        self.changed.emit()

class LineElement(CanvasElement):
    def __init__(self, x1=0, y1=0, x2=100, y2=100, color=QColor(0, 0, 0), thickness=2):
        # For Line, we use x,y as start and width,height as end relative offset or absolute?
        # Let's use x,y as start and width,height to store absolute end point for simplicity in serialization
        super().__init__(x1, y1, x2, y2)
        self._color = color
        self._thickness = thickness

    def get_rect(self):
        # For selection purposes, return a rect that contains the line
        return QRect(int(min(self.x, self.width)), int(min(self.y, self.height)), 
                     int(abs(self.x - self.width) + 5), int(abs(self.y - self.height) + 5))

    def clone(self):
        new_obj = LineElement(self.x, self.y, self.width, self.height, self.color, self.thickness)
        new_obj.id = self.id
        new_obj.opacity = self.opacity
        return new_obj

    @property
    def color(self): return self._color
    @color.setter
    def color(self, value):
        self._color = value
        self.changed.emit()

    @property
    def thickness(self): return self._thickness
    @thickness.setter
    def thickness(self, value):
        self._thickness = value
        self.changed.emit()
