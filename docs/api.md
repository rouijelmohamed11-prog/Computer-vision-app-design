# API Reference: Core Modules

This reference covers the primary classes and methods used across the VisionStudioAI Python codebase.

## Core Engine

### `core.engine.DesignEngine`
The central state manager for the canvas.

::: core.engine.DesignEngine
    options:
      show_root_heading: true
      show_source: true

### `core.history.HistoryManager`
Handles Undo and Redo operations.

::: core.history.HistoryManager
    options:
      show_root_heading: true

---

## NLP Engine

### `nlp.ai_reasoning.AIReasoning`
Maps aesthetic concepts to design rules.

::: nlp.ai_reasoning.AIReasoning
    options:
      show_root_heading: true

### `nlp.semantic_parser.SemanticParser`
Parses user intent from raw text.

::: nlp.semantic_parser.SemanticParser
    options:
      show_root_heading: true

---

## Vision Pipeline

### `vision.image_tools`
Utility functions for image manipulation.

::: vision.image_tools
    options:
      show_root_heading: true

### `vision.filters`
The core CV functions.

::: vision.filters
    options:
      show_root_heading: true
