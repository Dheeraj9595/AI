from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import httpx
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Text Processing API",
    description="API for text summarization, grammar correction, entity extraction, image and video generation",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Configuration
API_URL = "https://dheeraj9595.dheeraj-pandey.workers.dev/"
API_URL_IMAGE = "https://round-river-1dd8.dheeraj-pandey.workers.dev/"
API_TOKEN = os.getenv("API_TOKEN", "")
BYTZ_API_TOKEN = os.getenv("bytz_api_token", os.getenv("BYTZ_API_TOKEN", ""))
BYTZ_VIDEO_URL = "https://api.bytez.com/models/v2/ali-vilab/text-to-video-ms-1.7b"



# Request Models
class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Text to summarize", min_length=1)


class GrammarCorrectionRequest(BaseModel):
    text: str = Field(..., description="Text to correct grammar for", min_length=1)

class PolishText(BaseModel):
    text: str = Field(..., description="Text to polish and refactor", min_length=10)

class EntityExtractionRequest(BaseModel):
    text: str = Field(..., description="Text to extract entities from", min_length=1)

class EntityExtractionRequest1(BaseModel):
    text: str = Field(..., description="Text to extract entities from", min_length=5)


class ImageGenerationRequest(BaseModel):
    description: str = Field(..., description="Description of the image to generate", min_length=5)


class VideoGenerationRequest(BaseModel):
    text: str = Field(..., description="Text description for video generation", min_length=3)

# Response Models
class APIResponse(BaseModel):
    result: str = Field(..., description="Processed text result")
    success: bool = Field(default=True, description="Operation success status")


# Helper function to call external API
async def call_external_api(prompt: str, system_prompt: str) -> str:
    """
    Call the external API with the given prompt and system prompt.
    
    Args:
        prompt: The main prompt/question
        system_prompt: The system prompt to set the AI behavior
    
    Returns:
        The response text from the API
    
    Raises:
        HTTPException: If the API call fails
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    payload = {
        "prompt": prompt,
        "systemPrompt": system_prompt
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(API_URL, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            # Handle different possible response formats
            if isinstance(result, dict):
                if "response" in result:
                    return result["response"]
                elif "result" in result:
                    return result["result"]
                elif "text" in result:
                    return result["text"]
                elif "message" in result:
                    return result["message"]
                else:
                    # Return the whole dict as string if we can't find a specific field
                    return str(result)
            elif isinstance(result, str):
                return result
            else:
                return str(result)
                
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout - external API took too long to respond")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"External API error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


from fastapi import HTTPException
import httpx
import base64

async def call_external_api_for_image(prompt: str):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                API_URL_IMAGE,
                json=payload,
                headers=headers
            )
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")

            # 🟢 CASE 1: Binary image
            if content_type.startswith("image/"):
                return {
                    "type": "binary_image",
                    "content_type": content_type,
                    "image_bytes": response.content
                }

            # 🟢 CASE 2 & 3: JSON response
            data = response.json()

            if "image_url" in data:
                return {
                    "type": "image_url",
                    "url": data["image_url"]
                }

            if "image" in data:
                # base64 image
                image_bytes = base64.b64decode(data["image"])
                return {
                    "type": "base64_image",
                    "image_bytes": image_bytes
                }

            raise HTTPException(
                status_code=500,
                detail="Unsupported image response format"
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Image generation API timed out"
        )

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )


@app.get("/")
async def root():
    """Serve the frontend HTML"""
    return FileResponse("static/index.html")


@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Text Processing API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "summarize": "/summarize",
            "grammar-correction": "/grammar-correction",
            "entity-extraction": "/entity-extraction",
            "polish-text": "/polish-text",
            "generate-image": "/generate-image",
            "generate-video": "/generate-video",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Render and monitoring"""
    return {
        "status": "healthy",
        "service": "Text Processing API",
        "version": "1.0.0"
    }


