from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for /ai/chat endpoint."""
    
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User message in Hausa or English"
    )


class ChatResponse(BaseModel):
    """Response schema for /ai/chat endpoint."""
    
    response: str = Field(..., description="AI response from Gemini")
    language: str = Field(
        default="auto",
        description="Detected language (hausa, english, or mixed)"
    )
