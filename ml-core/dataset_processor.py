import asyncio
import os
from concurrent.futures import ProcessPoolExecutor
from enum import Enum

import joblib
import pandas as pd
from config import backend_src
from fastapi import HTTPException
from sklearn.preprocessing import LabelEncoder


class DatasetExtension(str, Enum):
	CSV = ".csv"
	EXCEL = ".xls"


class UnsupportedDatasetExtension(Exception):
	def __init__(self, message, extra_info):
		super().__init__(message)
		self.extra_info = extra_info


class DatasetProcessor:
	_instance = None
	_executor = ProcessPoolExecutor()
	_model = joblib.load(backend_src / "core" / "best_models" / "decision_knn_super_duper_model.joblib")

	def __new__(cls):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	@classmethod
	async def process_dataset(cls, task_id: str, dataset_path: str):
		ext = os.path.splitext(dataset_path)[-1]
		if ext not in [ext.value for ext in DatasetExtension]:
			raise UnsupportedDatasetExtension(
				f"Unsupported file extension: {ext}", {"code": 400}
			)

		df = cls.load_dataset(dataset_path)
		validated_df = cls.validate_df(df.copy())
		return await cls.run_model(validated_df, task_id)

	@classmethod
	def load_dataset(cls, dataset_path: str) -> pd.DataFrame:
		try:
			if dataset_path.endswith(DatasetExtension.CSV.value):
				return pd.read_csv(dataset_path)
			elif dataset_path.endswith(DatasetExtension.EXCEL.value):
				return pd.read_excel(dataset_path)
			else:
				raise UnsupportedDatasetExtension(
					"Unsupported file extension", {"code": 400}
				)
		except Exception as e:
			raise HTTPException(status_code=500, detail=str(e))
	
	@classmethod
	def validate_df(cls, dataframe: pd.DataFrame) -> pd.DataFrame:
		# Удаляем колонку 'ID', если она существует
		if 'ID' in dataframe.columns:
			df = dataframe.drop(columns=['ID'])
		else:
			df = dataframe.copy()  # Копируем DataFrame, если 'ID' нет

		label_encoder = LabelEncoder()

		# Проверяем и кодируем колонки, если они существуют
		for column in ['Субъект федерации отп', 'Субъект федерации наз', 'Гр груза по опер.номен']:
			if column in df.columns:
				df[column] = label_encoder.fit_transform(df[column])
			else:
				print(f"Колонка '{column}' не найдена и не будет закодирована.")

		# Удаляем колонки, если они существуют
		columns_to_drop = ['Город фактический', 'Грузоотправитель', 
						   '2022/01', '2022/02', '2022/03', 
						   '2022/04', '2022/05', '2022/06', 
						   '2022/07', '2022/08', 'Грузополучатель']
		
		for column in columns_to_drop:
			if column in df.columns:
				df = df.drop(column, axis=1)
			else:
				print(f"Колонка '{column}' не найдена и не будет удалена.")

		return df

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


# @app.post("/process/")
# async def create_task(task_id: str, dataset_path: str):
#     return await DatasetProcessor.process_dataset(task_id, dataset_path)
