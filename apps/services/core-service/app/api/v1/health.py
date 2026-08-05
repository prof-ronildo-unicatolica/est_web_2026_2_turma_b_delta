from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.core.database import get_db, get_mongo_db

router = APIRouter()


@router.get("/health")
async def health_check(
    db: Session = Depends(get_db),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    postgres_status = "unhealthy"
    mongo_status = "unhealthy"

    # Testar PostgreSQL
    try:
        db.execute(text("SELECT 1"))
        postgres_status = "healthy"
    except Exception as e:
        postgres_status = f"error: {str(e)}"

    # Testar MongoDB
    try:
        await mongo_db.command("ping")
        mongo_status = "healthy"
    except Exception as e:
        mongo_status = f"error: {str(e)}"

    if postgres_status != "healthy" or mongo_status != "healthy":
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "postgres": postgres_status,
                "mongodb": mongo_status,
            },
        )

    return {"status": "healthy", "postgres": postgres_status, "mongodb": mongo_status}
