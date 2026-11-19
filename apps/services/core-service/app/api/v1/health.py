import logging

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.core.database import get_db, get_mongo_db

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health_check(
    db: Session = Depends(get_db),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    postgres_healthy = False
    mongo_healthy = False

    try:
        db.execute(text("SELECT 1"))
        postgres_healthy = True
    except Exception:
        logger.exception("PostgreSQL health check failed")

    try:
        await mongo_db.command("ping")
        mongo_healthy = True
    except Exception:
        logger.exception("MongoDB health check failed")

    if not postgres_healthy or not mongo_healthy:
        raise HTTPException(
            status_code=503,
            detail="Serviço temporariamente indisponível.",
        )

    return {"status": "healthy"}
