from core.objects import TextElement, ShapeElement
from PyQt5.QtGui import QColor

class DesignGenerator:
    def __init__(self, engine):
        self.engine = engine

    def generate_from_intent(self, intent):
        self.engine.elements.clear()
        
        design_type = intent["type"]
        style = intent["style"]
        keywords = intent.get("parameters", {}).get("keywords", [])
        
        # Base background
        bg_color = QColor(255, 255, 255)
        if style == "gaming":
            bg_color = QColor(20, 20, 20)
        elif style == "luxury":
            bg_color = QColor(30, 30, 30)
        
        bg = ShapeElement("rectangle", 0, 0, bg_color)
        bg.width = 800
        bg.height = 600
        self.engine.add_element(bg)

        # Title
        title_text = " ".join(keywords).title() or "Untitled Design"
        title_color = QColor(0, 0, 0)
        if style in ["gaming", "luxury"]:
            title_color = QColor(255, 215, 0) if style == "luxury" else QColor(0, 255, 255)
            
        title = TextElement(title_text, 100, 100, font_size=40, color=title_color)
        self.engine.add_element(title)

        # Subtitle
        subtitle = TextElement(design_type.upper(), 100, 160, font_size=20, color=title_color)
        self.engine.add_element(subtitle)

        # Add some shapes based on style
        if style == "minimalist":
            shape = ShapeElement("circle", 600, 400, QColor(200, 200, 200))
            self.engine.add_element(shape)
        elif style == "gaming":
            accent = ShapeElement("rectangle", 0, 550, QColor(255, 0, 255))
            accent.width = 800
            accent.height = 50
            self.engine.add_element(accent)

        self.engine.elements_changed.emit()
