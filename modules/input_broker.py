from telebot import types
from telebot.async_telebot import AsyncTeleBot
import config
from modules import subsidiary_functions, start, discord
from database import functions as database_functions
from modules.discord_callback import chapter, notifications

bot = AsyncTeleBot(config.token)

async def return_function(message, chapter_name):
    subsidiary_functions.delete_previous_message(message=message)
    match chapter_name:
        case 'token':
            await discord.edit(message=message)
        case 'flags':
            await notifications.notifications(message=message)
        case _:
            await chapter.edit(message=message, chapter=chapter_name)

async def editing_token_or_flags(message, chapter, new_value):
    database_functions.update_state_pointers_to_null(message)
    table_name = 'user_data'
    match chapter:
        case 'token':
            column_name = 'discord_token'
            updated_value = new_value
        case 'flags':
            column_name = 'flags'
            old_value = database_functions.get_value_from_column_and_table_by_userid(column=column_name, table=table_name,
                                                                                     user_id=message.chat.id)
            if old_value is None:
                updated_value = new_value
            else:
                updated_value = old_value + '|' + new_value
            
    database_functions.update_column_in_table_by_userid(data=updated_value, column=column_name, 
                                                        table=table_name, user_id=message.chat.id)
    await subsidiary_functions.delete_previous_message(message=message.message_id + 1)
    await return_function(message=message, chapter=chapter)
    

async def editing_text(message, chapter, new_text):
    database_functions.update_state_pointers_to_null(message)
    database_functions.update_column_in_table_by_userid(data=new_text, column='text', 
                                                        table=f'users_{chapter}', user_id=message.chat.id)
    await subsidiary_functions.delete_previous_message(message=message.message_id + 1)
    await return_function(message=message, chapter=chapter)


async def editing_photo(message, chapter, filename):
    database_functions.update_state_pointers_to_null(message)
    old_value = database_functions.get_value_from_column_and_table_by_userid(column='images', table=f'users_{chapter}',
                                                                             user_id=message.chat.id)
    if old_value is None:
        updated_value = filename
    else:
        updated_value = old_value + '|' + filename
    database_functions.update_column_in_table_by_userid(data=updated_value, column='images', 
                                                        table=f'users_{chapter}', user_id=message.chat.id)
    
    await subsidiary_functions.delete_previous_message(message=message.message_id + 1)
    await return_function(message=message, chapter=chapter)
    

async def edit_photo(message):
    pointer = database_functions.check_user(message)
    if pointer == 0:
        database_functions.create_new_user(message)
        await start.send(message)
    else:
        state_pointers = database_functions.get_state_pointers_by_userid(message)
        filename = await subsidiary_functions.handle_docs_photo(message)
        if state_pointers[12] == 1:
            await editing_photo(message=message, chapter='transport', filename=filename)
        elif state_pointers[13] == 1:
            await editing_photo(message=message, chapter='numbers', filename=filename)
        elif state_pointers[14] == 1:
            await editing_photo(message=message, chapter='homes', filename=filename)
        elif state_pointers[15] == 1:
            await editing_photo(message=message, chapter='businesses', filename=filename)
        elif state_pointers[16] == 1:
            await editing_photo(message=message, chapter='clothes', filename=filename)
        elif state_pointers[17] == 1:
            await editing_photo(message=message, chapter='weapon', filename=filename)
        elif state_pointers[18] == 1:
            await editing_photo(message=message, chapter='loot', filename=filename)
        elif state_pointers[19] == 1:
            await editing_photo(message=message, chapter='general', filename=filename)
        elif state_pointers[20] == 1:
            await editing_photo(message=message, chapter='services', filename=filename)
        else:
            await start.send(message)


async def edit_text(message):
    pointer = database_functions.check_user(message)
    if pointer == 0:
        database_functions.create_new_user(message)
        await start.send(message)
    else:
        state_pointers = database_functions.get_state_pointers_by_userid(message)
        filename = await subsidiary_functions.handle_docs_photo(message)
        if state_pointers[1] == 1:
            await editing_token_or_flags(message=message, chapter='token', new_text=message.text)
        elif state_pointers[2] == 1:
            await editing_token_or_flags(message=message, chapter='flags', new_text=message.text)
        elif state_pointers[3] == 1:
            await editing_text(message=message, chapter='transport', new_text=message.text)
        elif state_pointers[4] == 1:
            await editing_text(message=message, chapter='numbers', new_text=message.text)
        elif state_pointers[5] == 1:
            await editing_text(message=message, chapter='homes', new_text=message.text)
        elif state_pointers[6] == 1:
            await editing_text(message=message, chapter='businesses', new_text=message.text)
        elif state_pointers[7] == 1:
            await editing_text(message=message, chapter='clothes', new_text=message.text)
        elif state_pointers[8] == 1:
            await editing_text(message=message, chapter='weapon', new_text=message.text)
        elif state_pointers[9] == 1:
            await editing_text(message=message, chapter='loot', new_text=message.text)
        elif state_pointers[10] == 1:
            await editing_text(message=message, chapter='general', new_text=message.text)
        elif state_pointers[11] == 1:
            await editing_text(message=message, chapter='services', new_text=message.text)
