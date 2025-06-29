import asyncio
from model.Model import Model

async def main() -> None:
	model = Model()

	reply = await model.ask((
		{'user': 'Здравствуйте. У меня болит грудь уже несколько часов.'},
	))

	print('AI:', reply)

asyncio.run(main())