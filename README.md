# AI Studio

A beautiful, full-stack AI-powered application for text processing and image generation.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the application
./run.sh

# Or manually
uvicorn main:app --reload
```

Then visit: **http://localhost:8000**

## ✨ Features

- 📝 **Text Summarization** - Get concise summaries of long content
- ✨ **Text Polishing** - Improve grammar, clarity, and style
- 🖼️ **Image Generation** - Create AI-generated images from text
- ✏️ **Grammar Correction** - Fix grammatical errors
- 🏷️ **Entity Extraction** - Extract named entities from text

## 📚 Documentation

All documentation is located in the [`docs/`](docs/) folder:

- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[docs/INDEX.md](docs/INDEX.md)** - Documentation index and guide
- **[docs/FEATURES.md](docs/FEATURES.md)** - Detailed feature documentation
- **[docs/FRONTEND.md](docs/FRONTEND.md)** - Frontend architecture
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Production deployment guide
- **[docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)** - Project overview

## 🌐 Web Interface

Access the beautiful web interface at `http://localhost:8000` with:
- Modern gradient design
- Responsive layout
- Real-time processing
- Toast notifications
- Copy to clipboard

## 📖 API Documentation

Interactive API documentation available at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python, FastAPI, Uvicorn
- **Deployment:** Render.com ready

## 📁 Project Structure

```
ai_workerai/
├── docs/              # All documentation
├── static/            # Frontend files
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── main.py            # FastAPI backend
├── requirements.txt   # Dependencies
└── run.sh            # Quick start script
```

## 🔧 Environment Variables

Create a `.env` file with:

```
API_TOKEN=your_token_here
bytz_api_token=your_bytez_api_key
```

- `API_TOKEN` - For text processing (summarize, polish, etc.) and image generation
- `bytz_api_token` - For video generation (Bytez API)

## 🚀 Deployment

Ready to deploy on Render.com:

```bash
# See docs/DEPLOYMENT.md for detailed instructions
```

## 📞 Support

- Check [docs/QUICKSTART.md](docs/QUICKSTART.md) for common issues
- Review API docs at `/docs` endpoint
- See [docs/INDEX.md](docs/INDEX.md) for all documentation

## 📄 License

© 2026 AI Studio. All rights reserved.

---

**Built with ❤️ using FastAPI and modern web technologies**
