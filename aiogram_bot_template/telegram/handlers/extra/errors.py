from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram_i18n import I18nContext

from ....exceptions import BotError

router: Final[Router] = Router(name=__name__)

ERROR_MESSAGE = 'Что-то пошло не так'


@router.error(ExceptionTypeFilter(BotError), F.update.message)
async def handle_some_error(error: ErrorEvent) -> Any:
    await error.update.message.answer(text=ERROR_MESSAGE)
