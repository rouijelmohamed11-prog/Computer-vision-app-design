from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor

class TemplateCard(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, title, icon_text, description, parent=None):
        super().__init__(parent)
        self.setObjectName("TemplateCard")
        self.setFixedSize(220, 160)
        self.setStyleSheet("""
            QFrame#TemplateCard {
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 4px;
            }
            QFrame#TemplateCard:hover {
                border-color: #3b82f6;
                background-color: #27272a;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.icon_label = QLabel(icon_text)
        self.icon_label.setStyleSheet("font-size: 24px; color: #3b82f6; margin-bottom: 8px;")
        layout.addWidget(self.icon_label)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: 700; font-size: 13px; color: #fafafa; text-transform: uppercase; letter-spacing: 0.02em;")
        layout.addWidget(self.title_label)
        
        self.desc_label = QLabel(description)
        self.desc_label.setStyleSheet("font-size: 11px; color: #a1a1aa;")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit(self.title_label.text())
        super().mousePressEvent(event)

class WelcomeDashboard(QWidget):
    template_selected = pyqtSignal(str)
    start_blank = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(40)

        # Header
        header = QVBoxLayout()
        title = QLabel("Vision Studio AI")
        title.setStyleSheet("font-size: 42px; font-weight: 800; color: #fafafa; letter-spacing: -0.02em;")
        header.addWidget(title)
        
        subtitle = QLabel("Engineering-grade computer vision design environment.")
        subtitle.setStyleSheet("font-size: 14px; color: #71717a; font-family: 'JetBrains Mono', monospace;")
        header.addWidget(subtitle)
        layout.addLayout(header)

        # Quick Actions
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        
        btn_new = QPushButton("+ New Architecture")
        btn_new.setObjectName("PrimaryButton")
        btn_new.setFixedSize(200, 44)
        btn_new.clicked.connect(self.start_blank)
        actions_layout.addWidget(btn_new)
        
        btn_open = QPushButton("⬚ Load Project")
        btn_open.setFixedSize(200, 44)
        actions_layout.addWidget(btn_open)
        
        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        # Templates Section
        templates_label = QLabel("Reference Architectures")
        templates_label.setStyleSheet("font-size: 11px; font-weight: 700; color: #71717a; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 20px;")
        layout.addWidget(templates_label)

        templates_grid = QGridLayout()
        templates_grid.setSpacing(16)
        
        templates = [
            ("Object Detection", "⌖", "Neural tracking & localization."),
            ("Face Recognition", "⚇", "Biometric verification pipeline."),
            ("Smart Retail", "▤", "Spatial analytics & flow-mapping."),
            ("Traffic Analysis", "☲", "Temporal dynamics & classification."),
            ("Medical Imaging", "✙", "Volumetric diagnostics & segmentation."),
            ("Industrial Inspection", "❖", "Defect detection & quality control.")
        ]
        
        for i, (name, icon, desc) in enumerate(templates):
            card = TemplateCard(name, icon, desc)
            card.clicked.connect(self.template_selected.emit)
            templates_grid.addWidget(card, i // 3, i % 3)
            
        layout.addLayout(templates_grid)
        layout.addStretch()

        # Footer Stats
        footer = QHBoxLayout()
        stats = [("50.2k", "Active Nodes"), ("1.24M", "Inference Cycles"), ("15.8k", "Core Designers")]
        for val, label in stats:
            container = QVBoxLayout()
            v_lab = QLabel(val)
            v_lab.setStyleSheet("font-size: 18px; font-weight: 700; color: #3b82f6; font-family: 'JetBrains Mono';")
            l_lab = QLabel(label)
            l_lab.setStyleSheet("font-size: 9px; color: #71717a; text-transform: uppercase; letter-spacing: 0.05em;")
            container.addWidget(v_lab, alignment=Qt.AlignLeft)
            container.addWidget(l_lab, alignment=Qt.AlignLeft)
            footer.addLayout(container)
            footer.addSpacing(60)
        
        footer.addStretch()
        layout.addLayout(footer)
