import telebot
import config
from telebot import types
import mysql.connector

bot = telebot.TeleBot(config.token)

lst_ids, lst_names, lst_usernames = [], [], []

# database_tables = {'Материал':'material',
#                 'Тип материала':'type',
#                 'Код переработки':'code',
#                 'ID кода':'ident_mat',
#                 'Способ утилизации':'point'
#                  }

# database_attributes = {'material':'',
#                 'type':'',
#                 'code':['code', 'type_id', 'material_id'],
#                 'ident_mat':'',
#                 'point':''
#                  }

@bot.message_handler(commands=['start'])
def start(message):

    new_user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    
    with open('users.txt', 'r+') as users_db:

        file = users_db.readlines()
        
        for line in file: 
            ids, names, usernames = line.split(' | ')
            lst_ids.append(ids)
            lst_names.append(names)
            lst_usernames.append(usernames)

        if str(new_user_id) not in lst_ids: 
            users_db.write(f'{new_user_id} | {name} | @{username}' + '\n')
            lst_ids.append(new_user_id)
            lst_names.append(name)
            lst_usernames.append(username)

    print(lst_ids)
    print(lst_names)
    print(lst_usernames)
    print('------------')

    if message.chat.id == 580190223:
        admin_start_kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        #adm_btn_1 = types.KeyboardButton(text = 'Добавить данные')
        #adm_btn_2 = types.KeyboardButton(text = 'Обновить данные')
        #adm_btn_3 = types.KeyboardButton(text = 'Удалить данные')
        btn_count = types.KeyboardButton(text = 'Статистика')
        btn_base = types.KeyboardButton(text = 'Ввести ♻')
        #admin_start_kb.add(adm_btn_1, adm_btn_2)
        admin_start_kb.add(btn_count, btn_base)
        
        bot.send_message(message.chat.id, f'Привет, создатель {message.from_user.first_name}!', reply_markup = admin_start_kb)

    else:
        start_kb = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
        btn1 = types.KeyboardButton(text = 'Ввести ♻')
        btn2 = types.KeyboardButton(text = 'Что такое код и идентификатор?')
        start_kb.add(btn1, btn2)
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAEEe4piWq0mnFJg__lBAAEnUeBISFMmMJsAAsARAAKm8XEeBsDSD0wNlZ8jBA')
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Чтобы узнать, можно ли переработать материал, просто введи его <b>код</b> или <b>идентификатор</b>', parse_mode='html', reply_markup = start_kb)

# @bot.message_handler(func = lambda m: m.text == 'Добавить в базу данных')
# def add(message):

#     db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="leokelman06",
#         database="greencloud"
#         )

#     cursor = db.cursor()

#     bot.send_message(message.chat.id, f'Вы перешли в особую зону. Выберите, с какой таблицей работать: ')

@bot.message_handler(func = lambda m: m.text == 'Статистика')
def count(message):
        
    admin_kb2 = types.ReplyKeyboardMarkup(resize_keyboard = True)
    #adm_btn_1 = types.KeyboardButton(text = 'Добавить данные')
    #adm_btn_2 = types.KeyboardButton(text = 'Обновить данные')
    #adm_btn_3 = types.KeyboardButton(text = 'Удалить данные')
    btn_base = types.KeyboardButton(text = 'Ввести ♻')
    #admin_kb2.add(adm_btn_1, adm_btn_2, adm_btn_3)
    admin_kb2.add(btn_base)

    bot.send_message(message.chat.id, f'Количество пользователей: {len(lst_ids)}'
                                      f'\n\n<i>Последний добавленный</i>:'
                                      f'\n<b>Name:</b> {lst_names[-1]}'
                                      f'\n<b>Username:</b> {lst_usernames[-1]}', parse_mode = 'html', reply_markup = admin_kb2)
        
                      

