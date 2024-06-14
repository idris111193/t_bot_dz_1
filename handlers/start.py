import sqlite3
from email import message

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import create_start_link

from config import bot
from database.async_db import AsyncDatabase
from database import sql_queries
from keyboards.start import start_menu_keyboard

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

async def process_reference_link(token, message, db=AsyncDatabase()):
        link = await create_start_link(bot=bot, payload=token)

        inviter =   await db.execute_query(
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

async def start_menu_keyboard_with_referral():
    keyboard = InlineKeyboardMarkup(row_width=1)
    referral_button = InlineKeyboardButton(text=" Invite Friends",
                                           callback_data="reference_menu")
    keyboard.add(referral_button)
    return keyboard

    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello {message.from_user.first_name}\n"
             f"Im your halp_bot, i can register your in profile mode\n"
             f"new function wil bi...",
        reply_markup=await start_menu_keyboard()
    )

    async def reference_menu_keyboard():
        keyboard = InlineKeyboardMarkup(row_width=1)
        invite_button = InlineKeyboardButton(text=" Invite Friends", callback_data="reference_invite")
        balance_button = InlineKeyboardButton(text=" Check Balance", callback_data="reference_balance")
        keyboard.add(invite_button, balance_button)
        return keyboard

    async def reference_menu_keyboard(call: CallbackQuery):
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Welcome to the referral program!\n'
                 'Invite your friends and earn bonuses.',
            reply_markup=await reference_menu_keyboard()
        )

    async def reference_balance_call(call: CallbackQuery,
                                     db=AsyncDatabase()):
        user = await db.execute_query(
            query=sql_queries.SELECT_USER_QUERY,
            params=(
                call.from_user.id,
            ),
            fetch="one"
        )
        if user:
            balance = user.get("BALANCE", 0)
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f'Your balance: {balance}'
            )
        else:
            await bot.send_message(
                chat_id=call.from_user.id,
                text="Your balance information is not available at the moment."
            )











