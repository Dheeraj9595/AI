# Text Processing API

A FastAPI application that provides text summarization, grammar correction, and entity extraction features by consuming an external AI API.

## Features

1. **Summarize Text** - Generate concise summaries of text
2. **Grammar Correction** - Correct grammatical errors and improve text clarity
3. **Entity Extraction** - Extract named entities (persons, organizations, locations, dates, etc.) from text

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up environment variables:
```bash
cp .env.example .env
# Edit .env and update API_TOKEN if needed
```

## Running the Application

Start the server:
```bash
uvicorn main:app --reload
```

Or using Python directly:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Endpoints

### 1. Summarize Text
**POST** `/summarize`

Request body:
```json
{
  "text": "Your text to summarize here..."
}
```

Response:
```json
{
  "result": "Summarized text...",
  "success": true
}
```

### 2. Grammar Correction
**POST** `/grammar-correction`

Request body:
```json
{
  "text": "Text with grammer erors to correct..."
}
```

Response:
```json
{
  "result": "Text with grammar errors corrected...",
  "success": true
}
```

### 3. Entity Extraction
**POST** `/entity-extraction`

Request body:
```json
{
  "text": "John Smith works at Microsoft in Seattle. He will visit New York on January 15th, 2024."
}
```

Response:
```json
{
  "result": "Entities extracted by category:\n- Person: John Smith\n- Organization: Microsoft\n- Location: Seattle, New York\n- Date: January 15th, 2024",
  "success": true
}
```

## Example Usage

### Using curl

**Summarize:**
```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Long text to summarize here..."}'
```

**Grammar Correction:**
```bash
curl -X POST "http://localhost:8000/grammar-correction" \
  -H "Content-Type: application/json" \
  -d '{"text": "This text has some grammer erors."}'
```

**Entity Extraction:**
```bash
curl -X POST "http://localhost:8000/entity-extraction" \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple Inc. was founded by Steve Jobs in Cupertino, California."}'
```

### Using Python requests

```python
import requests

# Summarize
response = requests.post(
    "http://localhost:8000/summarize",
    json={"text": "Your text here..."}
)
print(response.json())

# Grammar correction
response = requests.post(
    "http://localhost:8000/grammar-correction",
    json={"text": "Text with erors."}
)
print(response.json())

# Entity extraction
response = requests.post(
    "http://localhost:8000/entity-extraction",
    json={"text": "Elon Musk is the CEO of SpaceX, located in Hawthorne, California."}
)
print(response.json())
```

## Configuration

The API token can be set via:
1. Environment variable `API_TOKEN` (recommended for production)
2. Default value in code (for development)

To use environment variables, create a `.env` file:
```
API_TOKEN=your_token_here
```
