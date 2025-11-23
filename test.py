from app.dal.friend_info_dal import UserDal
from app.database import AsyncSessionLocal
import asyncio
async def main():
    async with AsyncSessionLocal() as db:
        dal = UserDal(db)
        user = await dal.get_users()
        print(user.Id)
asyncio.run(main())