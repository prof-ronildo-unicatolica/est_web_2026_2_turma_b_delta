"""Remove the unused administrator inserted by the old Mongo seed."""

import asyncio

from app.core.database import mongo_client, mongo_db


async def main() -> None:
    try:
        result = await mongo_db["users"].delete_one(
            {
                "email": "admin@hotel.com",
                "username": "admin",
                "role": "admin_master",
            }
        )
        print(
            "Legacy Mongo admin cleanup finished; "
            f"removed {result.deleted_count} matching account(s)."
        )
    finally:
        mongo_client.close()


if __name__ == "__main__":
    asyncio.run(main())
