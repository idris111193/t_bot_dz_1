import re

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile

from config import bot
from database.async_db import AsyncDatabase
from database import sql_queries
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.like_dislike import after_donate_keyboard

router = Router()


class DonateState(StatesGroup):
    amount = State()

@router.callback_query(lambda call: "donate_" in call.data)
async def donate_start(call: CallbackQuery,
                       state: FSMContext,
                       db=AsyncDatabase()):
    await call.message.delete()
    recipient_tg_id = re.sub("donate_", "", call.data)
    user = await db.execute_query(
                query=sql_queries.SELECT_USER_QUERY,
                params=(
                    call.from_user.id,
                ),
                fetch="one"
            )

    await bot.send_message(
        chat_id=call.from_user.id,
        text=f"Hello how much money would you to donate?\n"
             f"You have {user['BALANCE']}"
    )
    await state.update_data(recipient_td=recipient_tg_id)
    await state.update_data(limit=user['BALANCE'])
    await state.set_state(DonateState.amount)

@router.message()
async def process_donate_transactions(message: types.Message,
                                      state: FSMContext,
                                      db=AsyncDatabase()
                                      ):
    amount = message.text
    try:
        int(amount)
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Please enter a valid amount and make it numeric.\n"
                 "Please retry donate"
        )
        await state.clear()
        return

    data = await state.get_data()
    if int(amount) > data['limit'] or int(amount) <= 0:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Not enough money.\n"
                 "Please retry donate"
        )
        await state.clear()
        return

    await db.execute_query(
        query=sql_queries.UPDATE_SENDER_BALANCE_COLUMN_QUERY,
        params=(
            int(amount),
            message.from_user.id,
        ),
        fetch="none"
    )
    await db.execute_query(
        query=sql_queries.UPDATE_USER_BALANCE_COLUMN_QUERY,
        params=(
            int(amount),
            data['recipient_tg_id'],
        ),
        fetch="none"
    )
    await db.execute_query(
        query=sql_queries.INSERT_LIKE_QUERY,
        params=(
            None,
            data['recipient_tg_id'],
            message.from_user.id,
            2,
        ),
        fetch="none"
    )
    await db.execute_query(
        query=sql_queries.INSERT_DONATE_QUERY,
        params=(
            None,
            message.from_user.id,
            data['recipient_tg_id'],
            int(amount),
        ),
        fetch="none"
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Donate sent successfully!\n",
        reply_markup=await after_donate_keyboard()
    )
    await bot.send_message(
        chat_id=data['recipient_tg_id'],
        text=f"Someone donated ur profile\n"
             f"Amount: {amount}$\n"
    )
