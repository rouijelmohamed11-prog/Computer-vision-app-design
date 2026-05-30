from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton, 
    QColorDialog, QDoubleSpinBox, QGroupBox, QFormLayout, QFontComboBox, 
    QSlider, QHBoxLayout, QScrollArea, QFrame
)
from PyQt5.QtCore import pyqtSignal, Qt
from core.objects import TextElement, ShapeElement, ImageElement, LineElement

class CollapsibleSection(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.header = QPushButton(f"  ▾  {title.upper()}")
        self.header.setObjectName("SectionHeader")
        self.header.setCheckable(True)
        self.header.setChecked(True)
        self.header.setFixedHeight(32)
        self.header.setStyleSheet("""
            QPushButton#SectionHeader {
                text-align: left;
                background-color: #1A1A1A;
                border: none;
                border-bottom: 1px solid #1F1F1F;
                color: #6B7280;
                font-weight: 800;
                font-size: 10px;
                letter-spacing: 0.05em;
            }
            QPushButton#SectionHeader:checked {
                color: #A78BFA;
            }
        """)
        
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(12)
        
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.content)
        
        self.header.clicked.connect(self.toggle)

    def toggle(self):
        visible = self.header.isChecked()
        self.content.setVisible(visible)
        self.header.setText(f"  {'▾' if visible else '▸'}  {self.header.text()[5:]}")

