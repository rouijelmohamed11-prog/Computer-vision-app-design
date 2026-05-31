# NLP Deep Dive: From Text to Design

The intelligence of VisionStudioAI lies in its ability to translate natural language into aesthetic design decisions. This is handled by a sophisticated pipeline within the `nlp/` module.

## 1. Semantic Parsing (`nlp/semantic_parser.py`)

The first step in the pipeline is the **Semantic Parser**. It uses a keyword-based approach reinforced by regular expressions to categorize user input.

### Vocabulary Mapping
The parser understands three main categories of information:

| Category | Keywords |
| :--- | :--- |
| **Styles** | Minimal, Cyberpunk, Luxury, Brutalist, Retro |
| **Emotions** | Energetic, Calm, Dark, Vibrant |
| **Design Types** | Poster, Banner, Social Media |

### Parsing Logic
When a user types "Create a dark cyberpunk banner", the parser:
1.  Converts text to lowercase.
2.  Identifies "dark" as an **Emotion**.
3.  Identifies "cyberpunk" as a **Style**.
4.  Identifies "banner" as a **Design Type**.

## 2. Context Memory (`nlp/context_memory.py`)

VisionStudioAI maintains a **Stateful Context**. This means the AI remembers what you were working on earlier in the session.

*   **Persistence**: If you change the style to "Luxury", the AI remembers this style for subsequent commands until you reset it or explicitly change it.
*   **State Tracking**: It tracks the current design type, active style, mood, and design parameters.

## 3. AI Reasoning Engine (`nlp/ai_reasoning.py`)

This is the decision-making core. It maps high-level concepts (like "Cyberpunk") to low-level design attributes.

### Aesthetic Rules
Each style is associated with a set of concrete actions:

*   **Luxury**: Employs serif fonts, increases white space for a "premium" feel, and uses dark palettes.
*   **Cyberpunk**: Uses bold, futuristic fonts and triggers neon glow effects with high-contrast colors.
*   **Minimal**: Strips away clutter, maximizes white space, and uses neutral sans-serif typography.

## 4. Response Generation (`nlp/response_generator.py`)

To make the interaction feel natural, the system generates human-like feedback. Instead of just "Success", it might say:
> *"Transforming your banner into a high-tech cyberpunk experience with dynamic neon accents."*

## 5. Design Language Engine (`nlp/design_language_engine.py`)

The `DesignLanguageEngine` is the orchestrator that ties all the above components together. It processes the raw command and returns a structured JSON object that the **Core Engine** can use to modify the canvas.
