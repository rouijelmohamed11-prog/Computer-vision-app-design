import unittest
from nlp.design_language_engine import DesignLanguageEngine

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DesignLanguageEngine()

    def test_intelligent_reasoning(self):
        result = self.engine.process_command("Create a luxury poster")
        output = result["json"]
        self.assertEqual(output["style"]["primary"], "luxury")
        self.assertIn("add_white_space", output["actions"])
        self.assertIn("luxury", result["message"])

        result = self.engine.process_command("Make it cyberpunk")
        output = result["json"]
        self.assertEqual(output["style"]["primary"], "cyberpunk")
        self.assertIn("apply_glow_effect", output["actions"])
        self.assertIn("cyberpunk", result["message"])

if __name__ == "__main__":
    unittest.main()
