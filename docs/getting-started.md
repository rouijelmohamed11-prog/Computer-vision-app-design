# Getting Started

Follow these steps to set up VisionStudioAI on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**
- **Node.js 18+** (for the web dashboard)
- **Git**

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rouijelmohamed11-prog/Computer-vision-app-design.git
cd "app design"
```

### 2. Desktop App Setup (Python)

Create and activate a virtual environment:

=== "Windows"

    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

=== "macOS/Linux"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 3. Web Dashboard Setup (Node.js)

Navigate to the frontend directory and install dependencies:

```bash
cd studio-frontend
npm install
```

## Running the Application

### Launch Desktop Studio

From the project root (with the virtual environment active):

```bash
python main.py
```

### Start Web Dashboard

From the `studio-frontend` directory:

```bash
npm run dev
```

## Assets Configuration (Optional)

For a full library of assets, you can download the assets folder from [this link](https://drive.google.com/drive/u/0/folders/1OkSfIJ-k5Wgk1gqqWLVMpoABt8Ti2XWZ) and place it in the project root directory.
