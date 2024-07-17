from aiogram import Bot, Dispatcher
from dishka import Provider, Scope, provide

from aiogram_bot_template.app_config import AppConfig
from aiogram_bot_template.factory.app_config import create_app_config
from aiogram_bot_template.factory.bot import create_bot
from aiogram_bot_template.factory.dispatcher import create_dispatcher


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_config(self) -> AppConfig:
        return create_app_config()

class BotProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_bot(self, config: AppConfig) -> Bot:
        return create_bot(config=config)
    
class DispatcherProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_dispatcher(self, config: AppConfig) -> Dispatcher:
        return create_dispatcher(config=config)