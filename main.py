from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Text Processing API",
    description="API for text summarization, grammar correction, and entity extraction",
    version="1.0.0"
)

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
API_TOKEN = os.getenv("API_TOKEN", "")


# Request Models
class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Text to summarize", min_length=1)


class GrammarCorrectionRequest(BaseModel):
    text: str = Field(..., description="Text to correct grammar for", min_length=1)


class EntityExtractionRequest(BaseModel):
    text: str = Field(..., description="Text to extract entities from", min_length=1)


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


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Text Processing API",
        "version": "1.0.0",
        "endpoints": {
            "summarize": "/summarize",
            "grammar-correction": "/grammar-correction",
            "entity-extraction": "/entity-extraction"
        }
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
