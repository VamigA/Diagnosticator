from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from model.Model import Model

app = FastAPI()
model = Model()

app.add_middleware(
	CORSMiddleware,
	allow_origins=('*',),
	allow_credentials=True,
	allow_methods=('*',),
	allow_headers=('*',),
)

@app.get('/v1/generate_question')
async def generate_question() -> JSONResponse:
	'''
	Эндпоинт для генерации медицинского вопроса.

	Возвращает:
		JSONResponse: Сгенерированный вопрос в формате JSON.
	'''

	result = await model.generate()
	return JSONResponse(content=result)

__all__ = ('app',)