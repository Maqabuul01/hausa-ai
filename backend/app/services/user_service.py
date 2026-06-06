from sqlalchemy.orm import Session
from app.models.user import User
from typing import Optional

class UserService:
    """User service for user operations"""
    
    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> Optional[User]:
        """
        Get user profile
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            User object or None
        """
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def update_user_profile(
        db: Session,
        user_id: int,
        full_name: Optional[str] = None,
        language: Optional[str] = None
    ) -> Optional[User]:
        """
        Update user profile
        
        Args:
            db: Database session
            user_id: User ID
            full_name: Updated full name
            language: Updated language preference
        
        Returns:
            Updated User object
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return None
        
        if full_name:
            user.full_name = full_name
        if language:
            user.language = language
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Delete user account
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            True if deleted, False otherwise
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        
        return True
