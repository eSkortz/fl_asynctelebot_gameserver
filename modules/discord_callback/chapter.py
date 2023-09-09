from ctypes import pointer
from email import message
from telebot import types
import sqlite3
import datetime
import os
import asyncio
from telebot.async_telebot import AsyncTeleBot
import config
from database import functions as database_functions
from modules import subsidiary_functions
from modules import input_broker as broker
from modules import start, cars, fishing, discord
from modules.cars_callback import car_list, detail_car

bot = AsyncTeleBot(config.token)
src_path = config.src_path


def make_markup(chapter: str):

    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    markup_inline.add(types.InlineKeyboardButton(
        '♻ Включить/отключить объявление', callback_data=f'onoff|{chapter}'))
    markup_inline.add(types.InlineKeyboardButton(
        '📝 Отредактировать текст объявления', callback_data=f'edit_text|{chapter}'))
    markup_inline.add(types.InlineKeyboardButton(
        '🎑 Добавить фото для объявления', callback_data=f'edit_photo|{chapter}'))
    markup_inline.add(types.InlineKeyboardButton(
        '🧨 Удалить все фото', callback_data=f'delete_photo|{chapter}'))
    markup_inline.add(types.InlineKeyboardButton(
        '🗂 Показать все фото объявления', callback_data=f'show_all_photo|{chapter}'))
    markup_inline.add(types.InlineKeyboardButton(
        '🔙 Назад в раздел мои объявления', callback_data='myads'))
    
    return markup_inline
    


async def edit(message, chapter: str) -> None:

    discord_token = database_functions.get_value_from_column_and_table_by_userid(
        column='discord_token', table='user_data', user_id=message.chat.id
        )
    
    pointer = database_functions.get_value_from_column_and_table_by_userid(
        column='pointer', table=f'users_{chapter}', user_id=message.chat.id
    )
    text = database_functions.get_value_from_column_and_table_by_userid(
        column='text', table=f'users_{chapter}', user_id=message.chat.id
    )
    images = database_functions.get_value_from_column_and_table_by_userid(
        column='images', table=f'users_{chapter}', user_id=message.chat.id
    )
    message_text = subsidiary_functions.text_from_chapter(chapter)

    markup_inline = make_markup(chapter=chapter)

    match images:
        case None:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                        text=f'Обьявление для раздела {message_text} - ' \
                                            f'{subsidiary_functions.point_to_status(pointer)}\n\nТекст ' \
                                            f'объявления: "{text[:30]}..."\n\nТекущий auth-token: "{discord_token}"')
            await bot.edit_message_reply_markup(chat_id=message.chat.id, 
                                                message_id=message.message_id, reply_markup=markup_inline)
        case _:
            images_mas = images.split('|')
            await bot.edit_message_media(chat_id=message.chat.id, 
                                         media=open(f'{src_path}/users/{message.chat.id}/{images_mas[0]}', 'rb'), 
                                         reply_markup=markup_inline)
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                        text=f'Обьявление для раздела {message_text} - ' \
                                            f'{subsidiary_functions.point_to_status(pointer)}\n\nТекст ' \
                                            f'объявления: "{text[:30]}..."\n\nТекущий auth-token: "{discord_token}"')