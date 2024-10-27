import asyncio
import os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from enum import Enum

import joblib
import pandas as pd
from config import backend_src
from fastapi import HTTPException
from sklearn.preprocessing import LabelEncoder
from dataclasses import dataclass

class DatasetExtension(str, Enum):
	CSV = ".csv"
	EXCEL = ".xls"


class UnsupportedDatasetExtension(Exception):
	def __init__(self, message, extra_info):
		super().__init__(message)
		self.extra_info = extra_info


@dataclass
class Dataset:
	data: pd.DataFrame
	data1: pd.DataFrame
	data2: pd.DataFrame
	data3: pd.DataFrame
	data4: pd.DataFrame
	data5: pd.DataFrame
	data6: pd.DataFrame
	data7: pd.DataFrame
	data8: pd.DataFrame
	data9: pd.DataFrame
	data10: pd.DataFrame
	data11: pd.DataFrame
	data_concatenated: pd.DataFrame # pd.concat([data4, data5, data6, data7, data8, data9, data10, data11])


class DatasetProcessor:
	_instance = None
	_executor = ProcessPoolExecutor()
	_model = joblib.load(backend_src / "utils" / "models" / "decision_knn.joblib")

	def __new__(cls):
		"""
		Это не важно. (Метод для создания класса Singlethon)
		"""
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	@classmethod
	async def process_dataset(cls, task_id: str, dataset_path: Path):
		"""
		Стартовая функция с которой всё начинается.
		"""
		df = cls.load_dataset(dataset_path) # Загружаем датасет. На выход по сути должен вернуться объединенный датафрейм 
		validated_df = cls.validate_df(df.copy()) # Валидация датафрейма.
		return await cls.run_model(validated_df, task_id) # запуск угадывания

	@classmethod
	def load_dataset(cls, dataset_path: Path) -> Dataset:
		...
	
	@classmethod
	def validate_df(cls, dataframe: pd.DataFrame) -> pd.DataFrame:
		...
		return dataframe

	@classmethod
	async def run_model(cls, dataframe: pd.DataFrame, task_id: str):
		loop = asyncio.get_event_loop()
		result = await loop.run_in_executor(
			cls._executor, cls.run_model_sync, dataframe, task_id
		)
		return result

	@classmethod
	def run_model_sync(cls, dataframe: pd.DataFrame, task_id: str):
		predictions = cls._model.predict(dataframe)
		return {"task_id": task_id, "predictions": predictions}
