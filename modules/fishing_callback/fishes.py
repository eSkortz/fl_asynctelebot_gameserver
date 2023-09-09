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


def make_markup(deepth):

    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton('🐟 Назад к разделу рыбалки', callback_data='fishing'))

    match deepth:
        case 0:
            caption = f'🌊 Глубина 0-5 метров\n\n' \
                        f'🐡 Хлебный мякиш + любая удочка:\n' \
                        f'   50% - Уклейка - {subsidiary_functions.get_fish_price("ukleyka")}\n' \
                        f'   50% - Пескарь - {subsidiary_functions.get_fish_price("peskar")}\n\n' \
                        f'🐠 Личинки насекомых + любая удочка:\n' \
                        f'   25% - Красноперка - {subsidiary_functions.get_fish_price("krasnoperka")}\n' \
                        f'   25% - Уклейка - {subsidiary_functions.get_fish_price("ukleyka")}\n' \
                        f'   25% - Плотва - {subsidiary_functions.get_fish_price("plotva")}\n' \
                        f'   25% - Жерех - {subsidiary_functions.get_fish_price("zherekh")}\n\n' \
                        f'🐬 Дождевые черви + любая удочка:\n' \
                        f'   50% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   50% - Карась - {subsidiary_functions.get_fish_price("karas")}\n\n' \
                        f'🐋 Личинки мотыля + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'🦈 Мальки + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'⏱ Максимальное время рыбалки - 2 минуты\n' \
                        f'🎲 Среднее время рыбалки - 1 минута 40 секунд'
        case 5:
            caption = f'🌊 Глубина 5-15 метров\n\n' \
                        f'🐡 Хлебный мякиш + любая удочка:\n' \
                        f'   50% - Пескарь - {subsidiary_functions.get_fish_price("peskar")}\n' \
                        f'   25% - Уклейка - {subsidiary_functions.get_fish_price("ukleyka")}\n' \
                        f'   25% - Густера - {subsidiary_functions.get_fish_price("gustera")}\n\n' \
                        f'🐠 Личинки насекомых + любая удочка:\n' \
                        f'   25% - Красноперка - {subsidiary_functions.get_fish_price("krasnoperka")}\n' \
                        f'   25% - Уклейка - {subsidiary_functions.get_fish_price("ukleyka")}\n' \
                        f'   25% - Плотва - {subsidiary_functions.get_fish_price("plotva")}\n' \
                        f'   25% - Жерех - {subsidiary_functions.get_fish_price("zherekh")}\n\n' \
                        f'🐬 Дождевые черви + любая удочка:\n' \
                        f'   50% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🐋 Личинки мотыля + первая удочка:\n' \
                        f'   50% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🐋 Личинки мотыля + вторая/третья удочка:\n' \
                        f'   50% - Форель - {subsidiary_functions.get_fish_price("forel")}\n' \
                        f'   25% - Лосось - {subsidiary_functions.get_fish_price("losos")}\n' \
                        f'   25% - Тунец - {subsidiary_functions.get_fish_price("tunec")}\n\n' \
                        f'🦈 Мальки + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'⏱ Максимальное время рыбалки - 4 минуты\n' \
                        f'🎲 Среднее время рыбалки - 2 минуты 48 секунд'
        case 15:
            caption = f'🌊 Глубина 15-25 метров\n\n' \
                        f'🐡 Хлебный мякиш + любая удочка:\n' \
                        f'   25% - Красноперка - {subsidiary_functions.get_fish_price("krasnoperka")}\n' \
                        f'   25% - Пескарь - {subsidiary_functions.get_fish_price("peskar")}\n' \
                        f'   25% - Уклейка - {subsidiary_functions.get_fish_price("ukleyka")}\n' \
                        f'   25% - Жерех - {subsidiary_functions.get_fish_price("zherekh")}\n\n' \
                        f'🐠 Личинки насекомых + любая удочка:\n' \
                        f'   25% - Красноперка - {subsidiary_functions.get_fish_price("krasnoperka")}\n' \
                        f'   25% - Пескарь - {subsidiary_functions.get_fish_price("peskar")}\n' \
                        f'   25% - Плотва - {subsidiary_functions.get_fish_price("plotva")}\n' \
                        f'   25% - Густера - {subsidiary_functions.get_fish_price("gustera")}\n\n' \
                        f'🐬 Дождевые черви + любая удочка:\n' \
                        f'   25% - Сазан - {subsidiary_functions.get_fish_price("sazan")}\n' \
                        f'   25% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🐋 Личинки мотыля + первая удочка:\n' \
                        f'   25% - Сазан - {subsidiary_functions.get_fish_price("sazan")}\n' \
                        f'   25% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🐋 Личинки мотыля + вторая/третья удочка:\n' \
                        f'   25% - Форель - {subsidiary_functions.get_fish_price("forel")}\n' \
                        f'   25% - Лосось - {subsidiary_functions.get_fish_price("losos")}\n' \
                        f'   25% - Тунец - {subsidiary_functions.get_fish_price("tunec")}\n' \
                        f'   25% - Скат - {subsidiary_functions.get_fish_price("scat")}\n\n' \
                        f'🦈 Мальки + любая удочка:\n' \
                        f'   50% - Тунец - {subsidiary_functions.get_fish_price("tunec")}\n' \
                        f'   50% - Скат - {subsidiary_functions.get_fish_price("scat")}\n\n' \
                        f'⏱ Максимальное время рыбалки - 5 минут\n' \
                        f'🎲 Среднее время рыбалки - 3 минуты 19 секунд'
        case 25:
            caption = f'🌊 Глубина 25-45 метров\n\n' \
                        f'🐡 Хлебный мякиш + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'🐠 Личинки насекомых + любая удочка:\n' \
                        f'   25% - Красноперка - {subsidiary_functions.get_fish_price("krasnoperka")}\n' \
                        f'   25% - Жерех - {subsidiary_functions.get_fish_price("zherekh")}\n' \
                        f'   25% - Плотва - {subsidiary_functions.get_fish_price("plotva")}\n' \
                        f'   25% - Густера - {subsidiary_functions.get_fish_price("gustera")}\n\n' \
                        f'🐬 Дождевые черви + любая удочка:\n' \
                        f'   25% - Сазан - {subsidiary_functions.get_fish_price("sazan")}\n' \
                        f'   25% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🐋 Личинки мотыля + первая удочка:\n' \
                        f'   25% - Сазан - {subsidiary_functions.get_fish_price("sazan")}\n' \
                        f'   25% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🐋 Личинки мотыля + вторая/третья удочка:\n' \
                        f'   25% - Форель - {subsidiary_functions.get_fish_price("forel")}\n' \
                        f'   25% - Лосось - {subsidiary_functions.get_fish_price("losos")}\n' \
                        f'   25% - Тунец - {subsidiary_functions.get_fish_price("tunec")}\n' \
                        f'   25% - Скат - {subsidiary_functions.get_fish_price("scat")}\n\n' \
                        f'🦈 Мальки + первая удочка:\n' \
                        f'   25% - Сазан - {subsidiary_functions.get_fish_price("sazan")}\n' \
                        f'   25% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🦈 Мальки + вторая/третья удочка:\n' \
                        f'   25% - Тунец - {subsidiary_functions.get_fish_price("tunec")}\n' \
                        f'   25% - Скат - {subsidiary_functions.get_fish_price("scat")}\n' \
                        f'   25% - Белуга - {subsidiary_functions.get_fish_price("beluga")}\n' \
                        f'   25% - Мини-акула - {subsidiary_functions.get_fish_price("littleshark")}\n\n' \
                        f'⏱ Максимальное время рыбалки - 6 минут\n' \
                        f'🎲 Среднее время рыбалки - 3 минуты 36 секунд'
        case 45:
            caption = f'🌊 Глубина 45-65 метров\n\n' \
                        f'🐡 Хлебный мякиш + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'🐠 Личинки насекомых + любая удочка:\n' \
                        f'   25% - Красноперка - {subsidiary_functions.get_fish_price("krasnoperka")}\n' \
                        f'   25% - Жерех - {subsidiary_functions.get_fish_price("zherekh")}\n' \
                        f'   25% - Плотва - {subsidiary_functions.get_fish_price("plotva")}\n' \
                        f'   25% - Густера - {subsidiary_functions.get_fish_price("gustera")}\n\n' \
                        f'🐬 Дождевые черви + любая удочка:\n' \
                        f'   25% - Сазан - {subsidiary_functions.get_fish_price("sazan")}\n' \
                        f'   25% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🐋 Личинки мотыля + первая удочка:\n' \
                        f'   25% - Сазан - {subsidiary_functions.get_fish_price("sazan")}\n' \
                        f'   25% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🐋 Личинки мотыля + вторая/третья удочка:\n' \
                        f'   25% - Форель - {subsidiary_functions.get_fish_price("forel")}\n' \
                        f'   25% - Лосось - {subsidiary_functions.get_fish_price("losos")}\n' \
                        f'   25% - Тунец - {subsidiary_functions.get_fish_price("tunec")}\n' \
                        f'   25% - Скат - {subsidiary_functions.get_fish_price("scat")}\n\n' \
                        f'🦈 Мальки + первая удочка:\n' \
                        f'   25% - Сазан - {subsidiary_functions.get_fish_price("sazan")}\n' \
                        f'   25% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🦈 Мальки + вторая/третья удочка:\n' \
                        f'   25% - Тунец - {subsidiary_functions.get_fish_price("tunec")}\n' \
                        f'   25% - Скат - {subsidiary_functions.get_fish_price("scat")}\n' \
                        f'   25% - Белуга - {subsidiary_functions.get_fish_price("beluga")}\n' \
                        f'   25% - Мини-акула - {subsidiary_functions.get_fish_price("littleshark")}\n\n' \
                        f'⏱ Максимальное время рыбалки - 6 минут\n' \
                        f'🎲 Среднее время рыбалки - 4 минуты 8 секунд'
        case 65:
            caption = f'🌊 Глубина 65-85 метров\n\n' \
                        f'🐡 Хлебный мякиш + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'🐠 Личинки насекомых + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'🐬 Дождевые черви + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'🐋 Личинки мотыля + первая удочка:\n' \
                        f'   25% - Сазан - {subsidiary_functions.get_fish_price("sazan")}\n' \
                        f'   25% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🐋 Личинки мотыля + вторая/третья удочка:\n' \
                        f'   25% - Форель - {subsidiary_functions.get_fish_price("forel")}\n' \
                        f'   25% - Лосось - {subsidiary_functions.get_fish_price("losos")}\n' \
                        f'   25% - Тунец - {subsidiary_functions.get_fish_price("tunec")}\n' \
                        f'   25% - Скат - {subsidiary_functions.get_fish_price("scat")}\n\n' \
                        f'🦈 Мальки + первая удочка:\n' \
                        f'   25% - Сазан - {subsidiary_functions.get_fish_price("sazan")}\n' \
                        f'   25% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🦈 Мальки + вторая/третья удочка:\n' \
                        f'   25% - Тунец - {subsidiary_functions.get_fish_price("tunec")}\n' \
                        f'   25% - Скат - {subsidiary_functions.get_fish_price("scat")}\n' \
                        f'   25% - Белуга - {subsidiary_functions.get_fish_price("beluga")}\n' \
                        f'   25% - Мини-акула - {subsidiary_functions.get_fish_price("littleshark")}\n\n' \
                        f'⏱ Максимальное время рыбалки - 6 минут\n' \
                        f'🎲 Среднее время рыбалки - 4 минуты 20 секунд' 
        case 85:
            caption = f'🌊 Глубина 65-85 метров\n\n' \
                        f'🐡 Хлебный мякиш + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'🐠 Личинки насекомых + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'🐬 Дождевые черви + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'🐋 Личинки мотыля + любая удочка:\n' \
                        f'   На данной глубине ничего не ловится\n\n' \
                        f'🦈 Мальки + первая удочка:\n' \
                        f'   25% - Сазан - {subsidiary_functions.get_fish_price("sazan")}\n' \
                        f'   25% - Карась - {subsidiary_functions.get_fish_price("karas")}\n' \
                        f'   25% - Лещ - {subsidiary_functions.get_fish_price("lesh")}\n' \
                        f'   25% - Голавль - {subsidiary_functions.get_fish_price("golavl")}\n\n' \
                        f'🦈 Мальки + вторая/третья удочка:\n' \
                        f'   25% - Тунец - {subsidiary_functions.get_fish_price("tunec")}\n' \
                        f'   25% - Скат - {subsidiary_functions.get_fish_price("scat")}\n' \
                        f'   25% - Белуга - {subsidiary_functions.get_fish_price("beluga")}\n' \
                        f'   25% - Мини-акула - {subsidiary_functions.get_fish_price("littleshark")}\n\n' \
                        f'⏱ Максимальное время рыбалки - 6 минут\n' \
                        f'🎲 Среднее время рыбалки - 4 минуты 30 секунд'

    return markup_inline, caption

async def edit(message, deepth):

    markup_inline, caption = make_markup(deepth=deepth)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=caption)
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup_inline)
    await bot.edit_message_media(chat_id=message.chat.id, media=None)