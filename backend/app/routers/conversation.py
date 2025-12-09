from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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


# Get a list of all conversations
@router.get("/", response_model=ConversationListResponse)
async def list_conversations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Conversation))
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
