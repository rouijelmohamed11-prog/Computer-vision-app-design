# Computer-vision-app-design

VisionStudioAI is a modular application integrating advanced NLP, vision processing, and frontend components to provide an AI-driven design environment.

## Project Structure and File Roles

- `main.py`: The main entry point of the application.
- `requirements.txt`: List of required Python dependencies.
- `assets/`: Contains image assets used throughout the project.(download the file from https://drive.google.com/drive/u/0/folders/1OkSfIJ-k5Wgk1gqqWLVMpoABt8Ti2XWZ and name it assets)
- `core/`: Core engine logic for the application.
    - `engine.py`: Main execution engine.
    - `history.py`: Manages application state and history.
    - `objects.py`: Defines core data objects.
- `nlp/`: NLP modules for understanding and generating content.
    - `ai_reasoning.py`: Logic for reasoning and decision-making.
    - `context_memory.py`: Manages context across sessions.
    - `design_language_engine.py`: Processes design-specific language tasks.
    - `intent.py`: Identifies user intent.
    - `parser.py`: General-purpose text parser.
    - `response_generator.py`: Generates textual responses.
    - `semantic_parser.py`: Semantic analysis of inputs.
- `studio-frontend/`: Frontend application codebase.
- `tests/`: Suite of unit and integration tests.
- `ui/`: User interface components.
- `vision/`: Functionality related to image analysis and processing.


## Documentation

This project uses [MkDocs](https://www.mkdocs.org/) for documentation.

### Build and View Locally

1. Install requirements:
   ```bash
   pip install mkdocs mkdocs-material mkdocstrings[python]
   ```
2. Build and serve the documentation:
   ```bash
   mkdocs serve
   ```
3. Open `http://127.0.0.1:8000/` in your browser.

The documentation is configured for [Read the Docs](https://readthedocs.org/).

### Installation

1.  **Create a Virtual Environment:**
    Open a terminal in the project root directory and run:
    ```bash
    python -m venv .venv
    ```

2.  **Activate the Virtual Environment:**
    - On Windows:
      ```bash
      .\.venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Install modules and assets:**
    in folders go to studio-frontennd and installs modules
    ```bash
    npm install 
    ```
    then install asstes file from https://drive.google.com/drive/u/0/folders/1OkSfIJ-k5Wgk1gqqWLVMpoABt8Ti2XWZ (optional for library assets) rename the file to assets and put it in the folder workspace
### Running the Application

Once everything installed and the virtual environment is active, you can run the main application:

```bash
python main.py
```
