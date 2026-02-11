# Quick Start Guide

Get up and running with AI Studio in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (optional, for cloning)

## Installation

### Step 1: Navigate to Project Directory
```bash
cd /home/ubox48/practice/ai_workerai
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables (Optional)
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API token
# API_TOKEN=your_token_here
```

### Step 4: Start the Server

**Option A: Quick Start Script (Recommended)**
```bash
./run.sh
```

**Option B: Manual Start**
```bash
uvicorn main:app --reload
```

**Option C: Python Direct**
```bash
python3 main.py
```

## Access the Application

Once the server is running, open your browser and visit:

- **Web Interface:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## Using the Web Interface

### 1. Summarize Text
1. Click on the "Summarize" tab
2. Paste your text in the textarea
3. Click "Summarize" button
4. View and copy the summary

### 2. Polish Text
1. Click on the "Polish Text" tab
2. Enter text that needs improvement
3. Click "Polish Text" button
4. Get professionally polished text

### 3. Generate Image
1. Click on the "Generate Image" tab
2. Describe the image you want
3. Click "Generate Image" button
4. View and download the generated image

## Using the API

### Example: Summarize Text
```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your long text here..."}'
```

### Example: Polish Text
```bash
curl -X POST "http://localhost:8000/polish-text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Text with grammer erors."}'
```

### Example: Generate Image
```bash
curl -X POST "http://localhost:8000/generate-image" \
  -H "Content-Type: application/json" \
  -d '{"description": "A beautiful sunset over mountains"}'
```

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, specify a different port:
```bash
uvicorn main:app --port 8080
```

### Module Not Found
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### API Token Error
Ensure your API_TOKEN is set in the environment:
```bash
export API_TOKEN="your_token_here"
```

Or add it to your `.env` file.

## Next Steps

- Explore the interactive API docs at `/docs`
- Read the full documentation in `README.md`
- Check deployment guide in `DEPLOYMENT.md`
- Learn about the frontend in `FRONTEND.md`

## Support

For issues or questions:
- Check the main `README.md`
- Review API documentation at `/docs`
- Check application logs for errors

## Features Overview

✅ **Summarize Text** - Get concise summaries  
✅ **Polish Text** - Improve writing quality  
✅ **Generate Images** - Create AI-generated images  
✅ **Grammar Correction** - Fix grammar errors  
✅ **Entity Extraction** - Extract named entities  

Enjoy using AI Studio! 🚀
