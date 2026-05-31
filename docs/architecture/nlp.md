# NLP Engine

The NLP Engine translates human language into design actions. It's a multi-stage pipeline that processes raw text to influence the canvas.

## NLP Pipeline

1.  **Parsing**: The `NLPParser` (`nlp/parser.py`) uses a combination of keyword extraction and regex to identify what the user wants to create (e.g., "Add a title", "Import an image").
2.  **Intent Identification**: The system determines the "Goal" of the user. Is it a creation task, a modification task, or a styling task?
3.  **Design Reasoning**: The `AIReasoning` module (`nlp/ai_reasoning.py`) applies aesthetic rules based on the detected style or mood.

## AI Reasoning Rules

The reasoning engine uses a rule-based system to define aesthetics:

```python
rules = {
    "minimal": {
        "font_style": "sans-serif light",
        "actions": ["remove_clutter", "maximize_white_space"],
        "alignment": "center"
    }
}
```

This allows the application to make "smart" decisions about layout and typography without requiring a complex neural network for every small design choice.
