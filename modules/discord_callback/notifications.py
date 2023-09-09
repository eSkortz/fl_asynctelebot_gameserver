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
from modules.discord_callback import chapter

bot = AsyncTeleBot(config.token)
src_path = config.src_path


async def notifications(message):

    flags = database_functions.get_value_from_column_and_table_by_userid(
        column='flags', table='user_data', user_id=message.chat.id)
    
    markup_inline = types.InlineKeyboardMarkup(row_width=1)

    flags_mas = []
    match flags:
        case None:
            pass
        case _:
            flags_mas = flags.split('|')
            for index in range(len(flags_mas)):
                markup_inline.add(types.InlineKeyboardButton(f'{flags_mas[index]}', callback_data='null'))

    if len(flags_mas) < 9:
        markup_inline.add(types.InlineKeyboardButton('✏ Добавить ключевое слово', callback_data='add_flag'))
    markup_inline.add(types.InlineKeyboardButton('🗑 Очистить ключевые слова', callback_data='delete_flags'))
    markup_inline.add(types.InlineKeyboardButton('🔙 Назад к торговой площадке discord', callback_data='discord'))

    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                    text=f'🔔 Уведомления (ключевые слова и их вариации)\n' \
                                        'Например: "6гм" или "bmw f10")')
    await bot.edit_message_reply_markup(chat_id=message.chat.id, 
                                        message_id=message.message_id, reply_markup=markup_inline)


async def add_flag(message):

    database_functions.update_column_in_table_by_userid(
        data=1, column='adding_flag', table='state_pointers', user_id=message.chat.id)
    
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                    text=f'✏ Введите новое ключевое слово (Например: "6гм" или "bmw f10"): ')
    await bot.edit_message_reply_markup(chat_id=message.chat.id, 
                                        message_id=message.message_id, reply_markup=None)
    

async def delete_flags(message):

    database_functions.update_column_in_table_by_userid(
        data=None, column='flags', table='user_data', user_id=message.chat.id)
    
    await notifications(message=message)