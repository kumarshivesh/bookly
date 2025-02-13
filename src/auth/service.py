# src/auth/services.py
from src.db.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import UserCreateModel
from .utils import generate_password_hash

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)
        user = result.first()
        #print(f"'user': {user}")  # print statement
        return user
    
    async def user_exists(self, email:str, session: AsyncSession):
        user = await self.get_user_by_email(email,session)
        """
        if user is None:
            return False
        else:
            return True
        """
        return True if user is not None else False
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict) # Unpack the 'user_data_dict' to create a 'User' object with the provided request body data

        new_user.password_hash = generate_password_hash(user_data_dict['password'])
        new_user.role = user_data_dict.get('role', 'user')  # Set role from the request body, default to 'user'

        session.add(new_user)
        await session.commit()

        return new_user

    async def update_user(self, user:User , user_data: dict,session:AsyncSession):
        for k, v in user_data.items():
            setattr(user, k, v)

        await session.commit()

        return user

