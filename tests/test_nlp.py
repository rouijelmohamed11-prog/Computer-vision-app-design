import unittest
from nlp.parser import NLPParser

class TestNLPParser(unittest.TestCase):
    def setUp(self):
        self.parser = NLPParser()

    def test_parse_gaming_poster(self):
        prompt = "Create a modern gaming poster for a tournament"
        intent = self.parser.parse_prompt(prompt)
        self.assertEqual(intent["type"], "poster")
        self.assertEqual(intent["style"], "gaming")
        self.assertIn("tournament", intent["keywords"])

    def test_parse_minimalist_logo(self):
        prompt = "Make a minimal logo for a startup"
        intent = self.parser.parse_prompt(prompt)
        self.assertEqual(intent["type"], "logo")
        self.assertEqual(intent["style"], "minimalist")
        self.assertIn("startup", intent["keywords"])

    def test_default_values(self):
        prompt = "Something random"
        intent = self.parser.parse_prompt(prompt)
        self.assertEqual(intent["type"], "poster") # Default
        self.assertEqual(intent["style"], "modern") # Default

if __name__ == '__main__':
    unittest.main()
