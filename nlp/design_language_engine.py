import json
from nlp.context_memory import ContextMemory
from nlp.semantic_parser import SemanticParser
from nlp.ai_reasoning import AIReasoning
from nlp.response_generator import ResponseGenerator

class DesignLanguageEngine:
    def __init__(self):
        self.memory = ContextMemory()
        self.parser = SemanticParser()
        self.reasoning = AIReasoning()
        self.generator = ResponseGenerator()

    def process_command(self, user_input):
        # 1. Parse Input
        analysis = self.parser.parse(user_input)
        
        # 2. Update Context
        self.memory.update_state({
            "last_user_prompt": user_input,
            "current_design_type": analysis["design_type"] or self.memory.get_state()["current_design_type"],
            "active_style": analysis["style"] or self.memory.get_state()["active_style"],
            "mood": analysis["mood"]
        })
        
        # 3. Reasoning Layer
        state = self.memory.get_state()
        reasoning_output = self.reasoning.infer_actions(state)
        
        # 4. Construct Response
        structured_response = {
            "intent": "style_transformation" if analysis["style"] else "modification",
            "design_type": state["current_design_type"],
            "style": {"primary": state["active_style"]},
            "mood": state["mood"],
            "layout": {"alignment": reasoning_output.get("alignment", "center")},
            "typography": {"font_style": reasoning_output.get("font_style", "default")},
            "actions": reasoning_output.get("actions", [])
        }
        
        # 5. Generate Human-like response
        message = self.generator.generate(structured_response)
        
        return {
            "json": structured_response,
            "message": message
        }
