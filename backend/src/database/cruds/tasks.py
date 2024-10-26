from datetime import datetime, timezone
from typing import List, Optional
from loguru import logger

from sqlalchemy import select, delete

from ..db_manager import DatabaseManager
from ..models import Token, Task


class TasksCRUD:
    db_manager: DatabaseManager


    async def create_task(self, token_id: int, original_filename: str) -> str:
        async with self.db_manager.get_session() as session:
            task = Task(token_id=token_id, original_filename=original_filename)
            session.add(task)
            await session.commit()
            return task.id