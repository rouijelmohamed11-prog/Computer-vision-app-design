from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QLabel, QLineEdit, QFrame
from PyQt5.QtCore import Qt
from core.objects import TextElement, ImageElement, LineElement

class LayersPanel(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.init_ui()
        
        self.engine.elements_changed.connect(self.refresh_list)
        self.engine.selection_changed.connect(self.sync_selection)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        header = QFrame()
        header.setFixedHeight(40)
        header.setStyleSheet("background-color: #1A1A1A; border-bottom: 1px solid #1F1F1F;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(16, 0, 16, 0)
        
        title = QLabel("LAYERS")
        title.setStyleSheet("font-weight: 700; color: #6B7280; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em;")
        h_layout.addWidget(title)
        
        self.btn_del = QPushButton("✕")
        self.btn_del.setObjectName("IconButton")
        self.btn_del.setFixedSize(24, 24)
        self.btn_del.clicked.connect(self.engine.delete_selected)
        h_layout.addStretch()
        h_layout.addWidget(self.btn_del)
        
        layout.addWidget(header)
        
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #0F0F0F;
                border: none;
                padding: 4px;
            }
            QListWidget::item {
                background-color: transparent;
                border-radius: 4px;
                margin: 1px 4px;
                padding: 6px 8px;
                color: #D1D5DB;
            }
            QListWidget::item:hover {
                background-color: #1A1A1A;
            }
            QListWidget::item:selected {
                background-color: #2A1F5E;
                color: #C4B5FD;
            }
        """)
        layout.addWidget(self.list_widget)

    def refresh_list(self):
        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        
        for el in reversed(self.engine.elements):
            icon = "▢"
            if isinstance(el, TextElement): icon = "T"
            elif isinstance(el, ImageElement): icon = "🖼"
            elif isinstance(el, LineElement): icon = "╱"
            
            name = getattr(el, 'name', el.__class__.__name__.replace('Element', ''))
            display_name = f"{icon}  {name}"
            if not el.visible:
                display_name = "◌ " + display_name
            
            item = QListWidgetItem(display_name)
            item.setData(Qt.UserRole, el)
            
            if el.selected:
                item.setSelected(True)
                
            self.list_widget.addItem(item)
            
        self.list_widget.blockSignals(False)

    def sync_selection(self, selected_elements):
        self.list_widget.blockSignals(True)
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            el = item.data(Qt.UserRole)
            item.setSelected(el in selected_elements)
        self.list_widget.blockSignals(False)

    def on_selection_changed(self):
        self.engine.blockSignals(True)
        selected_items = self.list_widget.selectedItems()
        
        # Clear previous selection state in engine objects
        for el in self.engine.elements:
            el.selected = False
            
        new_selection = []
        for item in selected_items:
            el = item.data(Qt.UserRole)
            el.selected = True
            new_selection.append(el)
            
        self.engine._selected_elements = new_selection
        self.engine.blockSignals(False)
        self.engine.selection_changed.emit(new_selection)
        self.engine.elements_changed.emit()
