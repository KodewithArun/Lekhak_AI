from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.conversations import Conversation
from app.schemas.conversation import (
    ConversationCreate,
    ConversationGet,
    ConversationListResponse,
)

router = APIRouter()


# Create a new conversation
@router.post("/", response_model=ConversationGet)
async def create_conversation(
    conversation: ConversationCreate, db: AsyncSession = Depends(get_db)
):
    db_conversation = Conversation(
        company_id=conversation.company_id,
        product_id=conversation.product_id,
        user_query=conversation.user_query,
        generated_content=conversation.generated_content,
    )
    db.add(db_conversation)
    await db.commit()
    await db.refresh(db_conversation)
    return db_conversation


# Get a list of all conversations (optionally filtered by user_id)
@router.get("/", response_model=ConversationListResponse)
async def list_conversations(
    user_id: Optional[str] = None, db: AsyncSession = Depends(get_db)
):
    query = select(Conversation)
    if user_id:
        query = query.where(Conversation.user_id == user_id)

    result = await db.execute(query)
    all_conversations = result.scalars().all()
    return ConversationListResponse(conversations=all_conversations)


# Get a specific conversation by ID
@router.get("/{conversation_id}", response_model=ConversationGet)
async def get_conversation(conversation_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    db_conversation = result.scalar_one_or_none()
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation
