import re
import json

class SemanticParser:
    # Design vocabulary mapping
    VOCAB = {
        "styles": {
            "minimal": ["minimal", "clean", "simple", "minimalist"],
            "cyberpunk": ["cyberpunk", "neon", "high-tech", "futuristic", "matrix"],
            "luxury": ["luxury", "gold", "premium", "elegant", "sophisticated"],
            "brutalist": ["brutalist", "bold", "raw", "concrete"],
            "retro": ["retro", "vintage", "70s", "80s", "nostalgic"]
        },
        "emotions": {
            "energetic": ["energetic", "dynamic", "fast", "active"],
            "calm": ["calm", "relaxing", "peaceful", "serene"],
            "dark": ["dark", "mysterious", "shadowy"],
            "vibrant": ["vibrant", "bright", "colorful", "popping"]
        },
        "design_types": {
            "poster": ["poster", "flyer", "print"],
            "banner": ["banner", "web", "header"],
            "social_media": ["instagram", "post", "tiktok", "story"]
        }
    }

    def parse(self, text):
        text = text.lower()
        analysis = {
            "style": self._extract_category(text, self.VOCAB["styles"]),
            "mood": self._extract_list(text, self.VOCAB["emotions"]),
            "design_type": self._extract_category(text, self.VOCAB["design_types"]),
            "raw_tokens": re.findall(r'\w+', text)
        }
        return analysis

    def _extract_category(self, text, mapping):
        for category, keywords in mapping.items():
            if any(k in text for k in keywords):
                return category
        return None

    def _extract_list(self, text, mapping):
        found = []
        for category, keywords in mapping.items():
            if any(k in text for k in keywords):
                found.append(category)
        return found
