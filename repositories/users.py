import datetime
from typing import Optional, List

from base import BaseRepository
from core.security import hash_password
from models.user import User, UserIn
from db.users import users


class UserRepository(BaseRepository):

    async def get_all_users(self) -> List[User]:
        query = users.select().limit(100)
        return await self.database.fetch_all(query)

    async def create_user(self, u: UserIn) -> Optional[User]:
        user = User(
            email=u.email,
            hashed_password=hash_password(u.password),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )

        values = {**user.dict()}
        values.pop('id', None)
        query = users.insert().values(values)
        user.id = await self.database.execute(query)
        return User.parse_obj(user)

    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id == id)
        user = await self.database.fetch_one(query)
        if not user:
            return None
        return User.parse_obj(user)

    async def get_by_email(self, email: str) -> User:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)
        if not user:
            return None
        return User.parse_obj(user)
