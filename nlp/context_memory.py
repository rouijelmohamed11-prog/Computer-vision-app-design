class ContextMemory:
    def __init__(self):
        self.history = []
        self.state = {
            "current_design_type": None,
            "active_style": None,
            "mood": [],
            "last_user_prompt": None,
            "design_parameters": {}
        }

    def update_state(self, updates):
        self.state.update(updates)
        self.history.append(updates)

    def get_state(self):
        return self.state

    def reset(self):
        self.history = []
        self.state = {
            "current_design_type": None,
            "active_style": None,
            "mood": [],
            "last_user_prompt": None,
            "design_parameters": {}
        }
