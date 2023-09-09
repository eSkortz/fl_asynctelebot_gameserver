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
    markup_inline.add(types.InlineKeyboardButton('🌊 0-5 метров', callback_data='fishes|0'),
                      types.InlineKeyboardButton('🌊 5-15 метров', callback_data='fishes|5'),
                      types.InlineKeyboardButton('🌊 15-25 метров', callback_data='fishes|15'))
    markup_inline.add(types.InlineKeyboardButton('🌊 25-45 метров', callback_data='fishes|25'),
                      types.InlineKeyboardButton('🌊 45-65 метров', callback_data='fishes|45'),
                      types.InlineKeyboardButton('🌊 65-85 метров', callback_data='fishes|65'))
    markup_inline.add(types.InlineKeyboardButton('🔙 В главное меню', callback_data='main'),
                      types.InlineKeyboardButton('🌊 от 85 метров', callback_data='fishes|85'))

    await bot.send_photo(message.chat.id, photo=open(f'{src_path}/fishing.png', 'rb'),
                         caption='🐟 Это раздел рыбалки, здесь вы можете посмотреть какую рыбу на какой глубине, '
                                 'на какую наживку/удочку, вы можете поймать, сколько это займет времени, и сколько '
                                 'будет стоить пойманная вами рыба', 
                         reply_markup=markup_inline)
    

async def edit(message):

    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton('🌊 0-5 метров', callback_data='fishes|0'),
                      types.InlineKeyboardButton('🌊 5-15 метров', callback_data='fishes|5'),
                      types.InlineKeyboardButton('🌊 15-25 метров', callback_data='fishes|15'))
    markup_inline.add(types.InlineKeyboardButton('🌊 25-45 метров', callback_data='fishes|25'),
                      types.InlineKeyboardButton('🌊 45-65 метров', callback_data='fishes|45'),
                      types.InlineKeyboardButton('🌊 65-85 метров', callback_data='fishes|65'))
    markup_inline.add(types.InlineKeyboardButton('🔙 В главное меню', callback_data='main'),
                      types.InlineKeyboardButton('🌊 от 85 метров', callback_data='fishes|85'))

    await bot.edit_message_media(chat_id=message.chat.id, media=open(f'{src_path}/fishing.png', 'rb'), reply_markup=markup_inline)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, 
                                text='🐟 Это раздел рыбалки, здесь вы можете посмотреть какую рыбу на какой глубине, '
                                     'на какую наживку/удочку, вы можете поймать, сколько это займет времени, и сколько '
                                     'будет стоить пойманная вами рыба')