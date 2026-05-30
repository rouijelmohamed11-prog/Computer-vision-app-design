class ResponseGenerator:
    def generate(self, structured_output):
        style = structured_output["style"]["primary"]
        
        responses = {
            "luxury": f"I've refined your {structured_output['design_type']} with a luxury aesthetic, focusing on elegance and sophisticated white space.",
            "cyberpunk": f"Transforming your {structured_output['design_type']} into a high-tech cyberpunk experience with dynamic neon accents.",
            "minimal": f"Applying a clean, minimal approach to your {structured_output['design_type']} to emphasize simplicity and clarity."
        }
        
        return responses.get(style, "I've applied the requested modifications to your design.")
