from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QFrame
from PyQt5.QtCore import pyqtSignal, Qt
from core.objects import TextElement, ShapeElement, LineElement

class Toolbar(QWidget):
    image_added = pyqtSignal(str)

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(12)

        # Tools Section
        label = QLabel("CREATION")
        label.setStyleSheet("color: #6B7280; font-weight: 700; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em;")
        layout.addWidget(label)

        tools_grid = QWidget()
        grid = QVBoxLayout(tools_grid)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(8)

        self.add_tool_item(grid, "Text", "T", self.add_text)
        self.add_tool_item(grid, "Rectangle", "⬚", lambda: self.add_shape("rectangle"))
        self.add_tool_item(grid, "Circle", "○", lambda: self.add_shape("circle"))
        self.add_tool_item(grid, "Line", "╱", self.add_line)
        self.add_tool_item(grid, "Image", "🖼", self.add_image)
        
        layout.addWidget(tools_grid)

        # Drawing Section
        draw_label = QLabel("DRAWING")
        draw_label.setStyleSheet("color: #6B7280; font-weight: 700; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 16px;")
        layout.addWidget(draw_label)

        draw_grid = QWidget()
        d_grid = QVBoxLayout(draw_grid)
        d_grid.setContentsMargins(0, 0, 0, 0)
        d_grid.setSpacing(8)

        self.add_tool_item(d_grid, "Brush", "✎", lambda: self.set_tool("brush"))
        self.add_tool_item(d_grid, "Eraser", "⌫", lambda: self.set_tool("eraser"))
        
        layout.addWidget(draw_grid)
        layout.addStretch()

    def add_tool_item(self, layout, name, icon, callback):
        btn = QPushButton(f"  {icon}   {name}")
        btn.setObjectName("NavItem")
        btn.setStyleSheet("""
            QPushButton#NavItem {
                text-align: left;
                padding: 10px 14px;
                font-size: 13px;
                background-color: transparent;
                border-radius: 6px;
                color: #D1D5DB;
            }
            QPushButton#NavItem:hover {
                background-color: #1A1A1A;
                color: #F9FAFB;
            }
            QPushButton#NavItem:pressed {
                background-color: #262626;
            }
        """)
        btn.clicked.connect(callback)
        layout.addWidget(btn)

    def set_tool(self, tool_name):
        self.engine.current_tool = tool_name
        self.engine.elements_changed.emit()

    def add_text(self):
        el = TextElement("Double click to edit", 200, 200)
        self.engine.add_element(el)

    def add_shape(self, shape_type):
        el = ShapeElement(shape_type, 200, 200)
        self.engine.add_element(el)

    def add_line(self):
        el = LineElement(200, 200, 400, 400)
        self.engine.add_element(el)

    def add_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.image_added.emit(path)
