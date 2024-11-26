"""
    Это пример запуска в асинхронном режиме.

    Мы сначала создаём новый эвентовый цикл и ставим его как главный,
    потом запускаем на нём функцию main() и при её окончании отключаем
    все соединения, даже если выбросилось исключение (блок finally)

    Не забудьте про установку requirements.txt файла!
"""

import asyncio
from tortoise import Tortoise
from tortoise.connection import connections
from models.common import User

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def test():
    user = await User.create(age=15)
    assert await User.exists(pk=user.id)
    await user.delete()
    print("Всё хорошо работает!")


async def main():
    await Tortoise.init(
        db_url="sqlite://database.db",
        modules={"app": ["models.common"]}
    )
    await Tortoise.generate_schemas(safe=True)
    await test()


try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(connections.close_all())
    loop.close()