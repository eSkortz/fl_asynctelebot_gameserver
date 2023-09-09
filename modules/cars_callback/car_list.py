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

bot = AsyncTeleBot(config.token)

def make_markup(car_mark, page_id):

    cars = database_functions.get_all_cars_by_mark(car_mark)

    back_button_bool = True
    next_button_bool = True

    first_id = page_id

    if len(cars) > page_id + 10:
        last_id = len(cars)
        next_button_bool = False
    elif page_id == 0:
        back_button_bool = False
    else:
        last_id = page_id + 10

    pref_cost = str(cars[i][3] * 100 // 1000000)

    markup_inline = types.InlineKeyboardMarkup()
    for i in range(first_id, last_id):
        markup_inline.add(types.InlineKeyboardButton(f'{subsidiary_functions.emoji_from_mark(car_mark)} {cars[i][1]} 'f'- {subsidiary_functions.pref_cost[:-2]}.{pref_cost[-2:]}kk',callback_data=f'detail_car|{car_mark}|{cars[i][0]}'))

    back_page_button = types.InlineKeyboardButton('⬅ Назад', callback_data=f'car_list|{car_mark}|{page_id-10}')
    next_page_button = types.InlineKeyboardButton('Вперед ➡', callback_data=f'car_list|{car_mark}|{page_id+10}')

    if back_button_bool and next_button_bool:
        markup_inline.add(back_page_button, next_page_button)
    elif back_button_bool:
        markup_inline.add(back_page_button)
    elif next_button_bool:
        markup_inline.add(next_page_button)

    markup_inline.add(types.InlineKeyboardButton('🔙 К списку разделов', callback_data='cars'))

    return markup_inline

async def edit(message, car_mark, page_id):

    markup_inline = make_markup(car_mark, page_id)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f'{subsidiary_functions.emoji_from_mark(car_mark)} ' \
                                f'Список автомобилей {car_mark} ({page_id}-{page_id+10})')
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup_inline)