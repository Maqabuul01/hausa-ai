from sqlalchemy.orm import Session
from app.models.conversation import Conversation, Message
from app.services.ai_service import get_ai_service
from typing import Optional, List

class ConversationService:
    """Service for conversation management"""
    
    @staticmethod
    def create_conversation(
        db: Session,
        user_id: int,
        title: Optional[str] = None
    ) -> Conversation:
        """
        Create a new conversation
        
        Args:
            db: Database session
            user_id: User ID
            title: Conversation title
        
        Returns:
            Created Conversation object
        """
        conversation = Conversation(
            user_id=user_id,
            title=title or "New Conversation"
        )
        
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        return conversation
    
    @staticmethod
    def get_conversation(
        db: Session,
        conversation_id: int,
        user_id: int
    ) -> Optional[Conversation]:
        """
        Get conversation by ID (with user ownership check)
        
        Args:
            db: Database session
            conversation_id: Conversation ID
            user_id: User ID (for authorization)
        
        Returns:
            Conversation object or None
        """
        return db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()
    
    @staticmethod
    def get_user_conversations(
        db: Session,
        user_id: int,
        limit: int = 20,
        offset: int = 0
    ) -> List[Conversation]:
        """
        Get all conversations for a user
        
        Args:
            db: Database session
            user_id: User ID
            limit: Max results
            offset: Pagination offset
        
        Returns:
            List of Conversation objects
        """
        return db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(
            Conversation.updated_at.desc()
        ).offset(offset).limit(limit).all()
    
    @staticmethod
    def add_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str,
        language: str = "en"
    ) -> Message:
        """
        Add message to conversation
        
        Args:
            db: Database session
            conversation_id: Conversation ID
            role: "user" or "assistant"
            content: Message content
            language: Message language
        
        Returns:
            Created Message object
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            language=language
        )
        
        db.add(message)
        db.commit()
        db.refresh(message)
        
        return message
    
    @staticmethod
    def get_conversation_history(
        db: Session,
        conversation_id: int
    ) -> List[Message]:
        """
        Get all messages in a conversation
        
        Args:
            db: Database session
            conversation_id: Conversation ID
        
        Returns:
            List of Message objects
        """
        return db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).all()
    
    @staticmethod
    def process_chat_message(
        db: Session,
        conversation_id: int,
        user_id: int,
        user_message: str,
        language: str = "en"
    ) -> str:
        """
        Process user message and get AI response
        
        Args:
            db: Database session
            conversation_id: Conversation ID
            user_id: User ID (for authorization)
            user_message: User's input message
            language: Message language
        
        Returns:
            AI response text
        """
        # Verify conversation ownership
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()
        
        if not conversation:
            raise ValueError("Conversation not found or access denied")
        
        # Add user message to DB
        ConversationService.add_message(
            db, conversation_id, "user", user_message, language
        )
        
        # Get conversation history
        history = ConversationService.get_conversation_history(db, conversation_id)
        history_list = [
            {"role": msg.role, "content": msg.content}
            for msg in history[:-1]  # Exclude the message we just added
        ]
        
        # Get AI response
        ai_service = get_ai_service()
        ai_response = ai_service.generate_response(
            user_message=user_message,
            conversation_history=history_list,
            language=language
        )
        
        # Add AI response to DB
        ConversationService.add_message(
            db, conversation_id, "assistant", ai_response, language
        )
        
        return ai_response
