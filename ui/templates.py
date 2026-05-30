from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGroupBox, QScrollArea
from PyQt5.QtGui import QColor

class TemplatePanel(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 20, 15, 20)
        main_layout.setSpacing(10)

        header = QLabel("DESIGN TEMPLATES")
        header.setStyleSheet("font-weight: bold; color: #8B5CF6; font-size: 11px; letter-spacing: 1px;")
        main_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(15)
        
        group = QGroupBox("PRESETS")
        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.setContentsMargins(10, 20, 10, 10)
        
        self.presets = {
            "🎮 Gaming Poster": self.apply_gaming_template,
            "🏢 Business Flyer": self.apply_business_template,
            "🌿 Minimal Quote": self.apply_minimal_template,
            "🚀 Tech Startup": self.apply_tech_template
        }
        
        for name, func in self.presets.items():
            btn = QPushButton(name)
            btn.setMinimumHeight(50)
            btn.setStyleSheet("text-align: left; padding-left: 15px;")
            btn.clicked.connect(func)
            vbox.addWidget(btn)
        
        group.setLayout(vbox)
        layout.addWidget(group)
        layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def apply_gaming_template(self):
        from core.objects import TextElement, ShapeElement
        self.engine.elements.clear()
        bg = ShapeElement("rectangle", 0, 0)
        bg.color = QColor("#121212")
        bg.width, bg.height = 1200, 800
        self.engine.add_element(bg)
        
        txt = TextElement("LEVEL UP", 300, 300)
        txt.font_size = 120
        txt.color = QColor("#00FF00")
        self.engine.add_element(txt)
        self.engine.elements_changed.emit()

    def apply_business_template(self):
        from core.objects import TextElement, ShapeElement
        self.engine.elements.clear()
        bg = ShapeElement("rectangle", 0, 0)
        bg.color = QColor("#F3F4F6")
        bg.width, bg.height = 1200, 800
        self.engine.add_element(bg)
        
        txt = TextElement("Visionary Services", 100, 100)
        txt.font_size = 40
        txt.color = QColor("#111827")
        self.engine.add_element(txt)
        self.engine.elements_changed.emit()

    def apply_minimal_template(self):
        from core.objects import TextElement
        self.engine.elements.clear()
        txt = TextElement("Stay Simple.", 200, 350)
        txt.font_size = 80
        txt.color = QColor("#FFFFFF")
        self.engine.add_element(txt)
        self.engine.elements_changed.emit()

    def apply_tech_template(self):
        from core.objects import TextElement, ShapeElement
        self.engine.elements.clear()
        bg = ShapeElement("rectangle", 0, 0)
        bg.color = QColor("#0F172A")
        bg.width, bg.height = 1200, 800
        self.engine.add_element(bg)
        
        txt = TextElement("The Future is AI", 200, 300)
        txt.font_size = 60
        txt.color = QColor("#8B5CF6")
        self.engine.add_element(txt)
        self.engine.elements_changed.emit()
