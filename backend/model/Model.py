import aiofiles
import aiohttp
from datetime import datetime
import json
import random
import re
import traceback

class Model:
	"""
	Класс для генерации медицинских вопросов с помощью языковой модели через HTTP API.

	Атрибуты:
		__ATTEMPTS (int): Количество попыток генерации при ошибках.
		__ERRORS_FILE (str): Путь к файлу для логирования ошибок.

		__API_URL (str): URL эндпоинта модели для генерации.
		__SYSTEM_PROMPT_PATH (str): Путь к файлу с системным промптом.
		__KEYWORDS_PATH (str): Путь к файлу с ключевыми словами.
		__KEYWORDS_NUM_RANGE (tuple): Диапазон количества ключевых слов для генерации.

		__system_prompt (str): Содержимое системного промпта.
		__keywords (list): Список ключевых слов.
	"""

	__ATTEMPTS = 3
	__ERRORS_FILE = 'logs/Model.log'

	__API_URL = 'http://medgemma-server:8080/v1/chat/completions'
	__SYSTEM_PROMPT_PATH = 'model/system_prompt.txt'
	__KEYWORDS_PATH = 'model/keywords.txt'
	__KEYWORDS_NUM_RANGE = (2, 5)

	def __init__(self) -> None:
		"""
		Загрузка системного промпта и ключевых слов.
		"""

		with open(self.__SYSTEM_PROMPT_PATH) as f:
			self.__system_prompt = f.read()
		with open(self.__KEYWORDS_PATH) as f:
			self.__keywords = f.read().split()

	async def generate(self) -> dict[str, str]:
		"""
		Асинхронно генерирует медицинский вопрос с помощью языковой модели.

		Возвращает:
			dict[str, str]: Сгенерированный вопрос в формате JSON.

		Исключения:
			RuntimeError: Если не удалось получить результат после нескольких попыток.
		"""

		num_keywords = random.randint(*self.__KEYWORDS_NUM_RANGE)
		keywords = random.choices(self.__keywords, k=num_keywords)

		payload = {
			'messages': (
				{'role': 'system', 'content': self.__system_prompt},
				{'role': 'user', 'content': ' '.join(keywords)},
			),
			'cache_prompt': True,
		}

		async with aiohttp.ClientSession() as session:
			for _ in range(self.__ATTEMPTS):
				try:
					async with session.post(self.__API_URL, json=payload, timeout=120) as response:
						response.raise_for_status()
						result = await response.json()

						text = result['choices'][0]['message']['content']
						text_json = re.search(r'\{.*?\}', text, re.DOTALL)
						result = json.loads(text_json.group(0))
						return result
				except Exception as e:
					async with aiofiles.open(self.__ERRORS_FILE, 'a') as log_file:
						await log_file.write(f'[{datetime.now()}][ERROR] {type(e).__name__}: {e}\n')
						await log_file.write(traceback.format_exc())

		raise RuntimeError('Failed to generate question after multiple attempts!')

__all__ = ('Model',)