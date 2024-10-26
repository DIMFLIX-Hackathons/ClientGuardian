from sqladmin import ModelView
from typing import List

from database.models import Token, Task


class TokensView(ModelView, model=Token):
    column_list = [column.name for column in Token.__table__.columns]


class TasksView(ModelView, model=Task):
    column_list = [column.name for column in Task.__table__.columns]

all_views: List[ModelView] = [TokensView, TasksView]
