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

    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    markup_inline.add(types.InlineKeyboardButton('🚗 Автомобили', callback_data='cars'))
    markup_inline.add(fishing_button = types.InlineKeyboardButton('🐟 Рыбалка', callback_data='fishing'))
    markup_inline.add(discord_button = types.InlineKeyboardButton('🛒 Торговая площадка discord', callback_data='discord'))
    markup_inline.add(types.InlineKeyboardButton('📤 Официальный discord-сервер проекта', url='https://discord.com/channels/668553971618807818/751628125087072346'))

    await bot.send_photo(message.chat.id, photo=open(f'{src_path}/main.png', 'rb'),
                         caption='🎮 Это smotra assistant, сервис созданный для помощи при вопросах, возникающих '
                                 'в ходе игрового процесса на сервере smotra rage. Здесь вы сможете найти '
                                 'информацию об автомобилях, рыбалке, некоторых работах, '
                                 'а также автоматизировать процесс торговли на официальном discord-сервере ',
                         reply_markup=markup_inline)
    

async def edit(message):

    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    markup_inline.add(types.InlineKeyboardButton('🚗 Автомобили', callback_data='cars'))
    markup_inline.add(fishing_button = types.InlineKeyboardButton('🐟 Рыбалка', callback_data='fishing'))
    markup_inline.add(discord_button = types.InlineKeyboardButton('🛒 Торговая площадка discord', callback_data='discord'))
    markup_inline.add(types.InlineKeyboardButton('📤 Официальный discord-сервер проекта', url='https://discord.com/channels/668553971618807818/751628125087072346'))

    await bot.edit_message_media(chat_id=message.chat.id, media=open(f'{src_path}/main.png', 'rb'), reply_markup=markup_inline)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, 
                                text='🎮 Это smotra assistant, сервис созданный для помощи при вопросах, возникающих '
                                     'в ходе игрового процесса на сервере smotra rage. Здесь вы сможете найти '
                                     'информацию об автомобилях, рыбалке, некоторых работах, '
                                     'а также автоматизировать процесс торговли на официальном discord-сервере ')