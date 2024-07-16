from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from redis.asyncio import ConnectionPool, Redis

from ..app_config import AppConfig
from ..middlewares import DBSessionMiddleware, UserMiddleware
from ..services.database import create_pool
from ..telegram.handlers import admin, common, extra
from ..utils import msgspec_json as mjson


def _setup_outer_middlewares(dispatcher: Dispatcher, config: AppConfig) -> None:
    pool = dispatcher["session_pool"] = create_pool(
        dsn=config.postgres.build_dsn(), enable_logging=config.common.sqlalchemy_logging
    )

    dispatcher.update.outer_middleware(DBSessionMiddleware(session_pool=pool))
    dispatcher.update.outer_middleware(UserMiddleware())

def _setup_inner_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())


def create_dispatcher(config: AppConfig) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    redis: Redis = Redis(
        connection_pool=ConnectionPool(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
        )
    )

    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(redis=redis, json_loads=mjson.decode, json_dumps=mjson.encode),
        config=config,
    )
    dispatcher.include_routers(admin.router, common.router, extra.router)
    _setup_outer_middlewares(dispatcher=dispatcher, config=config)
    _setup_inner_middlewares(dispatcher=dispatcher)
    return dispatcher
