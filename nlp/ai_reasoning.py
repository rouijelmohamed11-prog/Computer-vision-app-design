class AIReasoning:
    def __init__(self):
        # Maps aesthetic descriptors to concrete design actions
        self.rules = {
            "luxury": {
                "font_style": "serif elegant",
                "actions": ["add_white_space", "use_serif_font", "apply_dark_palette"],
                "alignment": "center"
            },
            "cyberpunk": {
                "font_style": "bold futuristic",
                "actions": ["apply_glow_effect", "increase_contrast", "use_neon_palette"],
                "alignment": "left"
            },
            "minimal": {
                "font_style": "sans-serif light",
                "actions": ["remove_clutter", "maximize_white_space", "use_neutral_palette"],
                "alignment": "center"
            }
        }

    def infer_actions(self, state):
        style = state.get("active_style")
        if style in self.rules:
            return self.rules[style]
        return {"actions": ["balance_composition"]}