class PropertyPanel(QWidget):
    filter_requested = pyqtSignal(object, str)
    adjustment_requested = pyqtSignal(object, str, float)
    crop_requested = pyqtSignal(object)

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.current_element = None
        self.init_ui()
        self.engine.selection_changed.connect(self.set_element)

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: #0F0F0F; }")
        
        self.scroll_content = QWidget()
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll)

    def set_element(self, elements):
        self.clear_layout(self.content_layout)
        
        if not elements:
            placeholder = QLabel("Select an element to\nview properties")
            placeholder.setAlignment(Qt.AlignCenter)
            placeholder.setStyleSheet("color: #4B5563; font-style: italic; padding-top: 100px;")
            self.content_layout.addWidget(placeholder)
            return

        el = elements[-1] # Primary selection
        self.current_element = el

        # 1. Transform Section
        self.setup_transform_section(el)
        
        # 2. Appearance Section
        self.setup_appearance_section(el)
        
        # 3. Content Specific Section
        if isinstance(el, TextElement):
            self.setup_text_section(el)
        elif isinstance(el, ImageElement):
            self.setup_image_section(el)
        elif isinstance(el, (ShapeElement, LineElement)):
            self.setup_shape_section(el)
        
        # 4. Layer Actions
        self.setup_actions_section(el)
        
        self.content_layout.addStretch()

    def create_section(self, title):
        sec = CollapsibleSection(title)
        self.content_layout.addWidget(sec)
        return sec.content_layout

    def setup_transform_section(self, el):
        layout = self.create_section("Transform")
        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignLeft)
        
        # Styling for labels in form
        label_style = "color: #9CA3AF; font-size: 11px; font-weight: 500;"
        
        x_spin = QSpinBox()
        x_spin.setRange(-5000, 5000)
        x_spin.setValue(int(el.x))
        x_spin.valueChanged.connect(lambda v: self.update_prop(el, 'x', v))
        l1 = QLabel("X Position")
        l1.setStyleSheet(label_style)
        form.addRow(l1, x_spin)
        
        y_spin = QSpinBox()
        y_spin.setRange(-5000, 5000)
        y_spin.setValue(int(el.y))
        y_spin.valueChanged.connect(lambda v: self.update_prop(el, 'y', v))
        l2 = QLabel("Y Position")
        l2.setStyleSheet(label_style)
        form.addRow(l2, y_spin)
        
        w_spin = QSpinBox()
        w_spin.setRange(1, 5000)
        w_spin.setValue(int(el.width))
        w_spin.valueChanged.connect(lambda v: self.update_prop(el, 'width', v))
        l3 = QLabel("Width")
        l3.setStyleSheet(label_style)
        form.addRow(l3, w_spin)
        
        h_spin = QSpinBox()
        h_spin.setRange(1, 5000)
        h_spin.setValue(int(el.height))
        h_spin.valueChanged.connect(lambda v: self.update_prop(el, 'height', v))
        l4 = QLabel("Height")
        l4.setStyleSheet(label_style)
        form.addRow(l4, h_spin)

        layout.addLayout(form)
        
        rot_label = QLabel("Rotation")
        rot_label.setStyleSheet(label_style)
        layout.addWidget(rot_label)
        rot_slider = QSlider(Qt.Horizontal)
        rot_slider.setRange(0, 359)
        rot_slider.setValue(int(el.rotation))
        rot_slider.valueChanged.connect(lambda v: self.update_prop(el, 'rotation', v))
        layout.addWidget(rot_slider)

    def setup_appearance_section(self, el):
        layout = self.create_section("Appearance")
        
        op_label = QLabel("Opacity")
        op_label.setStyleSheet("color: #9CA3AF; font-size: 11px; font-weight: 500;")
        layout.addWidget(op_label)
        
        opacity_slider = QSlider(Qt.Horizontal)
        opacity_slider.setRange(0, 100)
        opacity_slider.setValue(int(getattr(el, 'opacity', 1.0) * 100))
        opacity_slider.valueChanged.connect(lambda v: self.update_prop(el, 'opacity', v / 100.0))
        layout.addWidget(opacity_slider)

    def setup_text_section(self, el):
        layout = self.create_section("Text Content")
        form = QFormLayout()
        label_style = "color: #9CA3AF; font-size: 11px; font-weight: 500;"
        
        txt_input = QLineEdit(el.text)
        txt_input.textChanged.connect(lambda t: self.update_prop(el, 'text', t))
        l1 = QLabel("Text")
        l1.setStyleSheet(label_style)
        form.addRow(l1, txt_input)

        font_input = QFontComboBox()
        font_input.currentFontChanged.connect(lambda f: self.update_font(el, f))
        l2 = QLabel("Font Family")
        l2.setStyleSheet(label_style)
        form.addRow(l2, font_input)

        size_input = QSpinBox()
        size_input.setRange(1, 500)
        size_input.setValue(el.font_size)
        size_input.valueChanged.connect(lambda v: self.update_prop(el, 'font_size', v))
        l3 = QLabel("Font Size")
        l3.setStyleSheet(label_style)
        form.addRow(l3, size_input)

        color_btn = QPushButton("Pick Color")
        color_btn.clicked.connect(lambda: self.pick_color(el))
        l4 = QLabel("Fill Color")
        l4.setStyleSheet(label_style)
        form.addRow(l4, color_btn)
        
        layout.addLayout(form)

    def setup_image_section(self, el):
        layout = self.create_section("Image Tools")
        
        btn_bg = QPushButton("✨ AI Background Removal")
        btn_bg.setObjectName("PrimaryButton")
        btn_bg.clicked.connect(lambda: self.filter_requested.emit(el, "Remove Background"))
        layout.addWidget(btn_bg)

        btn_crop = QPushButton("Smart Center Crop")
        btn_crop.clicked.connect(lambda: self.crop_requested.emit(el))
        layout.addWidget(btn_crop)

        # Filters Grid
        f_label = QLabel("Filters")
        f_label.setStyleSheet("color: #9CA3AF; font-size: 11px; font-weight: 700; margin-top: 10px;")
        layout.addWidget(f_label)
        
        grid = QHBoxLayout()
        for f in ["Grayscale", "Blur", "Edges"]:
            btn = QPushButton(f)
            btn.clicked.connect(lambda checked, name=f: self.filter_requested.emit(el, name))
            grid.addWidget(btn)
        layout.addLayout(grid)

        layout.addWidget(QLabel("Brightness"))
        b_slider = QSlider(Qt.Horizontal)
        b_slider.setRange(5, 20); b_slider.setValue(10)
        b_slider.valueChanged.connect(lambda v: self.adjustment_requested.emit(el, "Brightness", v/10.0))
        layout.addWidget(b_slider)
        
        layout.addWidget(QLabel("Saturation"))
        s_slider = QSlider(Qt.Horizontal)
        s_slider.setRange(0, 20); s_slider.setValue(10)
        s_slider.valueChanged.connect(lambda v: self.adjustment_requested.emit(el, "Saturation", v/10.0))
        layout.addWidget(s_slider)

    def setup_shape_section(self, el):
        layout = self.create_section("Style")
        color_btn = QPushButton("Change Color")
        color_btn.clicked.connect(lambda: self.pick_color(el))
        layout.addWidget(color_btn)
        
        if isinstance(el, LineElement):
            thick_label = QLabel("Thickness")
            thick_label.setStyleSheet("color: #9CA3AF; font-size: 11px;")
            layout.addWidget(thick_label)
            thick_input = QSpinBox()
            thick_input.setRange(1, 100); thick_input.setValue(el.thickness)
            thick_input.valueChanged.connect(lambda v: self.update_prop(el, 'thickness', v))
            layout.addWidget(thick_input)

    def setup_actions_section(self, el):
        layout = self.create_section("Hierarchy")
        
        h_layout = QHBoxLayout()
        btn_up = QPushButton("Bring to Front")
        btn_up.clicked.connect(lambda: self.engine.bring_to_front(el))
        h_layout.addWidget(btn_up)
        
        btn_down = QPushButton("Send to Back")
        btn_down.clicked.connect(lambda: self.engine.send_to_back(el))
        h_layout.addWidget(btn_down)
        layout.addLayout(h_layout)
        
        btn_del = QPushButton("Delete Element")
        btn_del.setStyleSheet("background-color: #7F1D1D; border-color: #991B1B; margin-top: 10px;")
        btn_del.clicked.connect(self.engine.delete_selected)
        layout.addWidget(btn_del)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def update_prop(self, el, prop, val):
        setattr(el, prop, val)
        self.engine.elements_changed.emit()

    def update_font(self, el, font):
        el._font_family = font.family()
        self.engine.elements_changed.emit()

    def pick_color(self, el):
        color = QColorDialog.getColor(el.color)
        if color.isValid():
            el.color = color
            self.engine.elements_changed.emit()
