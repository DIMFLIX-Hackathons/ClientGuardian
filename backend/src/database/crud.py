from .cruds.tokens import TokensCRUD
from .cruds.tasks import TasksCRUD
from .db_manager import DatabaseManager


class CommonCRUD(TokensCRUD, TasksCRUD):
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager




        
