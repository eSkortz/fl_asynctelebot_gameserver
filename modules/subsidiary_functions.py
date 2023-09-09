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

# Простая функция, возвращает читабельное числовое значение
def points_to_cost(value: int) -> str:
    if len(str(value)) == 4:
        str_value = str(value)
        result = f'{str_value[:1]}.{str_value[1:]}'
        return result
    elif len(str(value)) == 5:
        str_value = str(value)
        result = f'{str_value[:2]}.{str_value[2:]}'
        return result
    elif len(str(value)) == 6:
        str_value = str(value)
        result = f'{str_value[:3]}.{str_value[3:]}'
        return result
    elif len(str(value)) == 7:
        str_value = str(value)
        result = f'{str_value[:1]}.{str_value[1:4]}.{str_value[4:]}'
        return result
    elif len(str(value)) == 8:
        str_value = str(value)
        result = f'{str_value[:2]}.{str_value[2:5]}.{str_value[5:]}'
        return result
    elif len(str(value)) == 9:
        str_value = str(value)
        result = f'{str_value[:3]}.{str_value[3:6]}.{str_value[6:]}'
        return result
    elif len(str(value)) == 10:
        str_value = str(value)
        result = f'{str_value[:1]}.{str_value[1:4]}.{str_value[4:7]}.{str_value[7:]}'
        return result
    

# Простая функция, возвращает смайлик по марке машины
def emoji_from_mark(mark: str) -> str:
    if mark == 'audi':
        return '➰'
    elif mark == 'bmw':
        return '🌍'
    elif mark == 'mercedes':
        return '🧭'
    elif mark == 'multi':
        return '🌐'
    elif mark == 'lada':
        return '🛸'
    elif mark == 'japan':
        return '🎌'
    elif mark == 'elite':
        return '👑'
    elif mark == 'moto':
        return '🛵'
    elif mark == 'helicopter':
        return '🚁'
    elif mark == 'exclusive':
        return '💎'
    

# Простая функция, возвращает стоимость рыбы по ключу
def get_fish_price(fish: str) -> int:
    fish_dictionary = {
        "plotva": 9400,
        "krasnoperka": 7950,
        "ukleyka": 7900,
        "peskar": 7950,
        "karas": 7950,
        "lesh": 7960,
        "zherekh": 8450,
        "gustera": 12000,
        "golavl": 12000,
        "sazan": 11870,
        "forel": 11900,
        "losos": 12300,
        "tunec": 15760,
        "scat": 19100,
        "beluga": 19100,
        "littleshark": 19500
    }
    return fish_dictionary[f'{fish}']


# Простая функция, возвращает значение статуса раздела по bool
def point_to_status(point: int) -> str:
    if point == 1:
        return 'включено ✅'
    else:
        return 'выключено ❌'
    

# Функция для сохранения фотографии в папку пользователя
async def handle_docs_photo(message) -> str:
    file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    src = f'users/{message.chat.id}/' + file_info.file_path.replace('photos/', '')
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    return file_info.file_path.replace('photos/', '')


# Функция для удаления предыдущего в чате сообщения
async def delete_previous_message(message) -> None:
    counter = 0
    message_id = message.message_id - 1
    while counter <= 50:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
        except Exception:
            counter += 1
            message_id -= 1
            continue
        else:
            break


def text_from_chapter(chapter: str) -> str:
    match chapter:
        case 'transport':
            return '🚗 Транспорт'
        case 'numbers':
            return '🎱 Номера'
        case 'homes':
            return '🏠 Дома'
        case 'businesses':
            return '🏦 Бизнесы'
        case 'clothes':
            return '🥋 Одежда'
        case 'weapon':
            return '🔫 Оружие'
        case 'loot':
            return '📦 Лут-предметы'
        case 'general':
            return '📊 Торговая общий'
        case 'services':
            return '💵 Услуги'