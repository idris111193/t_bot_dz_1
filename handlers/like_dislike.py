from aiogram import Router, types
from aiogram.types import CallbackQuery, FSInputFile

from config import bot
import random
import re
from database.async_db import AsyncDatabase
from database import sql_queries
from keyboards.like_dislike import like_dislike_keyboard

router = Router()


@router.callback_query(lambda call: call.data == 'all_profiles')
async def all_profiles_call(call: CallbackQuery,
                            db=AsyncDatabase()):
    print(call.message.caption)
    if call.message.caption is None:
        pass
    else:
        await call.message.delete()
    profiles = await db.execute_query(
        query=sql_queries.SELECT_ALL_PROFILES,
        params=(
            call.from_user.id,
            call.from_user.id,
        ),
        fetch="all"
    )
    print(profiles)
    if not profiles:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You have liked all profiles, come later",
        )
    else:
        random_profile = random.choice(profiles)
        photo = FSInputFile(random_profile['PHOTO'])
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=f"Name: {random_profile['NICKNAME']}\n"
                    f"Bio: {random_profile['BIO']}\n",
            reply_markup=await like_dislike_keyboard(tg_id=random_profile['TELEGRAM_ID'])
        )


@router.callback_query(lambda call: "like_" in call.data)
async def detect_like_call(call: CallbackQuery,
                           db=AsyncDatabase()):

    owner_tg_id = re.sub("like_", "", call.data)

    await db.execute_query(
        query=sql_queries.INSERT_LIKE_QUERY,
        params=(
            None,
            owner_tg_id,
            call.from_user.id,
            1,
        ),
        fetch="none"
    )

    @router.callback_query(lambda call: "dislike" in call.data)
    async def detect_dislike_call(call: CallbackQuery,
                               db=AsyncDatabase()):
        owner_tg_id = re.sub("dislike", "", call.data)

        await db.execute_query(
            query=sql_queries.INSERT_LIKE_QUERY,
            params=(
                None,
                owner_tg_id,
                call.from_user.id,
                0,
            ),
            fetch="none"
        )

    await all_profiles_call(call=call)