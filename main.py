import sys
import os
import json
import cv2
import numpy as np
import traceback
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QLineEdit, QPushButton, QDockWidget, QAction, QFileDialog, 
    QDialog, QFormLayout, QSpinBox, QDialogButtonBox, QScrollArea,
    QLabel, QTabWidget, QFrame, QSplitter, QGraphicsOpacityEffect,
    QTabBar
)
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QPoint, QEasingCurve, pyqtProperty, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QImage, QPainter, QIcon, QColor

from core.engine import DesignEngine
from core.history import HistoryManager
from ui.canvas import DesignCanvas
from ui.toolbar import Toolbar
from ui.properties import PropertyPanel
from ui.layers import LayersPanel
from ui.palette import PalettePanel
from ui.templates import TemplatePanel
from ui.assets import AssetsPanel
from ui.styles import GLOBAL_STYLE
from nlp.parser import NLPParser
from nlp.intent import DesignGenerator
from vision import filters

class ToastNotification(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("Toast")
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(300, 45)
        self.hide()
        
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(500)

    def show_message(self, message):
        self.setText(message)
        self.move((self.parent().width() - self.width()) // 2, 80)
        self.show()
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()
        QTimer.singleShot(2500, self.fade_out)

    def fade_out(self):
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.hide)
        self.animation.start()

class StartupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Canvas")
        self.setStyleSheet(GLOBAL_STYLE)
        layout = QFormLayout(self)
        self.w_spin = QSpinBox()
        self.w_spin.setRange(100, 5000)
        self.w_spin.setValue(1200)
        layout.addRow("Width:", self.w_spin)
        self.h_spin = QSpinBox()
        self.h_spin.setRange(100, 5000)
        self.h_spin.setValue(800)
        layout.addRow("Height:", self.h_spin)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

class TopBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TopBar")
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(15)

        logo = QLabel("VISION STUDIO AI")
        logo.setObjectName("LogoLabel")
        layout.addWidget(logo)

        layout.addStretch()

        self.prompt_input = QLineEdit()
        self.prompt_input.setObjectName("AIPrompt")
        self.prompt_input.setPlaceholderText("Describe your design vision...")
        self.prompt_input.setMinimumWidth(500)
        layout.addWidget(self.prompt_input)

        self.gen_btn = QPushButton("✦ Generate")
        self.gen_btn.setObjectName("PrimaryButton")
        layout.addWidget(self.gen_btn)

        layout.addStretch()

        # View Controls
        self.zoom_label = QLabel("100%")
        self.zoom_label.setStyleSheet("color: #8B5CF6; font-weight: bold; min-width: 50px;")
        layout.addWidget(self.zoom_label)
        
        self.reset_view_btn = QPushButton("Reset View")
        layout.addWidget(self.reset_view_btn)

        self.undo_btn = QPushButton("Undo")
        self.redo_btn = QPushButton("Redo")
        self.export_btn = QPushButton("Export")
        self.export_btn.setObjectName("PrimaryButton")
        
        layout.addWidget(self.undo_btn)
        layout.addWidget(self.redo_btn)
        layout.addWidget(self.export_btn)

from ui.suggestions import SuggestionsPanel
from ui.dashboard import WelcomeDashboard
from PyQt5.QtWidgets import QStackedWidget

class ProjectTabs(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setExpanding(False)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.addTab("Untitled Project")
        self.addTab("Brand Identity")
        self.setStyleSheet("""
            QTabBar::tab {
                background: #0F0F0F;
                color: #6B7280;
                padding: 8px 20px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background: #1A1A1A;
                color: #C4B5FD;
                border-bottom: 2px solid #8B5CF6;
            }
        """)

class SideNav(QFrame):
    tab_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(56) # Slimmer
        self.setObjectName("SideNav")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 16, 0, 16)
        layout.setSpacing(8)

        self.btns = []
        icons = ["⌂", "◈", "⧉", "✦", "◩"]
        tooltips = ["Dashboard", "Architect", "Assets", "Intelligence", "Library"]
        
        for i, icon in enumerate(icons):
            btn = QPushButton(icon)
            btn.setObjectName("IconButton")
            btn.setCheckable(True)
            btn.setFixedSize(40, 40)
            btn.setToolTip(tooltips[i])
            btn.clicked.connect(lambda checked, idx=i: self.on_btn_clicked(idx))
            layout.addWidget(btn, alignment=Qt.AlignCenter)
            self.btns.append(btn)
        
        self.btns[0].setChecked(True)
        layout.addStretch()

    def on_btn_clicked(self, index):
        for i, btn in enumerate(self.btns):
            btn.setChecked(i == index)
        self.tab_changed.emit(index)

class FilterWorker(QThread):
    finished = pyqtSignal(object, np.ndarray, str)
    error = pyqtSignal(str)

    def __init__(self, el, filter_name, img_bgr):
        super().__init__()
        self.el = el
        self.filter_name = filter_name
        self.img_bgr = img_bgr

    def run(self):
        try:
            res = self.img_bgr
            if self.filter_name == "Grayscale": 
                res = filters.apply_grayscale(self.img_bgr)
                res = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
            elif self.filter_name == "Blur": res = filters.apply_blur(self.img_bgr)
            elif self.filter_name == "Sharpen": res = filters.apply_sharpen(self.img_bgr)
            elif self.filter_name == "Edges": 
                res = filters.apply_edges(self.img_bgr)
                res = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
            elif self.filter_name == "Faces": res = filters.detect_faces(self.img_bgr)
            elif self.filter_name == "Remove Background": res = filters.apply_remove_background(self.img_bgr)
            
            self.finished.emit(self.el, res, self.filter_name)
        except Exception as e:
            self.error.emit(str(e))

class CanvaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vision Studio AI - Ultimate Edition")
        
        # Default canvas size
        self.canvas_w, self.canvas_h = 1200, 800

        self.resize(1800, 1000)
        
        self.engine = DesignEngine()
        self.history = HistoryManager(self.engine)
        self.parser = NLPParser()
        self.generator = DesignGenerator(self.engine)

        self.init_ui()
        self.apply_theme()
        self.toast = ToastNotification("Ready", self)
        
        self.engine.elements_changed.connect(self.history.save_state)

    def apply_theme(self):
        self.setStyleSheet(GLOBAL_STYLE)

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Top Bar
        self.top_bar = TopBar(self)
        self.top_bar.gen_btn.clicked.connect(self.generate_design)
        self.top_bar.prompt_input.returnPressed.connect(self.generate_design)
        self.top_bar.undo_btn.clicked.connect(self.history.undo)
        self.top_bar.redo_btn.clicked.connect(self.history.redo)
        self.top_bar.export_btn.clicked.connect(self.export_design)
        self.top_bar.reset_view_btn.clicked.connect(self.reset_view)
        self.main_layout.addWidget(self.top_bar)

        # Content Container (SideNav + Stacked Area)
        self.content_container = QWidget()
        content_layout = QHBoxLayout(self.content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Left Side Navigation
        self.side_nav = SideNav()
        content_layout.addWidget(self.side_nav)

        # Stacked Widget for Main Content
        self.main_stack = QStackedWidget()
        
        # --- 1. Dashboard View ---
        self.dashboard = WelcomeDashboard()
        self.dashboard.start_blank.connect(self.create_new_design)
        self.dashboard.template_selected.connect(self.load_template)
        self.main_stack.addWidget(self.dashboard)

        # --- 2. Editor View ---
        self.editor_view = QWidget()
        editor_layout = QHBoxLayout(self.editor_view)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)

        # Left Sidebar (Collapsible Panel)
        self.left_panel = QTabWidget()
        self.left_panel.setObjectName("SidebarPanel")
        self.left_panel.setFixedWidth(300)
        self.left_panel.tabBar().hide()
        
        # Spacer for Home button in SideNav (Index 0)
        self.left_panel.addTab(QWidget(), "") 
        
        self.toolbar = Toolbar(self.engine)
        self.toolbar.image_added.connect(self.add_image_element)
        self.left_panel.addTab(self.toolbar, "")
        
        self.assets = AssetsPanel(self.engine)
        self.assets.asset_selected.connect(self.add_image_element)
        self.left_panel.addTab(self.assets, "")
        
        self.ai_suggestions = SuggestionsPanel(self.engine)
        self.left_panel.addTab(self.ai_suggestions, "")
        
        self.templates = TemplatePanel(self.engine)
        self.left_panel.addTab(self.templates, "")
        
        self.side_nav.tab_changed.connect(self.on_nav_changed)
        editor_layout.addWidget(self.left_panel)

        # Canvas Area
        self.canvas_splitter = QSplitter(Qt.Horizontal)
        self.canvas_splitter.setStyleSheet("QSplitter::handle { background: #1F1F1F; width: 1px; }")
        
        self.canvas_main_area = QWidget()
        c_main_layout = QVBoxLayout(self.canvas_main_area)
        c_main_layout.setContentsMargins(0, 0, 0, 0)
        c_main_layout.setSpacing(0)
        
        self.project_tabs = ProjectTabs()
        c_main_layout.addWidget(self.project_tabs)
        
        self.canvas_container = QWidget()
        self.canvas_container.setStyleSheet("background-color: #050505;")
        canvas_layout = QVBoxLayout(self.canvas_container)
        canvas_layout.setContentsMargins(20, 20, 20, 20)
        
        self.canvas = DesignCanvas(self.engine)
        self.canvas.setFixedSize(self.canvas_w, self.canvas_h)
        self.canvas.zoom_changed.connect(self.update_zoom_label)
        self.canvas.file_dropped.connect(self.add_image_at_pos)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setAlignment(Qt.AlignCenter)
        scroll.setWidget(self.canvas)
        scroll.setStyleSheet("background: transparent; border: none;")
        canvas_layout.addWidget(scroll)
        
        c_main_layout.addWidget(self.canvas_container)
        self.canvas_splitter.addWidget(self.canvas_main_area)

        # Right Inspector Panel
        self.right_panel = QTabWidget()
        self.right_panel.setObjectName("RightPanel")
        self.right_panel.setFixedWidth(320)
        
        self.properties = PropertyPanel(self.engine)
        self.properties.filter_requested.connect(self.apply_filter)
        self.properties.adjustment_requested.connect(self.apply_adjustment)
        self.properties.crop_requested.connect(self.apply_crop)
        self.right_panel.addTab(self.properties, "Properties")
        
        self.layers = LayersPanel(self.engine)
        self.right_panel.addTab(self.layers, "Layers")
        
        self.palette = PalettePanel()
        self.palette.color_selected.connect(self.apply_color_to_selection)
        self.right_panel.addTab(self.palette, "Styles")
        
        self.canvas_splitter.addWidget(self.right_panel)
        editor_layout.addWidget(self.canvas_splitter)
        
        self.main_stack.addWidget(self.editor_view)
        content_layout.addWidget(self.main_stack)

        self.main_layout.addWidget(self.content_container)

    def on_nav_changed(self, index):
        if index == 0:
            self.main_stack.setCurrentIndex(0)
        else:
            self.main_stack.setCurrentIndex(1)
            self.left_panel.setCurrentIndex(index)

    def create_new_design(self):
        dialog = StartupDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.canvas_w = dialog.w_spin.value()
            self.canvas_h = dialog.h_spin.value()
            self.canvas.setFixedSize(self.canvas_w, self.canvas_h)
            self.engine.elements.clear()
            self.engine.elements_changed.emit()
            self.main_stack.setCurrentIndex(1)
            self.side_nav.btns[1].setChecked(True)
            self.left_panel.setCurrentIndex(1)
            self.toast.show_message("New canvas created")

    def load_template(self, name):
        self.toast.show_message(f"Loading {name} template...")
        self.engine.elements.clear()
        # Add basic elements for the template
        from core.objects import TextElement, ShapeElement
        self.engine.add_element(TextElement(name.upper(), 100, 100, 48, QColor("#8B5CF6")))
        self.engine.add_element(ShapeElement("rectangle", 100, 200, QColor("#1F1F1F")))
        self.main_stack.setCurrentIndex(1)
        self.side_nav.btns[1].setChecked(True)
        self.left_panel.setCurrentIndex(1)
        self.toast.show_message(f"{name} template ready")

    def update_zoom_label(self, scale):
        self.top_bar.zoom_label.setText(f"{int(scale * 100)}%")

    def reset_view(self):
        self.canvas.scale = 1.0
        self.canvas.pan_offset = QPoint(0, 0)
        self.update_zoom_label(1.0)
        self.canvas.update()

    def keyPressEvent(self, event):
        sel = self.engine.selected_element
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            if sel:
                self.engine.remove_element(sel)
                self.toast.show_message("Element deleted")
        elif event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.history.undo()
            self.toast.show_message("Undo")
        elif event.key() == Qt.Key_Y and event.modifiers() == Qt.ControlModifier:
            self.history.redo()
            self.toast.show_message("Redo")
        elif sel and event.key() in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down]:
            nudge = 1 if event.modifiers() != Qt.ShiftModifier else 10
            if event.key() == Qt.Key_Left: sel.x -= nudge
            elif event.key() == Qt.Key_Right: sel.x += nudge
            elif event.key() == Qt.Key_Up: sel.y -= nudge
            elif event.key() == Qt.Key_Down: sel.y += nudge
        super().keyPressEvent(event)

    def generate_design(self):
        prompt = self.top_bar.prompt_input.text()
        if not prompt: return
        self.toast.show_message("AI is thinking...")
        intent = self.parser.parse_prompt(prompt)
        self.generator.generate_from_intent(intent)
        self.canvas.update()
        self.toast.show_message("Design generated!")

    def export_design(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export", "", "PNG (*.png);;JPG (*.jpg)")
        if path:
            image = QImage(self.canvas.size(), QImage.Format_ARGB32)
            image.fill(Qt.transparent)
            painter = QPainter(image)
            self.canvas.render(painter)
            painter.end()
            image.save(path)
            self.toast.show_message(f"Exported to {os.path.basename(path)}")

    def apply_color_to_selection(self, color):
        el = self.engine.selected_element
        if el and hasattr(el, 'color'):
            el.color = color
            self.toast.show_message("Color applied")

    def add_image_element(self, path):
        from core.objects import ImageElement
        el = ImageElement(path, 100, 100)
        el.original_pixmap = QPixmap(path)
        el.base_pixmap = el.original_pixmap
        self.engine.add_element(el)
        self.toast.show_message("Image added")

    def add_image_at_pos(self, path, pos):
        from core.objects import ImageElement
        el = ImageElement(path, pos.x(), pos.y())
        el.original_pixmap = QPixmap(path)
        el.base_pixmap = el.original_pixmap
        self.engine.add_element(el)

    def apply_filter(self, el, filter_name):
        if not el or not hasattr(el, 'original_pixmap') or el.original_pixmap.isNull(): return
        
        self.toast.show_message(f"Applying {filter_name}...")
        
        # Prepare data for worker
        image = el.original_pixmap.toImage().convertToFormat(QImage.Format_RGBA8888)
        w, h = image.width(), image.height()
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        arr = np.frombuffer(ptr, np.uint8).reshape((h, image.bytesPerLine() // 4, 4))
        arr = arr[:, :w, :].copy() 
        img_bgr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

        if filter_name == "Palette":
            colors = filters.extract_color_palette(img_bgr)
            self.toast.show_message(f"Extracted {len(colors)} colors!")
            return

        # Use a list to store worker to prevent GC
        if not hasattr(self, '_workers'): self._workers = []
        worker = FilterWorker(el, filter_name, img_bgr)
        worker.finished.connect(self.on_filter_finished)
        worker.error.connect(lambda e: self.toast.show_message(f"Error: {e}"))
        worker.finished.connect(lambda: self._workers.remove(worker))
        self._workers.append(worker)
        worker.start()

    def on_filter_finished(self, el, img_out_bgr, filter_name):
        try:
            if len(img_out_bgr.shape) == 3 and img_out_bgr.shape[2] == 4: 
                img_out = cv2.cvtColor(img_out_bgr, cv2.COLOR_BGRA2RGBA)
            else: 
                img_out = cv2.cvtColor(img_out_bgr, cv2.COLOR_BGR2RGBA)
            
            img_out = np.ascontiguousarray(img_out)
            h, w, _ = img_out.shape
            q_img = QImage(img_out.data, w, h, w * 4, QImage.Format_RGBA8888).copy()
            new_pixmap = QPixmap.fromImage(q_img)
            el.original_pixmap = new_pixmap
            el.base_pixmap = new_pixmap
            el._cached_pixmap = None
            self.engine.elements_changed.emit()
            self.toast.show_message(f"Applied {filter_name}")
        except Exception: traceback.print_exc()

    def apply_adjustment(self, el, adj_type, value):
        source_pixmap = getattr(el, 'base_pixmap', None) or el.original_pixmap
        if not el or source_pixmap.isNull(): return
        try:
            image = source_pixmap.toImage().convertToFormat(QImage.Format_RGBA8888)
            w, h = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.frombuffer(ptr, np.uint8).reshape((h, image.bytesPerLine() // 4, 4))
            arr = arr[:, :w, :].copy()
            img_bgr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
            
            if adj_type == "Brightness": img_bgr = filters.apply_brightness(img_bgr, value)
            elif adj_type == "Contrast": img_bgr = filters.apply_contrast(img_bgr, value)
            elif adj_type == "Saturation": img_bgr = filters.apply_saturation(img_bgr, value)
            
            img_rgba = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGBA)
            img_rgba = np.ascontiguousarray(img_rgba)
            h, w, _ = img_rgba.shape
            q_img = QImage(img_rgba.data, w, h, w * 4, QImage.Format_RGBA8888).copy()
            el.original_pixmap = QPixmap.fromImage(q_img)
            self.engine.elements_changed.emit()
        except Exception: traceback.print_exc()

    def apply_crop(self, el):
        if not el or not hasattr(el, 'original_pixmap') or el.original_pixmap.isNull(): return
        self.toast.show_message("Cropping image...")
        
        try:
            image = el.original_pixmap.toImage().convertToFormat(QImage.Format_RGBA8888)
            w, h = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.frombuffer(ptr, np.uint8).reshape((h, image.bytesPerLine() // 4, 4))
            arr = arr[:, :w, :].copy()
            img_bgr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
            
            cropped_bgr = filters.center_crop(img_bgr)
            
            img_rgba = cv2.cvtColor(cropped_bgr, cv2.COLOR_BGR2RGBA)
            img_rgba = np.ascontiguousarray(img_rgba)
            h, w, _ = img_rgba.shape
            q_img = QImage(img_rgba.data, w, h, w * 4, QImage.Format_RGBA8888).copy()
            
            el.original_pixmap = QPixmap.fromImage(q_img)
            el.base_pixmap = el.original_pixmap
            el.width = w
            el.height = h
            el._cached_pixmap = None
            self.engine.elements_changed.emit()
            self.toast.show_message("Smart crop applied")
        except Exception: traceback.print_exc()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CanvaApp()
    window.show()
    sys.exit(app.exec_())
