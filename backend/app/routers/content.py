from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.conversations import Conversation
from app.schemas.content import ContentRequest, ContentResponse
from app.services.lekhak_service import async_generate_content

router = APIRouter()


@router.post("/generated/", response_model=ContentResponse)
async def generate_content(request: ContentRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Generate content
        content = await async_generate_content(
            prompt=request.prompt,
            user_id=request.user_id,
            company_id=request.company_id,
            product_id=request.product_id,
        )

        # Save conversation to database if company_id is provided
        conversation_id = None
        if request.company_id:
            db_conversation = Conversation(
                company_id=request.company_id,
                product_id=request.product_id,
                user_query=request.prompt,
                generated_content=content,
            )
            db.add(db_conversation)
            await db.commit()
            await db.refresh(db_conversation)
            conversation_id = db_conversation.id

        return ContentResponse(
            content=content,
            company_id=request.company_id,
            product_id=request.product_id,
            user_query=request.prompt,
            generated_at=datetime.utcnow().isoformat(),
            conversation_id=conversation_id,
        )
    except Exception as e:
        # Return user-friendly error message
        error_message = str(e)
        raise HTTPException(status_code=503, detail=error_message)
