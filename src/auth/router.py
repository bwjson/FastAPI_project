import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache.decorator import cache
from database import get_async_session
from auth.models import role
from auth.schemas import RoleCreate

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.post("")
async def add_specific_operations(new_role: RoleCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(role).values(**new_role.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}