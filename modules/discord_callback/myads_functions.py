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


async def onoff(message, chapter_name):

    pointer = database_functions.get_value_from_column_and_table_by_userid(
        column='pointer', table=f'users_{chapter_name}', user_id=message.chat.id
    )

    match pointer:
        case 0:
            new_pointer_data = 1
        case 1:
            new_pointer_data = 0

    database_functions.update_column_in_table_by_userid(
        data=new_pointer_data, column='pointer', table=f'users_{chapter_name}', user_id=message.chat.id)
    
    await chapter.edit(message, chapter=chapter_name)


async def delete_photo(message, chapter: str):

    images = database_functions.get_value_from_column_and_table_by_userid(
        column='images', table=f'users_{chapter}', user_id=message.chat.id
    )

    database_functions.update_column_in_table_by_userid(
        data=None, column='images', table=f'users_{chapter}', user_id=message.chat.id)
    
    match images:
        case None:
            pass
        case _:
            images_mas = images.split('|')
            for index in range(len(images_mas)):
                os.remove(f'{src_path}/users/{images_mas[index]}')
    
    await chapter.edit(message=message, chapter=chapter)


async def edit_photo(message, chapter: str):
    
    database_functions.update_column_in_table_by_userid(
        data=1, column=f'change_photo_{chapter}', table='state_pointers', user_id=message.chat.id)

    await bot.edit_message_media(chat_id=message.chat.id, media=None, reply_markup=None)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, 
                                text='🎑 Отправьте новую фотографию (Фотографию нужно прикрепить как фото' \
                                    ' и причем только одну!): ')
    

async def edit_text(message, chapter: str):
    
    database_functions.update_column_in_table_by_userid(
        data=1, column=f'change_text_{chapter}', table='state_pointers', user_id=message.chat.id)

    await bot.edit_message_media(chat_id=message.chat.id, media=None, reply_markup=None)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, 
                                text='📝 Отправьте новый текст (Текст не должен содержать символ "/"): ')
    


async def show_all_photo(message, chapter: str):
    images = database_functions.get_value_from_column_and_table_by_userid(
        column='images', table=f'users_{chapter}', user_id=message.chat.id
    )

    match images:
        case None:
            pass
        case _:
            images_mas = images.split('|')
            media_group = []
            for i in range(len(images_mas)):
                media_group.append(
                    types.InputMediaPhoto(open(f'{src_path}/users/{message.chat.id}/{images_mas[i]}', 'rb')))
            markup_inline = types.InlineKeyboardMarkup(row_width=1)
            markup_inline.add(
                types.InlineKeyboardButton('🔙 Назад к разделу', callback_data=f'chapter|{chapter}'))
            await bot.edit_message_media(chat_id=message.chat.id, 
                                         media=media_group, 
                                         reply_markup=markup_inline)
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                        text=None)