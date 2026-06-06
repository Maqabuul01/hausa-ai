from sqlalchemy.orm import Session
from app.models.user import User
from app.security.jwt import hash_password, verify_password
from typing import Optional
from datetime import datetime

class AuthService:
    """Authentication service"""
    
    @staticmethod
    def register_user(
        db: Session,
        email: str,
        username: str,
        password: str,
        full_name: Optional[str] = None
    ) -> User:
        """
        Register a new user
        
        Args:
            db: Database session
            email: User email
            username: User username
            password: Plain text password
            full_name: User's full name
        
        Returns:
            Created User object
        
        Raises:
            ValueError: If email or username already exists
        """
        # Check if user exists
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            raise ValueError(f"Email {email} already registered")
        
        existing_username = db.query(User).filter(User.username == username).first()
        if existing_username:
            raise ValueError(f"Username {username} already taken")
        
        # Create new user
        user = User(
            email=email,
            username=username,
            hashed_password=hash_password(password),
            full_name=full_name
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate user with email and password
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
        
        Returns:
            User object if authenticated, None otherwise
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
