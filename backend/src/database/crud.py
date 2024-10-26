from .cruds.tokens import TokensCRUD
from .db_manager import DatabaseManager


class CommonCRUD(TokensCRUD):
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager




        
