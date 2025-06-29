import asyncio
from model.Model import Model

async def main() -> None:
	model = Model()
	reply = await model.generate()
	print(reply)

asyncio.run(main())