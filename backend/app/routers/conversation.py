from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.conversation import (
    ConversationCreate,
    ConversationGet,
    ConversationListResponse,
)
from app.models.conversations import Conversation

router = APIRouter(prefix="/conversations", tags=["conversations"])


# Create a new conversation
@router.post("/", response_model=ConversationGet)
async def create_conversation(
    conversation: ConversationCreate, db: Session = Depends(get_db)
):
    db_conversation = Conversation(
        title=conversation.title,
        user_id=conversation.user_id,
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


# Get a list of all conversations
@router.get("/", response_model=ConversationListResponse)
async def list_conversations(db: Session = Depends(get_db)):
    all_conversations = db.query(Conversation).all()
    return ConversationListResponse(conversations=all_conversations)
    return ConversationListResponse(conversations=conversations)


# Get a specific conversation by ID
@router.get("/{conversation_id}", response_model=ConversationGet)
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conversation = (
        db.query(Conversation).filter(Conversation.id == conversation_id).first()
    )
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation
