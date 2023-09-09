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

def make_markup(car_mark, car_id):

    car = database_functions.get_car_from_table_and_carid(car_mark=car_mark, car_id=car_id)
    car_model, car_max_speed, car_cost, car_photo, car_trunk = car[1], car[2], car[3], car[4], car[6]
    if car[5] == 0:
        car_obves = 'Нет обвесов'
    else:
        car_obves = 'Доступны обвесы'

    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    markup_inline.add(types.InlineKeyboardButton(f'🔙 К списку автомобилей {car_mark}', callback_data=f'car_list|{car_mark}|0'))
    match car_mark:
        case 'moto':
            caption = f'🚗 Модель: {car_model}\n' \
                        f'🗿 Максимальная скорость: {car_max_speed} км/ч\n' \
                        f'💰 Гос. стоимость: {subsidiary_functions.points_to_cost(car_cost)} руб.\n' \
                        f'♻ Стоимость слива: {subsidiary_functions.points_to_cost(int(car_cost * 0.75))} руб.\n' \
                        f'📦 Мест в багажнике: {car_trunk}\n' \
                        f'👄 Наличие обвесов: {car_obves}\n\n' \
                        f'⚙ Тюнинг:\n' \
                        f'Фулл тюнинг с турбиной - {subsidiary_functions.points_to_cost(int(car_cost * 0.168))} руб.\n' \
                        f'Фулл тюнинг без турбины - {subsidiary_functions.points_to_cost(int(car_cost * 0.141))} руб.\n\n' \
                        f'Двигатель - {subsidiary_functions.points_to_cost(int(car_cost * 0.063))} руб.\n' \
                        f'Коробка передач - {subsidiary_functions.points_to_cost(int(car_cost * 0.042))} руб.\n' \
                        f'Тормоза - {subsidiary_functions.points_to_cost(int(car_cost * 0.036))} руб.\n' \
                        f'Турбина - {subsidiary_functions.points_to_cost(int(car_cost * 0.0345))} руб.\n'
        case 'helicopter':
            caption = f'🚗 Модель: {car_model}\n' \
                        f'🗿 Максимальная скорость: {car_max_speed} км/ч\n' \
                        f'💰 Гос. стоимость: {subsidiary_functions.points_to_cost(car_cost)} руб.\n' \
                        f'♻ Стоимость слива: {subsidiary_functions.points_to_cost(int(car_cost * 0.75))} руб.\n' \
                        f'📦 Мест в багажнике: {car_trunk}\n' \
                        f'👄 Наличие обвесов: {car_obves}\n'
        case _:
            caption = f'🚗 Модель: {car_model}\n' \
                        f'🗿 Максимальная скорость: {car_max_speed} км/ч\n' \
                        f'💰 Гос. стоимость: {subsidiary_functions.points_to_cost(car_cost)} руб.\n' \
                        f'♻ Стоимость слива: {subsidiary_functions.points_to_cost(int(car_cost * 0.75))} руб.\n' \
                        f'📦 Мест в багажнике: {car_trunk}\n' \
                        f'👄 Наличие обвесов: {car_obves}\n\n' \
                        f'⚙ Тюнинг:\n' \
                        f'Фулл тюнинг с внешкой - {subsidiary_functions.points_to_cost(int(car_cost * 0.22125))} руб.\n' \
                        f'Фулл тюнинг без турбины и внешки' \
                        f' - {subsidiary_functions.points_to_cost(int(car_cost * 0.141))} руб.\n\n' \
                        f'Двигатель - {subsidiary_functions.points_to_cost(int(car_cost * 0.063))} руб.\n' \
                        f'Коробка передач - {subsidiary_functions.points_to_cost(int(car_cost * 0.042))} руб.\n' \
                        f'Тормоза - {subsidiary_functions.points_to_cost(int(car_cost * 0.036))} руб.\n' \
                        f'Турбина - {subsidiary_functions.points_to_cost(int(car_cost * 0.0345))} руб.\n\n' \
                        f'Тонировка - {subsidiary_functions.points_to_cost(int(car_cost * 0.012))} руб.\n' \
                        f'Ксенон/Неон - {subsidiary_functions.points_to_cost(int(car_cost * 0.018))} руб.\n' \
                        f'Пулестойкие покрышки - {subsidiary_functions.points_to_cost(int(car_cost * 0.033))} руб.\n' \
                        f'Параметры колес/высота подвески' \
                        f' - {subsidiary_functions.points_to_cost(int(car_cost * 0.01))} руб.\n'
    return caption, car_photo, markup_inline
    

async def edit(message, car_mark, car_id):
    caption, car_photo, markup_inline = make_markup(car_mark=car_mark, car_id=car_id)
    await bot.edit_message_media(chat_id=message.chat.id, media=open(f'{car_photo}', 'rb'), reply_markup=markup_inline)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=caption)