import aiohttp
from typing import Sequence

class Model:
	__API_URL = 'http://localhost:8080/completion'
	__SYSTEM_PROMPT_PATH = 'backend/model/system_prompt.txt'
	__MAX_TOKENS = 128

	def __init__(self) -> None:
		with open(self.__SYSTEM_PROMPT_PATH) as f:
			self.__system_prompt = f.read()

	async def ask(self, history: Sequence[dict]) -> str:
		prompt = self.__system_prompt + '\n\n'
		for turn in history:
			prompt += f'User: {turn["user"]}\n'
			if 'ai' in turn:
				prompt += f'AI: {turn["ai"]}\n'

		prompt += 'AI:'

		payload = {
			'prompt': prompt,
			'n_predict': self.__MAX_TOKENS,
			'temperature': 0.7,
			'stop': ('User:', 'Пользователь:', 'Patient:', 'Пациент:'),
		}

		async with aiohttp.ClientSession() as session:
			async with session.post(self.__API_URL, json=payload, timeout=120) as response:
				response.raise_for_status()
				result = await response.json()
				return result.get('content', '').strip()

__all__ = ('Model',)