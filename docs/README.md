# Text Processing API

A FastAPI application that provides text summarization, grammar correction, and entity extraction features by consuming an external AI API.

## Features

1. **Summarize Text** - Generate concise summaries of text
2. **Polish Text** - Improve grammar, clarity, and style of your writing
3. **Generate Images** - Create stunning images from text descriptions
4. **Grammar Correction** - Correct grammatical errors and improve text clarity
5. **Entity Extraction** - Extract named entities (persons, organizations, locations, dates, etc.) from text

## Live Demo

Access the beautiful web interface at `http://localhost:8000` after starting the server.

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

### Quick Start (Recommended)
```bash
./run.sh
```

### Manual Start
```bash
# Using uvicorn
uvicorn main:app --reload

# Or using Python directly
python3 main.py
```

The application will be available at `http://localhost:8000`

## Web Interface

The application includes a beautiful, modern web interface with:
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Real-time Processing** - Instant feedback and results
- **Beautiful UI** - Modern gradient design with smooth animations
- **Easy to Use** - Intuitive interface with clear instructions

Access the web interface at: `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Web Interface:** `http://localhost:8000`
- **Interactive API docs:** `http://localhost:8000/docs`
- **Alternative docs:** `http://localhost:8000/redoc`
- **API Info:** `http://localhost:8000/api`

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

## Deployment to Render

This application is ready to deploy on Render. Follow these steps:

### Option 1: Using Render Dashboard

1. **Create a new Web Service** on Render
2. **Connect your repository** (GitHub/GitLab/Bitbucket)
3. **Configure the service:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3
4. **Add Environment Variables:**
   - `API_TOKEN`: Your API token (e.g., `pridrEspigUVoYlfefruyUPRobr$rEpIprucRUspirlxLYiTA5LRakepiy9qibic`)
   - `PORT`: Automatically set by Render (no need to set manually)
5. **Deploy!**

### Option 2: Using render.yaml (Infrastructure as Code)

If you have `render.yaml` in your repository:

1. **Create a new Blueprint** on Render
2. **Connect your repository**
3. **Render will automatically detect and use `render.yaml`**
4. **Add the `API_TOKEN` environment variable** in the Render dashboard
5. **Deploy!**

### Environment Variables on Render

Make sure to set the following environment variable in your Render service:
- `API_TOKEN`: Your external API authentication token

The `PORT` environment variable is automatically provided by Render - you don't need to set it manually.

### Health Check

The application includes a root endpoint (`/`) that can be used as a health check endpoint in Render.

### Post-Deployment

After deployment, your API will be available at:
- `https://your-service-name.onrender.com`
- API Documentation: `https://your-service-name.onrender.com/docs`
