"""
AI-powered features API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from uuid import UUID
import structlog

from app.services.ai_service import AIService

logger = structlog.get_logger(__name__)
router = APIRouter()


class ChatRequest(BaseModel):
    """Request schema for AI chat."""
    message: str = Field(..., min_length=1, max_length=1000)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    """Response schema for AI chat."""
    response: str
    context: Dict[str, Any]


class PersonalityAssessmentRequest(BaseModel):
    """Request schema for personality assessment."""
    responses: Dict[str, Any]


class PersonalityAssessmentResponse(BaseModel):
    """Response schema for personality assessment."""
    profile: Dict[str, Any]
    recommendations: list[str]


def get_ai_service() -> AIService:
    """Dependency to get AIService instance."""
    return AIService()


# TODO: Add authentication dependency
def get_current_user_id() -> UUID:
    """Temporary mock user ID - replace with real authentication."""
    return UUID("00000000-0000-0000-0000-000000000001")


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    ai_service: AIService = Depends(get_ai_service),
    user_id: UUID = Depends(get_current_user_id)
):
    """Chat with AI assistant using personality-aware responses."""
    try:
        # For now, use default personality profile
        # TODO: Fetch user's actual personality profile from database
        default_personality = {
            "warm_candid": 0,
            "motivation_direction": 0,
            "proactive_reactive": 0,
            "reassurance_needs": 0,
            "language_variety": 0
        }
        
        response = await ai_service.generate_personality_response(
            request.message,
            default_personality,
            request.context
        )
        
        logger.info("AI chat completed", user_id=str(user_id))
        return ChatResponse(
            response=response,
            context=request.context
        )
    except Exception as e:
        logger.error("AI chat failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate AI response")


@router.post("/personality-assessment", response_model=PersonalityAssessmentResponse)
async def assess_personality(
    request: PersonalityAssessmentRequest,
    user_id: UUID = Depends(get_current_user_id)
):
    """Assess user personality based on responses."""
    try:
        # Simple personality assessment logic
        # TODO: Implement proper personality assessment algorithm
        
        profile = {
            "warm_candid": 0,
            "motivation_direction": 0,
            "proactive_reactive": 0,
            "reassurance_needs": 0,
            "language_variety": 0
        }
        
        recommendations = [
            "Complete the full personality assessment for better AI responses",
            "Try using natural language task creation",
            "Set up your daily schedule template"
        ]
        
        logger.info("Personality assessment completed", user_id=str(user_id))
        return PersonalityAssessmentResponse(
            profile=profile,
            recommendations=recommendations
        )
    except Exception as e:
        logger.error("Personality assessment failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to assess personality")


@router.get("/status")
async def get_ai_status():
    """Get AI service status and capabilities."""
    ai_service = AIService()
    
    return {
        "openai_available": ai_service.client is not None,
        "features": {
            "task_analysis": True,
            "semantic_search": ai_service.client is not None,
            "personality_responses": ai_service.client is not None,
            "scheduling_decisions": ai_service.client is not None
        },
        "models": {
            "chat": "gpt-4-turbo-preview" if ai_service.client else "fallback",
            "embeddings": "text-embedding-ada-002" if ai_service.client else "fallback"
        }
    } 