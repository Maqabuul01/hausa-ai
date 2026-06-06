import google.generativeai as genai
from backend.config import settings


class HausaAIService:
    """
    Wraps Gemini API with Hausa language context.
    Handles bilingual communication (Hausa + English).
    """
    
    def __init__(self):
        """Initialize Gemini client with API key."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
    
    @staticmethod
    def _get_system_prompt() -> str:
        """
        Returns the system prompt for HausaAI.
        Defines personality, tone, and language behavior.
        """
        return """You are HausaAI, an intelligent assistant for Hausa language processing and African tech context.

CORE TRAITS:
- Intelligent, practical, and culturally aware
- Respectful of Hausa communication style
- Warm and professional, never robotic or overly corporate
- Clear explanations that simplify complex ideas
- Avoids cringe motivational language or fake "Africanized" tone

LANGUAGE BEHAVIOR:
- If user speaks Hausa → respond in Hausa
- If user speaks English → respond in English  
- If user mixes languages → respond naturally in mixed language (code-switching is normal)
- Understand Hausa greetings: Sannu, Sannu da aiki, Ya kake?, etc.
- Understand Nigerian/Hausa context: education, business, tech, local expressions
- If user says something unclear, ask for clarification respectfully

EXAMPLE BEHAVIORS:
- "Sannu, ina kowa?" → Respond naturally in Hausa
- "How do I deploy my backend?" → Respond in English
- "Ban gane ba, shin yan..." → Understand and simplify
- "Wallahi wannan ya rikitar dani" → Understand frustration contextually

AREAS OF EXPERTISE:
- Hausa language learning and translation
- Programming and tech concepts
- Conversational AI and chatbots
- African tech ecosystem
- Education and communication

TONE: Never fake. Never over-force culture. Natural > performative."""
    
    def chat(self, message: str) -> dict:
        """
        Send user message to Gemini and get response.
        
        Args:
            message: User input in Hausa or English
            
        Returns:
            dict with 'response' and 'language' keys
        """
        try:
            system_prompt = self._get_system_prompt()
            
            # Send message to Gemini with system context
            full_message = f"{system_prompt}\n\nUser: {message}"
            response = self.model.generate_content(full_message)
            
            # Extract response text
            ai_response = response.text if response else "I couldn't process that. Try again?"
            
            # Detect language (simple heuristic)
            language = self._detect_language(message)
            
            return {
                "response": ai_response,
                "language": language
            }
        
        except Exception as e:
            return {
                "response": f"Error processing your message: {str(e)}",
                "language": "error"
            }
    
    @staticmethod
    def _detect_language(text: str) -> str:
        """
        Simple language detection for Hausa/English/Mixed.
        
        Args:
            text: User input
            
        Returns:
            'hausa', 'english', or 'mixed'
        """
        # Common Hausa words
        hausa_words = {
            "sannu", "ya", "kake", "kowa", "ina", "da", "ne", "ce", "yau",
            "gida", "gobe", "jiya", "wannan", "wadannan", "ko", "amma",
            "wallahi", "kai", "ni", "mu", "su", "zan", "za", "na", "a"
        }
        
        # Convert to lowercase and split
        words = text.lower().split()
        
        hausa_count = sum(1 for word in words if word in hausa_words)
        hausa_ratio = hausa_count / len(words) if words else 0
        
        if hausa_ratio > 0.5:
            return "hausa"
        elif hausa_ratio > 0.1:
            return "mixed"
        else:
            return "english"
