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


def make_markup(message):

    transport_bool = subsidiary_functions.point_to_status(
        database_functions.get_value_from_column_and_table_by_userid(
            column='pointer', table='users_transport', user_id=message.chat.id))
    numbers_bool = subsidiary_functions.point_to_status(
        database_functions.get_value_from_column_and_table_by_userid(
            column='pointer', table='users_numbers', user_id=message.chat.id))
    homes_bool = subsidiary_functions.point_to_status(
        database_functions.get_value_from_column_and_table_by_userid(
            column='pointer', table='users_homes', user_id=message.chat.id))
    business_bool = subsidiary_functions.point_to_status(
        database_functions.get_value_from_column_and_table_by_userid(
            column='pointer', table='users_businesses', user_id=message.chat.id))
    clothes_bool = subsidiary_functions.point_to_status(
        database_functions.get_value_from_column_and_table_by_userid(
            column='pointer', table='users_clothes', user_id=message.chat.id))
    weapon_bool = subsidiary_functions.point_to_status(
        database_functions.get_value_from_column_and_table_by_userid(
            column='pointer', table='users_weapon', user_id=message.chat.id))
    loot_bool = subsidiary_functions.point_to_status(
        database_functions.get_value_from_column_and_table_by_userid(
            column='pointer', table='users_loot', user_id=message.chat.id))
    general_bool = subsidiary_functions.point_to_status(
        database_functions.get_value_from_column_and_table_by_userid(
            column='pointer', table='users_general', user_id=message.chat.id))
    services_bool = subsidiary_functions.point_to_status(
        database_functions.get_value_from_column_and_table_by_userid(
            column='pointer', table='users_services', user_id=message.chat.id))

    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    markup_inline.add(types.InlineKeyboardButton(f'🚗 Транспорт | {transport_bool}',
                                                    callback_data='chapter|transport'))
    markup_inline.add(types.InlineKeyboardButton(f'🎱 Номера | {numbers_bool}',
                                                callback_data='chapter|number'))
    markup_inline.add(types.InlineKeyboardButton(f'🏠 Дома | {homes_bool}',
                                                callback_data='chapter|home'))
    markup_inline.add(types.InlineKeyboardButton(f'🏦 Бизнесы | {business_bool}',
                                                    callback_data='chapter|business'))
    markup_inline.add(types.InlineKeyboardButton(f'🥋 Одежда | {clothes_bool}',
                                                callback_data='chapter|clothes'))
    markup_inline.add(types.InlineKeyboardButton(f'🔫 Оружие | {weapon_bool}',
                                                callback_data='chapter|weapon'))
    markup_inline.add(types.InlineKeyboardButton(f'📦 Лут-предметы | {loot_bool}',
                                                callback_data='chapter|loot'))
    markup_inline.add(types.InlineKeyboardButton(f'📊 Торговая общий | {general_bool}',
                                                callback_data='chapter|general'))
    markup_inline.add(types.InlineKeyboardButton(f'💵 Услуги | {services_bool}',
                                                callback_data='chapter|main'))
    markup_inline.add(types.InlineKeyboardButton(f'🕐 Сменить таймер',
                                                callback_data='change_timer'))
    markup_inline.add(types.InlineKeyboardButton('🔙 Назад к торговой площадке discord',
                                                callback_data='discord'))
    
    return markup_inline
    


async def edit(message) -> None:
    user_timer = database_functions.get_value_from_column_and_table_by_userid(column='timer', table='user_data', user_id=message.chat.id)

    markup_inline = make_markup(message=message)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                text=f'📝 Мои объявления в smotra (раздел|статус)\n ' \
                                     f'🕐 Текущий таймер: {user_timer} минут')
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup_inline)