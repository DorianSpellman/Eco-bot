from numpy import mat
import telebot
import config
from telebot import types

import mysql.connector
from mysql.connector import connect

db = mysql.connector.connect(
  host="localhost",
  user="milleo",
  password="leokelman06",
  database="greencloud"
)
cursor = db.cursor()

bot = telebot.TeleBot(config.token)

que = 'Что такое код и идентификатор?'
enter_code = 'Ввести ♻'

@bot.message_handler(commands=['start'])
def start(message):
    start_kb = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    btn1 = types.KeyboardButton(text = 'Ввести ♻')
    btn2 = types.KeyboardButton(text = 'Что такое код и идентификатор?')
    start_kb.add(btn1, btn2)
    bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAEEe4piWq0mnFJg__lBAAEnUeBISFMmMJsAAsARAAKm8XEeBsDSD0wNlZ8jBA')
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Чтобы узнать, можно ли переработать материал, просто введи его <b>код</b> или <b>идентификатор</b>', parse_mode='html', reply_markup = start_kb)

@bot.message_handler(func = lambda m: m.text == que)
def ans(message):
    ans_kb = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    enter_btn = types.KeyboardButton(text = 'Ввести ♻')
    ans_kb.add(enter_btn)

    with open('eco.jpg', 'rb') as eco:
        bot.send_photo(message.chat.id, eco)
        bot.send_message(message.chat.id, 'А теперь попробуй ввести код  🌱', reply_markup = ans_kb)

@bot.message_handler(func = lambda m: m.text == enter_code)
def intro(message):
    msg = bot.send_message(message.chat.id, 'Лучше введи цифру, но при её отсутствии попробуем разобраться и с буквами..!')
    bot.register_next_step_handler(msg, find_code)

def find_code(message):

    try:
        user_input = message.text
        user_input = user_input.lower()

        if user_input.isnumeric():

            cursor.execute(f"SELECT mat_name FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = {user_input} OR ident_mat.name_identmat = '{user_input}' LIMIT 1")
            mat_name = str(cursor.fetchall())
            mat_name = mat_name[3:-4:]
            
            cursor.execute(f"SELECT mat_using FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = {user_input} OR ident_mat.name_identmat = '{user_input}' LIMIT 1")
            mat_using = str(cursor.fetchall())
            mat_using = mat_using[3:-4:]

            cursor.execute(f"SELECT notice FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = {user_input} OR ident_mat.name_identmat = '{user_input}' LIMIT 1")
            notice = str(cursor.fetchone())
            notice = notice[2:-3:]

            cursor.execute(f"SELECT preparation FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = {user_input} OR ident_mat.name_identmat = '{user_input}' LIMIT 1")
            preparation = str(cursor.fetchone())
            preparation = preparation[2:-3:]
            preparation = preparation.replace('on', '')

        else:
            
            cursor.execute(f"SELECT mat_name FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '{user_input}' LIMIT 1")
            mat_name = str(cursor.fetchall())
            mat_name = mat_name[3:-4:]

            cursor.execute(f"SELECT mat_using FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '{user_input}' LIMIT 1")
            mat_using = str(cursor.fetchall())
            mat_using = mat_using[3:-4:]

            cursor.execute(f"SELECT notice FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '{user_input}' LIMIT 1")
            notice = str(cursor.fetchone())
            notice = notice[2:-3:]

            cursor.execute(f"SELECT preparation FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '{user_input}' LIMIT 1")
            preparation = str(cursor.fetchone())
            preparation = preparation[2:-3:]
            preparation = preparation.replace('on', '')
            

        keyb = types.InlineKeyboardMarkup()
        recycle_buttton = types.InlineKeyboardButton(text = 'Узнать, где можно переработать 🌍', url = 'https://recyclemap.ru')
        keyb.add(recycle_buttton)

        bot.send_message(message.chat.id, 
                                        f'<b>{mat_name}</b>'
                                        f'\n\n{mat_using}'
                                        f'\n\n{notice}'
                                        f'\n\n<i>{preparation}</i>', 
                                        parse_mode='html', reply_markup = keyb)

    except:
        bot.send_message(message.chat.id, 'Увы, я ещё не знаю такой материал :C', reply_markup = types.ReplyKeyboardRemove())
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAEEfz9iXDuRf6v2-BiH8zB8XY2cDMdIlAACWRIAAqbxcR5xRKqTi3F9aSQE')
        
@bot.message_handler(func = lambda m: True)
def another(message):
    bot.send_message(message.chat.id, 'Нажмите /start, чтобы начать, или ' + enter_code + ' , чтобы продолжить!')

bot.polling(none_stop=True, interval=0)