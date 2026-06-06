import google.generativeai as genai
from typing import Optional, List, Dict
import os
from datetime import datetime

class GeminiAIService:
    """Gemini AI service for chat interactions"""
    
    def __init__(self):
        """Initialize Gemini AI client"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-pro")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        language: str = "en"
    ) -> str:
        """
        Generate AI response using Gemini
        
        Args:
            user_message: The user's input message
            conversation_history: Previous messages in conversation
            language: Language code (en, ha, etc.)
        
        Returns:
            AI generated response
        """
        try:
            # Build system prompt for Hausa AI
            system_prompt = self._get_system_prompt(language)
            
            # Format conversation history
            messages = self._format_conversation(
                system_prompt,
                conversation_history or [],
                user_message
            )
            
            # Generate response
            response = self.model.generate_content(messages)
            
            if response.text:
                return response.text
            else:
                return "I couldn't generate a response. Please try again."
        
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return f"Error: Unable to process your request - {str(e)}"
    
    def _get_system_prompt(self, language: str) -> str:
        """
        Get system prompt based on language
        
        Args:
            language: Language code
        
        Returns:
            System prompt string
        """
        prompts = {
            "en": """You are HausaAI, a helpful AI assistant specialized in Hausa language and culture.
            You provide accurate, respectful, and helpful responses.
            You support both English and Hausa languages.
            Always be clear, concise, and user-friendly.""",
            "ha": """Ka ce Kai HausaAI, aiki-zama mai taimakawa da sana'a game da harshen Hausa.
            Ka ba da amsa masu gaskiya, mutunci, da taimakawa.
            Ka goyi bayan English da harshen Hausa.
            Koyaushe ka sami bayyani, gajere, kuma da nauyin mai amfani.""",
        }
        return prompts.get(language, prompts["en"])
    
    def _format_conversation(
        self,
        system_prompt: str,
        history: List[Dict[str, str]],
        user_message: str
    ) -> str:
        """
        Format conversation for Gemini
        
        Args:
            system_prompt: System instruction
            history: Previous conversation messages
            user_message: Current user message
        
        Returns:
            Formatted prompt string
        """
        formatted = system_prompt + "\n\n"
        
        # Add conversation history
        for msg in history:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")
            formatted += f"{role}: {content}\n"
        
        # Add current message
        formatted += f"User: {user_message}\n"
        formatted += "Assistant: "
        
        return formatted
    
    async def stream_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        language: str = "en"
    ):
        """
        Stream AI response for real-time chat experience
        
        Args:
            user_message: The user's input message
            conversation_history: Previous messages
            language: Language code
        
        Yields:
            Text chunks as they're generated
        """
        try:
            system_prompt = self._get_system_prompt(language)
            messages = self._format_conversation(
                system_prompt,
                conversation_history or [],
                user_message
            )
            
            response = self.model.generate_content(
                messages,
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        
        except Exception as e:
            yield f"Error: {str(e)}"

# Singleton instance
_ai_service = None

def get_ai_service() -> GeminiAIService:
    """Get or create AI service instance"""
    global _ai_service
    if _ai_service is None:
        _ai_service = GeminiAIService()
    return _ai_service
