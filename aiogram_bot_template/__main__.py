import asyncio

from aiogram import Bot, Dispatcher
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from aiogram_bot_template.dishka_di import (BotProvider, ConfigProvider,
                                            DispatcherProvider)
from aiogram_bot_template.utils.loggers import setup_logger

from .app_config import AppConfig
from .runners import run_polling, run_webhook


def main() -> None:
    setup_logger()
    container = make_async_container(BotProvider(), ConfigProvider(), DispatcherProvider())
    loop = asyncio.new_event_loop()
    bot = loop.run_until_complete(container.get(Bot))
    dispatcher = loop.run_until_complete(container.get(Dispatcher))
    config = loop.run_until_complete(container.get(AppConfig))
    loop.close()
    setup_dishka(container=container, router=dispatcher)
    if config.webhook.use:
        return run_webhook(dispatcher=dispatcher, bot=bot, config=config)
    return run_polling(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    main()
