from aiogram import Router, types
from aiogram.filters import Command
from config import bot
from database.async_db import AsyncDatabase
from database import sql_queries

router = Router()

@router.message(Command("start"))
async def start_menu(message: types.message,
                     db=AsyncDatabase()):
    print(message)
    await db.execute_query(
        query=sql_queries.INSERT_USER_QUERY,
        params=(
            None,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        ),
        fetch="None"
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text="HELLO"
    )


async def start_command(message: types.message):
  user_id = message.from_user.id
  username = message.from_user.username