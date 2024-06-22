import sqlite3
from email import message

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from config import bot
from database.async_db import AsyncDatabase
from database import sql_queries
from keyboards.start import start_menu_keyboard
from scraper.news_scraper import NewsScraper

router = Router()


@router.message(Command("start"))
async def start_menu(message: types.Message,
                     db=AsyncDatabase()):
    command = message.text
    token = command.split()
    print(token)
    if len(token) > 1:
        await process_reference_link(token=token[1], message=message)


    await db.execute_query(
        query=sql_queries.INSERT_USER_QUERY,
        params=(
            None,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            None,
            0
        ),
        fetch="none"
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello {message.from_user.first_name}\n"
             f"Im your halp_bot, i can register your in profile mode\n"
             f"new function wil bi...",
        reply_markup=await start_menu_keyboard()
    )

async def process_reference_link(token, message, db=AsyncDatabase()):
        link = await create_start_link(bot=bot, payload=token)

        inviter = await db.execute_query(
        query=sql_queries.SELECT_USER_BY_LINK_QUERY,
        params=(
            link,
        ),
        fetch="one"
    )
        print(inviter)
        if inviter['TELEGRAM_ID'] == message.from_user.id:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="hello you can't use our link"
            )
            return
        try:
            await db.execute_query(
                query=sql_queries.UPDATE_USER_BALANCE_COLUMN_QUERY,
                params=(
                    100,
                    inviter['TELEGRAM_ID'],
                ),
                fetch="none"
            )
            await db.execute_query(
                query=sql_queries.INSERT_REFERENCE_QUERY,
                params=(
                    None,
                    inviter['TELEGRAM_ID'],
                    message.from_user.id,
                ),
                fetch="none"
            )
        except sqlite3.IntegrityError:
            pass




@router.callback_query(lambda call: call.data == 'news')
async def news_call(call: CallbackQuery):
    scraper = NewsScraper()
    data = scraper.scrape_data()
    print(data)
    for news in data:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="" + news
        )








