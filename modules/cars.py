from telebot import types
import sqlite3
import datetime
import os
import asyncio
from telebot.async_telebot import AsyncTeleBot
import config
from modules import subsidiary_functions
from database import functions as database_functions

bot = AsyncTeleBot(config.token)
src_path = config.src_path

async def send(message):

    pointer = database_functions.check_user(message)
    if not pointer:
        database_functions.create_new_user(message)

    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton('➰ Audi', callback_data='car_list|audi|0'), 
                      types.InlineKeyboardButton('🌍 BMW', callback_data='car_list|bmw|0'), 
                      types.InlineKeyboardButton('🧭 Mercedes', callback_data='car_list|mercedes|0'))
    markup_inline.add(types.InlineKeyboardButton('🌐 Мультибрендовые', callback_data='car_list|multi|0'),
                      types.InlineKeyboardButton('🛸 АвтоВАЗ', callback_data='car_list|lada|0'),
                      types.InlineKeyboardButton('🎌 Японские', callback_data='car_list|japan|0'))
    markup_inline.add(types.InlineKeyboardButton('👑 Элитные', callback_data='car_list|elite|0'),
                      types.InlineKeyboardButton('🛵 Мотоциклы', callback_data='car_list|moto|0'),
                      types.InlineKeyboardButton('🚁 Вертолеты', callback_data='car_list|helicopter|0'))
    markup_inline.add(types.InlineKeyboardButton('🔙 В главное меню', callback_data='main'),
                      types.InlineKeyboardButton('💎 Эксклюзивы', callback_data='car_list|exclusive|0'))

    await bot.send_photo(message.chat.id, photo=open(f'{src_path}/cars.png', 'rb'),
                         caption='🚗 Здесь представлены разделы автомобилей на сервере. В разделе '
                                 '"эксклюзивы" вы можете найти информацию об автомобиляx, которые '
                                 'выпадают исключительно с кейсов или выдаются, как награды, '
                                 'с боевого пропуска', 
                         reply_markup=markup_inline)
    

async def edit(message):

    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton('➰ Audi', callback_data='car_list|audi|0'), 
                      types.InlineKeyboardButton('🌍 BMW', callback_data='car_list|bmw|0'), 
                      types.InlineKeyboardButton('🧭 Mercedes', callback_data='car_list|mercedes|0'))
    markup_inline.add(types.InlineKeyboardButton('🌐 Мультибрендовые', callback_data='car_list|multi|0'),
                      types.InlineKeyboardButton('🛸 АвтоВАЗ', callback_data='car_list|lada|0'),
                      types.InlineKeyboardButton('🎌 Японские', callback_data='car_list|japan|0'))
    markup_inline.add(types.InlineKeyboardButton('👑 Элитные', callback_data='car_list|elite|0'),
                      types.InlineKeyboardButton('🛵 Мотоциклы', callback_data='car_list|moto|0'),
                      types.InlineKeyboardButton('🚁 Вертолеты', callback_data='car_list|helicopter|0'))
    markup_inline.add(types.InlineKeyboardButton('🔙 В главное меню', callback_data='main'),
                      types.InlineKeyboardButton('💎 Эксклюзивы', callback_data='car_list|exclusive|0'))

    await bot.edit_message_media(chat_id=message.chat.id, media=open(f'{src_path}/cars.png', 'rb'), reply_markup=markup_inline)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, 
                                text='🚗 Здесь представлены разделы автомобилей на сервере. В разделе '
                                     '"эксклюзивы" вы можете найти информацию об автомобиляx, которые '
                                     'выпадают исключительно с кейсов или выдаются, как награды, '
                                     'с боевого пропуска')