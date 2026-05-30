from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PyQt5.QtCore import Qt, pyqtSignal

class SuggestionsPanel(QWidget):
    suggestion_selected = pyqtSignal(dict)

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(16)

        label = QLabel("AI SUGGESTIONS")
        label.setStyleSheet("color: #A78BFA; font-weight: 800; font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em;")
        layout.addWidget(label)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none;")
        
        container = QWidget()
        self.list_layout = QVBoxLayout(container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(12)
        
        # Add some mock suggestions for now
        self.add_suggestion("Modern Minimalist", "Clean typography with soft pastels")
        self.add_suggestion("Cyberpunk Neon", "Dark background with vibrant accents")
        self.add_suggestion("Corporate Professional", "Reliable blue tones and sans-serif fonts")
        
        self.scroll.setWidget(container)
        layout.addWidget(self.scroll)
        
        layout.addStretch()

    def add_suggestion(self, title, desc):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1A1A1A;
                border: 1px solid #262626;
                border-radius: 10px;
                padding: 12px;
            }
            QFrame:hover {
                border-color: #8B5CF6;
                background-color: #1F1F1F;
            }
        """)
        c_layout = QVBoxLayout(card)
        
        t_label = QLabel(title)
        t_label.setStyleSheet("color: #F9FAFB; font-weight: 700; font-size: 13px;")
        c_layout.addWidget(t_label)
        
        d_label = QLabel(desc)
        d_label.setWordWrap(True)
        d_label.setStyleSheet("color: #9CA3AF; font-size: 11px;")
        c_layout.addWidget(d_label)
        
        btn = QPushButton("Apply Style")
        btn.setObjectName("PrimaryButton")
        btn.clicked.connect(lambda: self.suggestion_selected.emit({"style": title}))
        c_layout.addWidget(btn)
        
        self.list_layout.addWidget(card)
