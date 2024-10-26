from ..db_manager import DatabaseManager
from ..models import Task
from typing import List


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
            query = session.query(Task).filter_by(token_id=token_id)
            return await query.all()
        