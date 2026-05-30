from PyQt5.QtWidgets import QWidget, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap, QTransform
from core.objects import TextElement, ImageElement, ShapeElement, LineElement
import math

class DesignCanvas(QWidget):
    file_dropped = pyqtSignal(str, QPoint)
    zoom_changed = pyqtSignal(float)

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        
        # View State
        self.scale = 1.0
        self.pan_offset = QPoint(0, 0)
        self.last_mouse_pos = QPoint()
        self.space_pressed = False
        
        # Interaction State
        self.drag_elements = []
        self.drag_offsets = {}
        self.resize_element = None
        self.rotate_element = None
        self.resize_handle = None # 'tl', 'tr', 'bl', 'br'
        self.handle_size = 10
        self.grid_size = 10
        self.brush_active = False
        
        # Canvas pixmap for brush (fixed size for now)
        self.canvas_pixmap = QPixmap(5000, 5000)
        self.canvas_pixmap.fill(Qt.transparent)

        self.engine.elements_changed.connect(self.update)

    def transform_point(self, pos):
        """Map widget coordinates to canvas coordinates"""
        return (QPointF(pos) - QPointF(self.pan_offset)) / self.scale

    def inverse_transform_point(self, pos):
        """Map canvas coordinates to widget coordinates"""
        return QPointF(pos) * self.scale + QPointF(self.pan_offset)

    def get_element_transform(self, el):
        t = QTransform()
        rect = el.get_rect()
        center = rect.center()
        t.translate(center.x(), center.y())
        t.rotate(el.rotation)
        t.translate(-center.x(), -center.y())
        return t

    def get_handle_rects(self, el):
        rect = el.get_rect()
        hs = self.handle_size / self.scale
        handles = {
            'tl': QRectF(rect.left() - hs/2, rect.top() - hs/2, hs, hs),
            'tr': QRectF(rect.right() - hs/2, rect.top() - hs/2, hs, hs),
            'bl': QRectF(rect.left() - hs/2, rect.bottom() - hs/2, hs, hs),
            'br': QRectF(rect.right() - hs/2, rect.bottom() - hs/2, hs, hs),
            'rot': QRectF(rect.center().x() - hs/2, rect.top() - 30/self.scale - hs/2, hs, hs)
        }
        return handles

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        painter.fillRect(self.rect(), QColor("#09090b"))
        
        # Draw Rulers
        self.draw_rulers(painter)
        
        painter.save()
        painter.translate(self.pan_offset)
        painter.scale(self.scale, self.scale)
        
        # Draw Technical Grid
        grid_pen = QPen(QColor("#18181b"), 1)
        painter.setPen(grid_pen)
        spacing = 100
        for x in range(0, 5000, spacing):
            painter.drawLine(x, 0, x, 5000)
        for y in range(0, 5000, spacing):
            painter.drawLine(0, y, 5000, y)

        # Draw Canvas Base
        painter.fillRect(0, 0, self.width(), self.height(), QColor(5, 5, 5))
        painter.drawPixmap(0, 0, self.canvas_pixmap)
        
        for el in self.engine.elements:
            if not el.visible: continue
            
            painter.save()
            rect = el.get_rect()
            t = self.get_element_transform(el)
            painter.setTransform(t, True)
            painter.setOpacity(el.opacity)
            
            if isinstance(el, ShapeElement):
                painter.setBrush(el.color)
                painter.setPen(Qt.NoPen)
                if el.shape_type == "rectangle": painter.drawRect(rect)
                elif el.shape_type == "circle": painter.drawEllipse(rect)
            elif isinstance(el, LineElement):
                painter.setPen(QPen(el.color, el.thickness))
                painter.drawLine(int(el.x), int(el.y), int(el.width), int(el.height))
            elif isinstance(el, TextElement):
                painter.setPen(el.color)
                painter.setFont(QFont(el._font_family, el.font_size))
                painter.drawText(rect, Qt.AlignCenter, el.text)
            elif isinstance(el, ImageElement) and el.original_pixmap:
                if el._cached_pixmap is None:
                    el._cached_pixmap = el.original_pixmap.scaled(rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                painter.drawPixmap(rect, el._cached_pixmap)

            if el.selected:
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(QColor("#3b82f6"), 2 / self.scale))
                painter.drawRect(rect.adjusted(-1, -1, 1, 1))
                
                if el == self.engine.selected_element and not isinstance(el, LineElement):
                    painter.setBrush(QColor("#FFFFFF"))
                    painter.setPen(QPen(QColor("#3b82f6"), 1 / self.scale))
                    handles = self.get_handle_rects(el)
                    for h_id, h_rect in handles.items():
                        if h_id == 'rot': painter.drawEllipse(h_rect)
                        else: painter.drawRect(h_rect)
            painter.restore()
        painter.restore()

    def draw_rulers(self, painter):
        painter.setPen(QPen(QColor("#1F1F1F"), 1))
        # Top Ruler
        painter.drawLine(0, 20, self.width(), 20)
        # Left Ruler
        painter.drawLine(20, 0, 20, self.height())
        
        painter.setFont(QFont('Inter', 8))
        step = 100 * self.scale
        if step < 20: step = 100
        
        # Horizontal ticks
        for x in range(0, self.width(), int(step)):
            cx = (x - self.pan_offset.x()) / self.scale
            painter.drawText(x + 2, 15, str(int(cx)))
            painter.drawLine(x, 15, x, 20)
            
        # Vertical ticks
        for y in range(0, self.height(), int(step)):
            cy = (y - self.pan_offset.y()) / self.scale
            painter.drawText(2, y + 15, str(int(cy)))
            painter.drawLine(15, y, 20, y)

    def wheelEvent(self, event):
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            new_scale = self.scale * zoom_factor
        else:
            new_scale = self.scale / zoom_factor
            
        new_scale = max(0.1, min(new_scale, 10.0))
        
        # Zoom towards mouse cursor
        mouse_pos = event.pos()
        old_canvas_pos = self.transform_point(mouse_pos)
        self.scale = new_scale
        new_mouse_pos = self.inverse_transform_point(old_canvas_pos)
        # new_mouse_pos is QPointF, needs to be QPoint for pan_offset
        self.pan_offset += mouse_pos - new_mouse_pos.toPoint()
        
        self.zoom_changed.emit(self.scale)
        self.update()

    def mousePressEvent(self, event):
        canvas_pos = self.transform_point(event.pos())
        multi = (event.modifiers() == Qt.ShiftModifier)
        
        if event.button() == Qt.MiddleButton or (event.button() == Qt.LeftButton and self.space_pressed):
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            return

        if self.engine.current_tool in ["brush", "eraser"]:
            self.brush_active = True
            self.paint_canvas(canvas_pos.toPoint())
            return

        # Check for handles on selected element
        sel_el = self.engine.selected_element
        if sel_el and not isinstance(sel_el, LineElement) and not multi:
            t = self.get_element_transform(sel_el)
            it, ok = t.inverted()
            if ok:
                el_space_pos = it.map(canvas_pos)
                handles = self.get_handle_rects(sel_el)
                for h_id, h_rect in handles.items():
                    if h_rect.contains(el_space_pos):
                        if h_id == 'rot':
                            self.rotate_element = sel_el
                        else:
                            self.resize_element = sel_el
                            self.resize_handle = h_id
                        return

        # Hit testing elements
        found = None
        for el in reversed(self.engine.elements):
            t = self.get_element_transform(el)
            it, ok = t.inverted()
            if ok:
                el_space_pos = it.map(canvas_pos)
                if QRectF(el.get_rect()).contains(el_space_pos):
                    found = el
                    break
        
        if found:
            self.engine.select_element(found, multi=multi)
            self.drag_elements = self.engine.selected_elements
            self.drag_offsets = {el: canvas_pos - QPointF(el.get_rect().topLeft()) for el in self.drag_elements}
        else:
            if not multi:
                self.engine.clear_selection()
            self.drag_elements = []

    def mouseMoveEvent(self, event):
        canvas_pos = self.transform_point(event.pos())
        
        if self.cursor() == Qt.ClosedHandCursor:
            delta = event.pos() - self.last_mouse_pos
            self.pan_offset += delta
            self.last_mouse_pos = event.pos()
            self.update()
            return

        if self.brush_active:
            self.paint_canvas(canvas_pos.toPoint())
            return

        if self.rotate_element:
            rect = self.rotate_element.get_rect()
            center = QPointF(rect.center())
            delta = canvas_pos - center
            angle = math.degrees(math.atan2(delta.y(), delta.x())) + 90
            self.rotate_element.rotation = angle
            self.update()

        elif self.resize_element:
            rect = self.resize_element.get_rect()
            p = canvas_pos
            
            if self.resize_handle == 'br':
                self.resize_element.width = max(10, p.x() - rect.left())
                self.resize_element.height = max(10, p.y() - rect.top())
            elif self.resize_handle == 'tl':
                new_w = rect.right() - p.x()
                new_h = rect.bottom() - p.y()
                if new_w > 10:
                    self.resize_element.x = p.x()
                    self.resize_element.width = new_w
                if new_h > 10:
                    self.resize_element.y = p.y()
                    self.resize_element.height = new_h
            self.update()
            
        elif self.drag_elements:
            for el in self.drag_elements:
                offset = self.drag_offsets[el]
                new_pos = canvas_pos - offset
                # Snap to grid
                new_x = round(new_pos.x() / self.grid_size) * self.grid_size
                new_y = round(new_pos.y() / self.grid_size) * self.grid_size
                
                if isinstance(el, LineElement):
                    dx = new_x - el.x
                    dy = new_y - el.y
                    el.x += dx
                    el.y += dy
                    el.width += dx
                    el.height += dy
                else:
                    el.x = new_x
                    el.y = new_y
            self.update()

    def mouseReleaseEvent(self, event):
        self.drag_elements = []
        self.resize_element = None
        self.rotate_element = None
        self.resize_handle = None
        self.brush_active = False
        self.setCursor(Qt.ArrowCursor)
        self.update()

    def paint_canvas(self, pos):
        painter = QPainter(self.canvas_pixmap)
        if self.engine.current_tool == "brush":
            painter.setPen(QPen(Qt.black, 5, Qt.SolidLine, Qt.RoundCap))
        else:
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.setPen(QPen(Qt.transparent, 20, Qt.SolidLine, Qt.RoundCap))
        painter.drawPoint(pos)
        painter.end()
        self.update()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        canvas_pos = self.transform_point(event.pos())
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                # canvas_pos is QPointF, emit needs QPoint
                self.file_dropped.emit(f, canvas_pos.toPoint())
