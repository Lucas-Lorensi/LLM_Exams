# Medical Exam PDF Parser

This application extracts medical examination data from PDF reports and converts it into structured JSON format using a local LLM.

## Features

- Upload medical lab PDFs via a simple web interface
- Extract text content from PDFs automatically
- Process extracted text using DeepSeek 8B language model
- Parse results into structured JSON for easy data analysis
- Local processing for data privacy

## Requirements

- Python 3.10 or newer
- Ollama (for running the LLM locally)
- 8+ GB RAM recommended for the language model
- Approximately 5GB free disk space for the LLM

## Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/medical-exam-parser.git
cd medical-exam-parser
```

### Step 2: Set Up Python Virtual Environment

Create and activate a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

If the requirements.txt file doesn't exist, create it with these contents:

```
gradio
pdfplumber
```

### Step 4: Install Ollama

Download and install Ollama based on your operating system:

- **Windows**: Download from [Ollama's official website](https://ollama.ai/download)
- **macOS**: 
  ```bash
  curl -fsSL https://ollama.ai/install.sh | sh
  ```
- **Linux**:
  ```bash
  curl -fsSL https://ollama.ai/install.sh | sh
  ```

### Step 5: Download the DeepSeek Language Model

Pull the DeepSeek 8B model using Ollama:

```bash
ollama pull deepseek:8b-r1
```

This will download approximately 4.5GB of model data. The download time will vary based on your internet connection.

## Running the Application

From the project directory with your virtual environment activated:

```bash
python app.py
```

This will start the Gradio interface, typically accessible at `http://127.0.0.1:7860` in your web browser.

## How to Use

1. Open the application in your web browser
2. Upload a medical lab PDF report through the file upload interface
3. Wait for the processing to complete (this may take 10-30 seconds depending on your hardware)
4. View the extracted information in structured JSON format
5. The results include exam name, value, unit of measurement, reference range, and observations about whether values are within normal ranges

## Project Structure

- `app.py`: Main application file with Gradio interface
- `extractor.py`: Functions for PDF text extraction
- `llm_config/prompt.txt`: Template for the LLM prompt
- `uploads/`: Directory where uploaded PDFs are temporarily stored

## Troubleshooting

- **JSON Parsing Errors**: Sometimes the LLM may not output perfectly formatted JSON. The app attempts to extract any valid JSON object within the response, but occasionally manual correction might be needed.
- **Ollama Issues**: If Ollama fails to start, ensure the service is running with `ollama serve` in a separate terminal.
- **Memory Issues**: If you encounter out-of-memory errors, close other applications or consider using a smaller language model.
- **PDF Extraction Problems**: Some PDFs with unusual formatting or scanned as images may not extract correctly. The app works best with digitally generated PDFs.

## License

[Your License Information Here]

## Acknowledgements

- This project uses [DeepSeek](https://github.com/deepseek-ai/DeepSeek-Coder) for natural language processing
- PDF extraction is handled by [pdfplumber](https://github.com/jsvine/pdfplumber)
- Web interface built with [Gradio](https://gradio.app/)