from multiprocessing import Value
import config
import sqlite3
import datetime
import os

database_path = config.db_path
src_path = config.src_path

def get_all_users():
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute(f'SELECT * FROM user_data;')
    users = cursor.fetchall()
    database.close()
    return users


def get_state_pointers_by_userid(message):
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM state_pointers;")
    state_pointers = cursor.fetchall()
    for i in range(len(state_pointers)):
        if state_pointers[i][0] == message.chat.id:
            user_state_pointers = state_pointers[i]
    return user_state_pointers


def check_user(message): 
    users = get_all_users()
    pointer = False
    for i in range(len(users)):
        if users[i][0] == message.chat.id:
            pointer = True
    return pointer


def create_new_user(message):

    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute("INSERT INTO user_data VALUES(?,?,?,?,?,?);", 
                   (message.chat.id, None, 180, datetime.datetime.now(), None, None))
    cursor.execute("INSERT INTO users_transport VALUES(?,?,?,?);", (message.chat.id, 0, None, None))
    cursor.execute("INSERT INTO users_numbers VALUES(?,?,?,?);", (message.chat.id, 0, None, None))
    cursor.execute("INSERT INTO users_homes VALUES(?,?,?,?);", (message.chat.id, 0, None, None))
    cursor.execute("INSERT INTO users_businesses VALUES(?,?,?,?);", (message.chat.id, 0, None, None))
    cursor.execute("INSERT INTO users_clothes VALUES(?,?,?,?);", (message.chat.id, 0, None, None))
    cursor.execute("INSERT INTO users_weapon VALUES(?,?,?,?);", (message.chat.id, 0, None, None))
    cursor.execute("INSERT INTO users_loot VALUES(?,?,?,?);", (message.chat.id, 0, None, None))
    cursor.execute("INSERT INTO users_general VALUES(?,?,?,?);", (message.chat.id, 0, None, None))
    cursor.execute("INSERT INTO users_services VALUES(?,?,?,?);", (message.chat.id, 0, None, None))
    cursor.execute("INSERT INTO state_pointers VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                   (message.chat.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    database.commit()

    os.mkdir(f'{src_path}/users/{message.chat.id}')

    database.close()


def update_column_in_table_by_userid(data, column, table, user_id):
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute(f'UPDATE {table} SET {column} = "{data}" WHERE user_id = {user_id}')
    database.commit()
    database.close()


def get_value_from_column_and_table_by_userid(column, table, user_id):
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute(f'SELECT {column} FROM {table} WHERE user_id = {user_id}')
    value = cursor.fetchall()
    return value

def update_state_pointers_to_null(message):
    database = sqlite3.connect(database_path)
    cursor = database.cursor()

    cursor.execute(f'UPDATE state_pointers SET change_token = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_flags = 0 WHERE user_id = {message.chat.id}')

    cursor.execute(f'UPDATE state_pointers SET change_text_transport = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_text_number = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_text_home = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_text_business = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_text_clothes = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_text_weapon = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_text_loot = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_text_services = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_text_general = 0 WHERE user_id = {message.chat.id}')

    cursor.execute(f'UPDATE state_pointers SET change_photo_transport = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_photo_number = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_photo_home = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_photo_business = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_photo_clothes = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_photo_weapon = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_photo_loot = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_photo_services = 0 WHERE user_id = {message.chat.id}')
    cursor.execute(f'UPDATE state_pointers SET change_photo_general = 0 WHERE user_id = {message.chat.id}')

    database.commit()
    database.close()


def get_all_cars_by_mark(car_mark):
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM {car_mark};")
    cars = cursor.fetchall()
    database.close()
    return cars


def get_car_from_table_and_carid(car_mark, car_id):
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute(f'SELECT * FROM {car_mark} WHERE id = {car_id}')
    car = cursor.fetchall()
    return car[0]


def get_user_by_id(user_id):
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute(f'SELECT * FROM user_data WHERE user_id = {user_id}')
    user = cursor.fetchall()
    return user[0]