@bot.message_handler(func = lambda m: m.text == 'Что такое код и идентификатор?')
def ans(message):
    ans_kb = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    enter_btn = types.KeyboardButton(text = 'Ввести ♻')
    ans_kb.add(enter_btn)

    with open('eco.jpg', 'rb') as eco:
        bot.send_photo(message.chat.id, eco)
        bot.send_message(message.chat.id, 'А теперь попробуй ввести код  🌱', reply_markup = ans_kb)

@bot.message_handler(func = lambda m: m.text == 'Ввести ♻')
def intro(message):
    msg = bot.send_message(message.chat.id, 'Лучше введи цифру, но при её отсутствии попробуем разобраться и с буквами..!')
    bot.register_next_step_handler(msg, find_code)

def find_code(message):

    db = mysql.connector.connect(
        host="localhost",
        user="milleo",
        password="leokelman06",
        database="greencloud"
        )

    cursor = db.cursor()

    try:
        user_input = message.text
        user_input = user_input.lower()
        #user_input = tuple(user_input.lower())

        if user_input.isnumeric():
            
            cursor.execute(f"SELECT mat_name FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = {user_input} LIMIT 1")
            #select_mn = "SELECT mat_name FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = %s LIMIT 1"
            #cursor.execute(select_mn, user_input)
            mat_name = str(cursor.fetchall())
            mat_name = mat_name[3:-4:]
            
            cursor.execute(f"SELECT mat_using FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = {user_input} LIMIT 1")
            #select_mu = "SELECT mat_using FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = %s LIMIT 1"
            #cursor.execute(select_mu, user_input)
            mat_using = str(cursor.fetchall())
            mat_using = mat_using[3:-4:]

            cursor.execute(f"SELECT notice FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = {user_input} LIMIT 1")
            #select_n = "SELECT notice FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = %s LIMIT 1"
            #cursor.execute(select_n, user_input)
            notice = str(cursor.fetchone())
            notice = notice[2:-3:]

            cursor.execute(f"SELECT preparation FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = {user_input} LIMIT 1")
            #select_p = "SELECT preparation FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE code.code = %s LIMIT 1"
            #cursor.execute(select_p, user_input)
            preparation = str(cursor.fetchone())
            preparation = preparation[2:-3:]
            preparation = preparation.replace('on', '')

        else:
            
            cursor.execute(f"SELECT mat_name FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '{user_input}' LIMIT 1")
            #select_mn = "SELECT mat_name FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '%s' LIMIT 1"
            #cursor.execute(select_mn, user_input)
            mat_name = str(cursor.fetchall())
            mat_name = mat_name[3:-4:]

            cursor.execute(f"SELECT mat_using FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '{user_input}' LIMIT 1")
            #select_mu = "SELECT mat_using FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '%s' LIMIT 1"
            #cursor.execute(select_mu, user_input)
            mat_using = str(cursor.fetchall())
            mat_using = mat_using[3:-4:]

            cursor.execute(f"SELECT notice FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '{user_input}' LIMIT 1")
            #select_n = "SELECT notice FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '%s' LIMIT 1"
            #cursor.execute(select_n, user_input)
            notice = str(cursor.fetchone())
            notice = notice[2:-3:]

            cursor.execute(f"SELECT preparation FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '{user_input}' LIMIT 1")
            #select_p = "SELECT preparation FROM material INNER JOIN code USING(material_id) INNER JOIN ident_mat USING(code_id) WHERE ident_mat.name_identmat = '%s' LIMIT 1"
            #cursor.execute(select_p, user_input)
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
        
        bot.send_message(message.chat.id, 'Увы, я ещё не знаю такой материал :C')
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAEEfz9iXDuRf6v2-BiH8zB8XY2cDMdIlAACWRIAAqbxcR5xRKqTi3F9aSQE')
        
@bot.message_handler(func = lambda m: True)
def another(message):
    bot.send_message(message.chat.id, 'Нажмите /start, чтобы начать, или ' + 'Ввести ♻' + ' , чтобы продолжить!')

bot.polling(none_stop=True, interval=0)