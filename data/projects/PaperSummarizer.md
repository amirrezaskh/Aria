# Paper Summarizer

An intelligent academic paper summarization system that combines computer vision and natural language processing to extract, analyze, and summarize research papers from PDF format.

## Overview

This project provides an end-to-end solution for automatically summarizing academic papers by:
- Converting PDF pages to images
- Using object detection to identify different document elements (text, titles, figures, tables)
- Extracting text using OCR (Optical Character Recognition)
- Analyzing figures with vision-language models
- Generating comprehensive summaries using large language models

## Architecture

The system consists of two main components:

### 1. Client (`main.ipynb`)
A Jupyter notebook that handles:
- PDF processing and page extraction
- Object detection using Detectron2 with Faster R-CNN
- Text extraction using EasyOCR
- Figure extraction and processing
- Communication with the summarization server

### 2. Server (`server.py`)
A Flask-based API server that provides:
- Figure analysis using LLaVA (Large Language and Vision Assistant)
- Text summarization using Ollama with Llama 3.2
- Page-wise and full-paper summarization
- RESTful API endpoint for processing requests

## Features

- **Multi-modal Analysis**: Processes both text and visual elements (figures, tables)
- **Intelligent Object Detection**: Identifies different document components with 70% confidence threshold
- **OCR Text Extraction**: Supports English text recognition
- **Figure Understanding**: Uses vision-language models to describe and summarize figures
- **Hierarchical Summarization**: Creates page-level summaries before generating final paper summary
- **PDF Output**: Converts final summary to PDF format using Pandoc

## Requirements

### Python Dependencies
- `cv2` (OpenCV)
- `easyocr`
- `detectron2`
- `pdf2image`
- `requests`
- `numpy`
- `flask`
- `ollama`
- `transformers` (for LLaVA model)
- `tqdm`

### External Dependencies
- **Pandoc**: For converting Markdown summary to PDF
- **Faster R-CNN Model**: Pre-trained model file (`faster-rcnn.pth`)
- **Ollama**: For running Llama 3.2 model locally

### System Requirements
- **GPU**: Recommended for faster processing (CPU fallback available)
- **Memory**: Minimum 8GB RAM (16GB+ recommended for large papers)
- **Storage**: Space for model files and temporary image processing

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd paper-summarizer
   ```

2. **Install Python dependencies**
   ```bash
   pip install opencv-python easyocr detectron2 pdf2image requests numpy flask transformers tqdm
   ```

3. **Install Ollama**
   Follow instructions at [ollama.ai](https://ollama.ai) to install Ollama

4. **Install Pandoc**
   ```bash
   # macOS
   brew install pandoc
   
   # Ubuntu/Debian
   sudo apt-get install pandoc
   ```

5. **Download required models**
   - Place your Faster R-CNN model file as `faster-rcnn.pth` in the project directory
   - The LLaVA model will be downloaded automatically on first use

## Usage

### 1. Start the Server
```bash
python server.py
```
The server will start on `http://localhost:8000`

### 2. Process a Paper
1. Place your PDF file in the project directory as `paper.pdf`
2. Open and run the `main.ipynb` notebook
3. The system will:
   - Process each page of the PDF
   - Extract text and figures
   - Send data to the summarization server
   - Generate a comprehensive summary
   - Save the summary as both `summary.md` and `summary.pdf`

## Configuration

### Server Configuration
- **Host**: `0.0.0.0` (accepts external connections)
- **Port**: `8000`
- **Models**: LLaVA 1.5 7B, Llama 3.2

### Detection Configuration
- **Score Threshold**: 0.7 (70% confidence)
- **Classes**: text, title, list, table, figure
- **Model**: Faster R-CNN with ResNet-50 FPN backbone

## API Documentation

### POST `/summarize`
Processes paper content and returns a summary.

**Request:**
- **Files**: `figures` - Array of figure images (JPEG format)
- **Form Data**: 
  - `full_text`: JSON string containing extracted text from all pages
  - `figure_pages`: JSON string containing figure count per page

**Response:**
```json
{
  "summary": "Generated paper summary in Markdown format"
}
```

## Output Format

The generated summary includes:
- **Title of the Paper**
- **Problem Statement**
- **Methodology**
- **Key Findings & Results**
- **Conclusion & Implications**

## Performance Notes

- Processing time depends on paper length and complexity
- Figure analysis requires significant computational resources
- First run may be slower due to model downloads
- Consider using GPU acceleration for better performance

## Limitations

- Currently supports English text only
- Requires manual placement of PDF as `paper.pdf`
- Server URL is hardcoded in the notebook
- Limited to specific object detection classes

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgments

- **Detectron2**: For object detection capabilities
- **EasyOCR**: For text extraction
- **LLaVA**: For vision-language understanding
- **Ollama**: For local LLM inference
- **Transformers**: For model integration