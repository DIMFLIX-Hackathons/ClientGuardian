from typing import List

from sqlalchemy import delete, select

from ..db_manager import DatabaseManager
from ..models import Task


class TasksCRUD:
    db_manager: DatabaseManager

    async def create_task(self, token_id: int, original_filename: str) -> str:
        async with self.db_manager.get_session() as session:
            task = Task(token_id=token_id, original_filename=original_filename)
            session.add(task)
            await session.commit()
            return task.id

    async def get_my_tasks(self, token_id: id) -> List[Task]:
        async with self.db_manager.get_session() as session:
            query = await session.execute(
                select(Task).filter(Task.token_id == token_id)
            )
            return query.scalars().all()

    async def get_task_by_id(self, task_id):
        async with self.db_manager.get_session() as session:
            query = select(Task).where(Task.id == task_id)
            result = await session.execute(query)
            return result.scalars().first()

    async def delete_task(self, token_id, task_id):
        async with self.db_manager.get_session() as session:
            query = delete(Task).where(Task.id == task_id, Task.token_id == token_id)
            await session.execute(query)
            await session.commit()
