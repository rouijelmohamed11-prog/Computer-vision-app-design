import re
import json

class NLPParser:
    TYPES = {
        "poster": ["poster", "flyer", "wall art"],
        "banner": ["banner", "header", "cover"],
        "logo": ["logo", "icon", "brand"],
        "thumbnail": ["thumbnail", "youtube", "yt"]
    }
    
    STYLES = {
        "gaming": ["gaming", "gamer", "esports", "neon"],
        "minimalist": ["minimalist", "clean", "simple", "minimal"],
        "modern": ["modern", "sleek", "corporate"],
        "luxury": ["luxury", "gold", "premium", "elegant"]
    }

    def parse_prompt(self, prompt: str):
        prompt = prompt.lower()
        
        # Detect Intent
        action = "create"
        if "color" in prompt or "change" in prompt:
            action = "style_change"
        elif "filter" in prompt or "effect" in prompt:
            action = "filter_apply"
        
        design_type = "poster"
        for key, aliases in self.TYPES.items():
            if any(alias in prompt for alias in aliases):
                design_type = key
                break
                
        style = "modern"
        for key, aliases in self.STYLES.items():
            if any(alias in prompt for alias in aliases):
                style = key
                break

        intent = {
            "action": action,
            "type": design_type,
            "style": style,
            "parameters": {
                "keywords": re.findall(r'\w+', prompt)
            }
        }
        return intent
