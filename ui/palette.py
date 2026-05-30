from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QGroupBox, QScrollArea
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal

class PalettePanel(QWidget):
    color_selected = pyqtSignal(QColor)

    def __init__(self):
        super().__init__()
        self.palettes = {
            "Modern AI": ["#8B5CF6", "#A78BFA", "#C4B5FD", "#0F172A", "#1E293B"],
            "Gaming": ["#00FFFF", "#FF00FF", "#00FF00", "#FFD700", "#121212"],
            "Luxury": ["#1A1A1A", "#D4AF37", "#FFFFFF", "#8B0000", "#2D2D2D"],
            "Minimal": ["#FFFFFF", "#F3F4F6", "#9CA3AF", "#4B5563", "#111827"]
        }
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 20, 15, 20)
        main_layout.setSpacing(10)

        header = QLabel("COLOR PALETTES")
        header.setStyleSheet("font-weight: bold; color: #8B5CF6; font-size: 11px; letter-spacing: 1px;")
        main_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        
        for name, hex_colors in self.palettes.items():
            group = QGroupBox(name.upper())
            grid = QGridLayout()
            grid.setSpacing(8)
            for i, hex_code in enumerate(hex_colors):
                btn = QPushButton()
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {hex_code};
                        border: 1px solid #3F3F46;
                        border-radius: 4px;
                    }}
                    QPushButton:hover {{
                        border: 2px solid white;
                    }}
                """)
                btn.setFixedSize(45, 45)
                color = QColor(hex_code)
                btn.clicked.connect(lambda checked, c=color: self.color_selected.emit(c))
                grid.addWidget(btn, i // 3, i % 3)
            group.setLayout(grid)
            layout.addWidget(group)
        
        layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
