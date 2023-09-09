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
from modules.discord_callback import myads

bot = AsyncTeleBot(config.token)


async def change_timer(message):
    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton(f'3 часа', callback_data='changing_timer|180'))
    markup_inline.add(types.InlineKeyboardButton(f'4 часа', callback_data='changing_timer|240'))
    markup_inline.add(types.InlineKeyboardButton(f'5 часов', callback_data='changing_timer|300'))
    markup_inline.add(types.InlineKeyboardButton(f'6 часов', callback_data='changing_timer|360'))
    markup_inline.add(types.InlineKeyboardButton('🔙 Назад в раздел мои объявления', callback_data='myads'))
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                text='🕐 Выберите таймер: ')
    await bot.edit_message_reply_markup(chat_id=message.chat.id, 
                                        message_id=message.message_id, reply_markup=markup_inline)
    

async def changing_timer(message, timer: int):

    database_functions.update_column_in_table_by_userid(
        data=timer, column='timer', table='user_data', user_id=message.chat.id)
    
    await myads.edit(message=message)