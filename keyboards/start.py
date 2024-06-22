from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def start_menu_keyboard():
    registration_button = InlineKeyboardButton(
        text= 'Registration 🔥',
        callback_data= 'registration'
    )

    profile_button = InlineKeyboardButton(
        text='My profile',
        callback_data='my_profile'
    )
    profiles_button = InlineKeyboardButton(
        text='View profiles',
        callback_data='all_profiles'
    )

    reference_menu_button = InlineKeyboardButton(
        text='Reference Menu',
        callback_data='reference_menu'
    )

    link_button = InlineKeyboardButton(
        text="Latest News",
        callback_data="news"
    )

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [registration_button],
        [profile_button],
        [profiles_button],
        [reference_menu_button],
        [link_button],
    ])
    return markup

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def start_referal_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    referral_button = InlineKeyboardButton(text="call",
                                           callback_data="reference menu")
    keyboard.add(referral_button)
    return keyboard
