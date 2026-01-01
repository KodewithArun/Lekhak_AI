from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.framework import Framework
from app.schemas.framework import FrameworkCreate, FrameworkResponse

router = APIRouter()

@router.post("/", response_model=FrameworkResponse)
async def create_framework(framework: FrameworkCreate, db: AsyncSession = Depends(get_db)):
    """Create a new custom framework."""
    db_framework = Framework(
        name=framework.name,
        description=framework.description,
        instruction=framework.instruction
    )
    db.add(db_framework)
    await db.commit()
    await db.refresh(db_framework)
    return db_framework

@router.get("/", response_model=List[FrameworkResponse])
async def get_frameworks(db: AsyncSession = Depends(get_db)):
    """List all available content frameworks."""
    result = await db.execute(select(Framework))
    frameworks = result.scalars().all()
    return frameworks

@router.get("/{id}", response_model=FrameworkResponse)
async def get_framework(id: int, db: AsyncSession = Depends(get_db)):
    """Get specific framework details."""
    result = await db.execute(select(Framework).where(Framework.id == id))
    framework = result.scalar_one_or_none()
    if not framework:
        raise HTTPException(status_code=404, detail="Framework not found")
    return framework
