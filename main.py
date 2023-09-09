import asyncio
from telebot.async_telebot import AsyncTeleBot
import config
from database import functions as database_functions
from modules import input_broker as broker
from modules import start, cars, fishing, discord
from modules.cars_callback import car_list, detail_car
from modules.fishing_callback import fishes
from modules.discord_callback import myads, chapter, timer, myads_functions, notifications

bot = AsyncTeleBot(config.token)
db_path = config.db_path

# Отработка команд start и main
@bot.message_handler(commands=['start', 'main'])
async def start(message):
    await start.send(message=message)

# Отработка команды cars
@bot.message_handler(commands=['cars'])
async def cars(message):
    await cars.send(message=message)

# Отработка команды fishing
@bot.message_handler(commands=['fishing'])
async def fishing(message):
    await fishing.send(message=message)

# Отработка команды discord
@bot.message_handler(commands=['discord'])
async def discord(message):
    await discord.send(message=message)


# Отработка всех сообщений с типом контента photo, сюда включается прикрепление фотографий к разделу
@bot.message_handler(content_types=['photo'])
async def input_photo(message):
   await broker.edit_photo(message=message)


# Отработка всех сообщений с типом контента text, сюда ключается изменение текста раздела
@bot.message_handler(content_types=['text'])
async def input_text(message):
    await broker.edit_text(message=message)


# Отработка всех кнопок
@bot.callback_query_handler(func=lambda call: True)
async def callback(call):

    calling_data = call.data.split('|')

    match calling_data[0]:

        # Главное меню
        case 'main':
            await start.edit(message=call.message)

        # Разметка под раздел автомобилей
        case 'cars':
            await cars.edit(message=call.message)

        # Разметка под раздел рыбалки
        case 'fishing':
            await fishing.edit(message=call.message)

        # разметка под раздел дискорда
        case 'discord':
            await discord.edit(message=call.message)

        # Разметка под раздел определенной марки
        case 'car_list':
            await car_list.edit(message=call.message, car_mark=calling_data[1], page_id=int(calling_data[2]))

        # Разметка под карточку конкретной машины
        case 'detail_car':
            await detail_car.edit(message=call.message, car_mark=calling_data[1], car_id=int(calling_data[2]))

        # Разметка под раздел определенной глубины
        case 'fishes':
            await fishes.edit(message=call.message, deepth=int(calling_data[1]))

        # Отправка разметки с разделами обьявлений и их статусами
        case 'myads':
            await myads.edit(message=call.message)

        # Отправка разметки для определенного раздела
        case 'chapter':
            await chapter.edit(message=call.message, chapter=calling_data[1])

        # Обработка колбека на включение или отключение обьявления и вызов соответствующей асинхронной функции
        case 'onoff':
            await myads_functions.onoff(message=call.message, chapter_name=calling_data[1])
        
        # Отправка сообщения и изменение поинтера в бд для ориентирования на вызов определенной функции для
        # редактирования текста
        case 'edit_text':
            await myads_functions.edit_text(message=call.message, chapter=calling_data[1])

        # Отправка сообщения и изменение поинтера в бд для ориентирования на вызов определенной функции для
        # редактирования фото
        case 'edit_photo':
            await myads_functions.edit_photo(message=call.message, chapter=calling_data[1])

        # Очистка закрепленных за разделом фотографий
        case 'delete_photo':
            await myads_functions.delete_photo(message=call.message, chapter=calling_data[1])

        # Отправка всех фотографий закрепленных за разделом у конкретного пользователя
        case 'show_all_photo':
            await myads_functions.show_all_photo(message=call.message, chapter=calling_data[1])

        # Отправка разметки под изменение таймера
        case 'change_timer':
            await timer.change_timer(message=call.message)

        # Изменение таймер для пользователя и запись результата в бд
        case 'changing_timer':
            await timer.changing_timer(message=call.message)

        # Открытие раздела уведомлений по кнопке
        case 'notifications':
            await notifications.notifications(message=call.message)
        
        # Добавление нового флага для уведомлений
        case 'add_flag':
            await notifications.add_flag(message=call.message)
        
        # Удаление всех флагов для уведомлений
        case 'delete_flags':
            await notifications.delete_flags(message=call.message)

        # Изменение auth-токена
        case 'change_token':
            token = database_functions.get_value_from_column_and_table_by_userid(
                column='discord_token', table='user_data', user_id=call.message.chat.id
            )
            database_functions.update_column_in_table_by_userid(
                data=1, column='input_token', table='state_pointers', user_id=call.message.chat.id)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'🔑 Введите ваш discord_auth_token (Текущий токен:{token}): ')
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                            message_id=call.message.message_id, reply_markup=None)


# Основная корутина с двумя вложенными - одна на ботполлинг, другая на автоотключение обьявлений
async def main():
    # task1 = asyncio.create_task(auto_off())
    task2 = asyncio.create_task(bot.polling(none_stop=True, timeout=0))
    # await task1
    await task2


# Запуск основной корутины
asyncio.run(main())
