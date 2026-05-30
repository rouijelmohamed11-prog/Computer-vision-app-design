import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage, QImageReader
from PyQt5.QtCore import QSize, pyqtSignal, Qt, QThread, QObject

class AssetLoader(QObject):
    asset_loaded = pyqtSignal(str, str, QImage)
    finished = pyqtSignal()

    def __init__(self, assets_dir):
        super().__init__()
        self.assets_dir = assets_dir

    def run(self):
        if not os.path.exists(self.assets_dir):
            self.finished.emit()
            return

        files = sorted(os.listdir(self.assets_dir))
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                path = os.path.normpath(os.path.join(self.assets_dir, filename))
                reader = QImageReader(path)
                reader.setAutoTransform(True)
                orig_size = reader.size()
                if orig_size.isValid():
                    target_size = orig_size.scaled(150, 150, Qt.KeepAspectRatio)
                    reader.setScaledSize(target_size)
                    thumb = reader.read()
                    if not thumb.isNull():
                        self.asset_loaded.emit(filename, path, thumb)
        self.finished.emit()

class AssetsPanel(QWidget):
    asset_selected = pyqtSignal(str)

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.assets_dir = os.path.join(os.getcwd(), "assets")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)

        header = QLabel("IMAGE LIBRARY")
        header.setStyleSheet("font-weight: bold; color: #8B5CF6; font-size: 11px; letter-spacing: 1px;")
        layout.addWidget(header)
        
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setIconSize(QSize(120, 120))
        self.list_widget.setResizeMode(QListWidget.Adjust)
        self.list_widget.setMovement(QListWidget.Static)
        self.list_widget.setSpacing(8)
        self.list_widget.setWordWrap(True)
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #1A1A1A;
                border: 1px solid #2D2D2D;
                border-radius: 8px;
                outline: none;
            }
            QListWidget::item {
                background-color: #2D2D2D;
                border-radius: 6px;
                margin: 4px;
                color: #9CA3AF;
                font-size: 10px;
            }
            QListWidget::item:hover {
                background-color: #3F3F46;
            }
            QListWidget::item:selected {
                background-color: #8B5CF6;
                color: white;
            }
        """)
        
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list_widget)
        
        hint = QLabel("Tip: Double-click to add to canvas")
        hint.setStyleSheet("font-size: 10px; color: #4B5563; font-style: italic;")
        layout.addWidget(hint)

        self.start_loading()

    def start_loading(self):
        self.thread = QThread()
        self.loader = AssetLoader(self.assets_dir)
        self.loader.moveToThread(self.thread)
        self.thread.started.connect(self.loader.run)
        self.loader.asset_loaded.connect(self.add_asset_item)
        self.loader.finished.connect(self.thread.quit)
        self.loader.finished.connect(self.loader.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def add_asset_item(self, filename, path, thumb_image):
        item = QListWidgetItem()
        pixmap = QPixmap.fromImage(thumb_image)
        item.setIcon(QIcon(pixmap))
        display_name = filename[:12] + ".." if len(filename) > 12 else filename
        item.setText(display_name)
        item.setToolTip(filename)
        item.setData(Qt.UserRole, path)
        item.setTextAlignment(Qt.AlignCenter)
        self.list_widget.addItem(item)

    def on_item_double_clicked(self, item):
        path = item.data(Qt.UserRole)
        self.asset_selected.emit(path)
