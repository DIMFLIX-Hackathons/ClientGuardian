from datetime import datetime, timezone
from typing import List, Optional
from loguru import logger

from sqlalchemy import select, delete

from ..db_manager import DatabaseManager
from ..models import Token, Task


class TokensCRUD:
    db_manager: DatabaseManager

    
    async def check_token(self,token):
        async with self.db_manager.get_session() as session:
            query = select(Token).where(Token.token==token)
            result = await session.execute(query)
            token_from_db = result.scalars().first()
            
            if not token_from_db or not token_from_db.enabled:
                print("нету или не включе")
                return False
            
            if datetime.now() > token_from_db.lifetime:
                print("Время вышло")
                return False
            
            return True

    async def get_user_files_by_token(self,token):
        async with self.db_manager.get_sesion() as session:
            query = select(Task).where(Task.token_id == select(Token.id).where(Token.token == token))
            result = await session.execute(query)
            if result.rowcount > 0:
                return result.scalars().all()  
            return None

    async def delete_task_by_id(self, task_id):
        async with self.db_manager.get_session() as session:
            query = delete(Task).where(Task.id==task_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0
            