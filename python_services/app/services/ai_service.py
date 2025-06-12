"""
AI service for handling OpenAI integration and intelligent task analysis.
"""

from typing import Dict, Any, List, Optional
import json
import asyncio
from datetime import datetime

import structlog
from app.core.config import settings

logger = structlog.get_logger(__name__)


class AIService:
    """Service for AI-powered task analysis and natural language processing."""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize OpenAI client if API key is valid."""
        try:
            # Only initialize if we have a real API key
            if settings.openai_api_key and settings.openai_api_key != "your-openai-api-key":
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=settings.openai_api_key)
                logger.info("OpenAI client initialized successfully")
            else:
                logger.warning("OpenAI API key not configured - AI features will use fallbacks")
        except Exception as e:
            logger.error("Failed to initialize OpenAI client", error=str(e))
        
    async def analyze_task_input(
        self, 
        input_text: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze natural language input and extract structured task data."""
        
        if not self.client:
            logger.warning("OpenAI client not available, using fallback analysis")
            return self._fallback_task_analysis(input_text)
        
        system_prompt = """
        You are an AI assistant specialized in task management. 
        Analyze the user's input and extract structured task information.
        
        Return a JSON object with these fields:
        - title: concise task title (required)
        - description: detailed description if provided
        - priority: integer 1-5 (1=critical, 5=someday), default 3
        - est_duration: estimated duration in minutes
        - target_deadline: ISO datetime if mentioned
        - tags: array of relevant tags
        - subtasks: array of subtask objects if the task can be broken down
        - suggestions: array of helpful suggestions for the user
        
        Examples:
        Input: "I need to buy a new HDMI cord on Amazon before the end of the day!"
        Output: {
            "title": "Buy HDMI cord",
            "description": "Purchase HDMI cord from Amazon",
            "priority": 1,
            "est_duration": 15,
            "target_deadline": "2024-01-27T17:00:00Z",
            "tags": ["shopping", "electronics"],
            "suggestions": ["Check reviews before purchasing", "Compare prices"]
        }
        """
        
        user_prompt = f"""
        Analyze this task input: "{input_text}"
        
        Context: {json.dumps(context) if context else "None"}
        
        Return only valid JSON.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content
            analysis = json.loads(content)
            
            logger.info("Task analysis completed", input_length=len(input_text))
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error("Failed to parse AI response as JSON", error=str(e))
            # Fallback to basic parsing
            return self._fallback_task_analysis(input_text)
            
        except Exception as e:
            logger.error("AI task analysis failed", error=str(e))
            return self._fallback_task_analysis(input_text)
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text using OpenAI."""
        if not self.client:
            logger.warning("OpenAI client not available, returning dummy embedding")
            # Return a dummy embedding of the right size for testing
            return [0.0] * 1536
            
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            
            embedding = response.data[0].embedding
            logger.debug("Generated embedding", text_length=len(text))
            return embedding
            
        except Exception as e:
            logger.error("Failed to generate embedding", error=str(e))
            # Return dummy embedding as fallback
            return [0.0] * 1536
    
    async def analyze_scheduling_decision(
        self,
        task_data: Dict[str, Any],
        schedule_context: Dict[str, Any],
        user_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze whether and when to schedule a task."""
        
        if not self.client:
            logger.warning("OpenAI client not available, using simple scheduling logic")
            return {
                "action": "schedule",
                "reasoning": "Default scheduling decision (AI not available)",
                "suggested_time": "09:00",
                "priority_score": task_data.get("priority", 3)
            }
        
        system_prompt = """
        You are an intelligent scheduling assistant. Analyze the task and context
        to decide whether to schedule it and when.
        
        Return JSON with:
        - action: "schedule", "bump", or "reject"
        - reasoning: explanation of decision
        - suggested_time: HH:MM format if scheduling
        - bump_task_id: UUID of task to bump if action is "bump"
        - priority_score: calculated priority score
        """
        
        user_prompt = f"""
        Task: {json.dumps(task_data)}
        Schedule Context: {json.dumps(schedule_context)}
        User Preferences: {json.dumps(user_preferences)}
        
        Make a scheduling decision.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            decision = json.loads(content)
            
            logger.info("Scheduling decision completed", action=decision.get("action"))
            return decision
            
        except Exception as e:
            logger.error("Scheduling analysis failed", error=str(e))
            # Return fallback decision
            return {
                "action": "schedule",
                "reasoning": f"Fallback decision due to error: {str(e)}",
                "suggested_time": "09:00",
                "priority_score": task_data.get("priority", 3)
            }
    
    async def generate_personality_response(
        self,
        message: str,
        personality_profile: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a response tailored to user's personality profile."""
        
        if not self.client:
            return f"I understand you said: '{message}'. (AI personality features not available)"
        
        # Convert personality scores to descriptive traits
        traits = self._personality_to_traits(personality_profile)
        
        system_prompt = f"""
        You are the user's AI assistant with these personality traits:
        - Communication style: {traits['communication']}
        - Motivation approach: {traits['motivation']}
        - Proactivity level: {traits['proactivity']}
        - Reassurance needs: {traits['reassurance']}
        - Language variety: {traits['language']}
        
        Respond in a way that matches these traits exactly. Be authentic and helpful.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7 if traits['language'] == 'varied' else 0.3,
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error("Personality response generation failed", error=str(e))
            return f"I understand you said: '{message}'. (Error generating personalized response)"
    
    def _fallback_task_analysis(self, input_text: str) -> Dict[str, Any]:
        """Fallback task analysis if AI parsing fails."""
        return {
            "title": input_text[:100],  # First 100 chars as title
            "description": input_text if len(input_text) > 100 else None,
            "priority": 3,
            "est_duration": 30,  # Default 30 minutes
            "tags": [],
            "suggestions": ["Review and refine this task"]
        }
    
    def _personality_to_traits(self, profile: Dict[str, Any]) -> Dict[str, str]:
        """Convert personality scores to descriptive traits."""
        
        def score_to_trait(score: int, negative_trait: str, positive_trait: str) -> str:
            if score <= -3:
                return f"very {negative_trait}"
            elif score <= -1:
                return negative_trait
            elif score >= 3:
                return f"very {positive_trait}"
            elif score >= 1:
                return positive_trait
            else:
                return f"balanced {negative_trait}/{positive_trait}"
        
        return {
            'communication': score_to_trait(
                profile.get('warm_candid', 0), 
                'candid and direct', 
                'warm and encouraging'
            ),
            'motivation': score_to_trait(
                profile.get('motivation_direction', 0),
                'problem-avoiding',
                'goal-seeking'
            ),
            'proactivity': score_to_trait(
                profile.get('proactive_reactive', 0),
                'reactive and responsive',
                'proactive and driving'
            ),
            'reassurance': score_to_trait(
                profile.get('reassurance_needs', 0),
                'low maintenance',
                'supportive and reassuring'
            ),
            'language': 'varied and creative' if profile.get('language_variety', 0) > 0 else 'consistent and clear'
        } 