@app.post("/summarize", response_model=APIResponse)
async def summarize_text(request: SummarizeRequest):
    """
    Summarize the given text.
    
    Args:
        request: Contains the text to summarize
    
    Returns:
        APIResponse with the summarized text
    """
    system_prompt = "You are a helpful assistant specialized in summarizing text. Provide a concise and clear summary of the given text."
    
    prompt = f"Please summarize the following text:\n\n{request.text}"
    
    try:
        result = await call_external_api(prompt, system_prompt)
        return APIResponse(result=result, success=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to summarize text: {str(e)}")

@app.post("/polish", response_model=APIResponse)
@app.post("/polish-text", response_model=APIResponse)
async def polish(request: PolishText):
    """
    Polish the sentence and correct the formate of the sentence

    Args:
        request: Contains the text to Polish

    Returns:
        PolishText with the reformated text    
    """

    system_prompt = "Polish the language, correct the grammar, and reformat the following sentence to sound clear and professional."

    prompt = f"Please Polish the sentence and improve the following text:\n\n{request.text}\n\nReturn only the corrected version without additional explanations."

    try:
        result = await call_external_api(prompt, system_prompt)
        return APIResponse(result=result, success=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to polish sentence: {str(e)}")
        
                
@app.post("/grammar-correction", response_model=APIResponse)
async def correct_grammar(request: GrammarCorrectionRequest):
    """
    Correct grammar and improve the given text.
    
    Args:
        request: Contains the text to correct
    
    Returns:
        APIResponse with the corrected text
    """
    system_prompt = "You are a helpful assistant specialized in grammar correction. Correct any grammatical errors, improve sentence structure, and enhance clarity while maintaining the original meaning and style."
    
    prompt = f"Please correct the grammar and improve the following text:\n\n{request.text}\n\nReturn only the corrected version without additional explanations."
    
    try:
        result = await call_external_api(prompt, system_prompt)
        return APIResponse(result=result, success=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to correct grammar: {str(e)}")


@app.post("/entity-extraction", response_model=APIResponse)
async def extract_entities(request: EntityExtractionRequest):
    """
    Extract named entities from the given text.
    
    Identifies and extracts entities such as:
    - Person names
    - Organizations
    - Locations (cities, countries, etc.)
    - Dates and times
    - Money amounts
    - Other relevant entities
    
    Args:
        request: Contains the text to extract entities from
    
    Returns:
        APIResponse with extracted entities in a structured format
    """
    system_prompt = "You are a helpful assistant specialized in Named Entity Recognition (NER). Extract all named entities from the given text and organize them by category (Person, Organization, Location, Date, Money, etc.). Provide a clear and structured list of all entities found."
    
    prompt = f"Please extract all named entities from the following text and organize them by category:\n\n{request.text}\n\nProvide a structured list showing entity type and the extracted entities."
    
    try:
        result = await call_external_api(prompt, system_prompt)
        return APIResponse(result=result, success=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract entities: {str(e)}")

import re

def parse_entities(llm_text: str) -> dict[str, list[str]]:
    entities = {}
    current_key = None

    for line in llm_text.splitlines():
        line = line.strip()

        # Match entity header like **Person**
        header_match = re.match(r"\*\*(.+?)\*\*", line)
        if header_match:
            current_key = header_match.group(1)
            entities[current_key] = []
            continue

        # Match entity value like * Dheeraj
        if line.startswith("*") and current_key:
            value = line.lstrip("*").strip()
            entities[current_key].append(value)

    return entities


@app.post("/entity-dict", response_model=APIResponse)
async def extract_entities(request: EntityExtractionRequest):
    system_prompt = (
        "You are a helpful assistant specialized in Named Entity Recognition (NER). "
        "Extract all named entities from the given text and organize them by category "
        "(Person, Organization, Location, Date, Money, etc.). "
        "Provide a clear and structured list of all entities found."
    )

    prompt = (
        "Please extract all named entities from the following text and organize them by category:\n\n"
        f"{request.text}\n\n"
        "Provide a structured list showing entity type and the extracted entities."
    )

    try:
        result = await call_external_api(prompt, system_prompt)
        result = parse_entities(result)
        return APIResponse(result=str(result), success=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract entities: {str(e)}"
        )





from fastapi.responses import Response

@app.post("/generate-image")
async def generate_image(request: ImageGenerationRequest):
    """
    Generate an image from a text description.
    
    Args:
        request: Contains the description of the image to generate
    
    Returns:
        JSON with the image URL (as data URI)
    """
    try:
        result = await call_external_api_for_image(request.description)
        
        # Convert image bytes to base64 data URI
        import base64
        image_base64 = base64.b64encode(result["image_bytes"]).decode('utf-8')
        data_uri = f"data:{result['content_type']};base64,{image_base64}"
        
        return {
            "success": True,
            "image_url": data_uri,
            "description": request.description
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate image: {str(e)}")


async def call_bytez_video_api(text: str):
    """Call Bytez API for text-to-video generation."""
    if not BYTZ_API_TOKEN:
        raise HTTPException(status_code=500, detail="Bytez API token not configured. Set bytz_api_token in .env")
    
    headers = {
        "Authorization": BYTZ_API_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {"text": text}
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                BYTZ_VIDEO_URL,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            
            content_type = response.headers.get("content-type", "")
            
            # Binary video response
            if "video" in content_type or "octet-stream" in content_type or content_type.startswith("video/"):
                return {
                    "type": "binary",
                    "content_type": content_type,
                    "video_bytes": response.content
                }
            
            # JSON response
            data = response.json()
            error = data.get("error")
            if error:
                raise HTTPException(status_code=500, detail=str(error))
            
            output = data.get("output")
            if output is None:
                raise HTTPException(status_code=500, detail="No output in API response")
            
            # output can be: URL string, base64 string, or object with url/base64
            if isinstance(output, str):
                if output.startswith("http"):
                    return {"type": "url", "video_url": output}
                if output.startswith("data:"):
                    return {"type": "data_uri", "video_url": output}
                try:
                    video_bytes = base64.b64decode(output)
                    return {
                        "type": "base64",
                        "video_bytes": video_bytes,
                        "content_type": "video/mp4"
                    }
                except Exception:
                    raise HTTPException(status_code=500, detail="Could not decode video output")
            
            if isinstance(output, dict):
                if "url" in output:
                    return {"type": "url", "video_url": output["url"]}
                if "video_url" in output:
                    return {"type": "url", "video_url": output["video_url"]}
                if "base64" in output:
                    video_bytes = base64.b64decode(output["base64"])
                    return {
                        "type": "base64",
                        "video_bytes": video_bytes,
                        "content_type": output.get("content_type", "video/mp4")
                    }
            
            raise HTTPException(status_code=500, detail="Unsupported video response format")
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Video generation timed out (may take 1-2 minutes)")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")


@app.post("/generate-video")
async def generate_video(request: VideoGenerationRequest):
    """
    Generate a video from text description using Bytez API.
    
    Args:
        request: Contains the text description for the video
    
    Returns:
        JSON with video_url (data URI or URL) and success status
    """
    try:
        result = await call_bytez_video_api(request.text)
        
        if result["type"] == "url":
            return {
                "success": True,
                "video_url": result["video_url"],
                "description": request.text
            }
        
        if result["type"] == "data_uri":
            return {
                "success": True,
                "video_url": result["video_url"],
                "description": request.text
            }
        
        if result["type"] in ("binary", "base64"):
            video_bytes = result["video_bytes"]
            content_type = result.get("content_type", "video/mp4")
            video_base64 = base64.b64encode(video_bytes).decode("utf-8")
            data_uri = f"data:{content_type};base64,{video_base64}"
            return {
                "success": True,
                "video_url": data_uri,
                "description": request.text
            }
        
        raise HTTPException(status_code=500, detail="Unsupported response format")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate video: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

#updated code