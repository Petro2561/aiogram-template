from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

if TYPE_CHECKING:
    from ....services.database import DBUser

router: Final[Router] = Router(name=__name__)

START_MESSAGE = 'Привет'


@router.message(CommandStart())
async def start_command(message: Message, user: DBUser) -> Any:
    await message.answer(text=f'{START_MESSAGE}, {user.name}!')    
