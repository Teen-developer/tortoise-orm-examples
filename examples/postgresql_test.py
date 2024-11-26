"""
    Пример соединения с PostgreSQL базой.

    Перед запуском обновите 3 переменные ниже.
    Не забудьте про установку requirements.txt файла!
"""

POSTGRES_PASSWORD = "AndrewWasHere"
POSTGRES_IP = "127.0.0.1"
POSTGRES_PORT = 5432

import asyncio
import asyncpg
from tortoise import Tortoise
from tortoise.connection import connections
from models.common import User

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def test():
    print("Пытаемся создать пользователя...")
    user = await User.create(age=15)
    assert await User.exists(pk=user.id)
    print("Получилось! База принимает соединения!")
    await user.delete()


async def main():
    connectionString = (
        f"asyncpg://postgres:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_IP}:{POSTGRES_PORT}/postgres"
    )

    print("Подключение по этой ссылке:")
    print(connectionString)

    await Tortoise.init(
        db_url=connectionString,
        modules={"app": ["models.common"]}
    )
    await Tortoise.generate_schemas(safe=True)
    await test()


try:
    loop.run_until_complete(main())
except ConnectionRefusedError:
    print("Порт не верен")
except asyncpg.exceptions.ConnectionDoesNotExistError:
    print("Скорее всего, пароль в POSTGRES_PASSWORD не верен или сервер не запущен")
    print("Проверьте ссылку, по которой осуществляется подключение")
else:
    print("🟩 Подключение успешно! Поздравляю! 🥳")
finally:
    loop.run_until_complete(connections.close_all())
    loop.close()