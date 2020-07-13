from bot import bot
from messages import *
import config
from db import dolg_col, music_col, user_access
from threading import Timer
import functions

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, config.rep)
	
	
@bot.message_handler(commands=['me', 'я'])
def me(message):
    user = ' '
    for name, value in config.user_id.items():
        if str(message.from_user.id) == value:
            user = config.user_name[name]
    lst = ' '
    for dolg in dolg_col.find():
        if dolg['user1'] == user[0] or dolg['user2'] == user[0]:
            lst += dolg['user1'] + ' ' + dolg['user2'] + ' ' + dolg['dolg'] + '\n'
    if lst != ' ':
        bot.send_message(message.chat.id, lst)
    else:
        bot.send_message(message.chat.id, 'empty')


@bot.message_handler(commands=['all', 'всі', 'все'])
def all_list(message):
    lst = ' '
    for dolg in dolg_col.find():
        lst += dolg['user1'] + ' ' + dolg['user2'] + ' ' + str(dolg['dolg']) + '\n'
    if lst != ' ':
        bot.send_message(message.chat.id, lst)
    else:
        bot.send_message(message.chat.id, 'empty')


@bot.message_handler(commands=['dolg', 'долг'])
def dolg(message):
    mes = message.text[6:]
    mes = mes.lower()
    rep = mes.split()
    if len(rep) < 3:
        bot.reply_to(message, "Wrong input")
    else:
        user_id = find_id(rep[0])
        user1 = find_name(rep[0])
        user2 = find_name(rep[1])
        if (str(message.from_user.id) == config.user_id['misha']) or (
                str(message.from_user.id) == user_id and (user1 != user2) and user1 != ' ' and user2 != ' '):
            result = str(int(functions.eval_(rep[2])))
            if result == None:
                result = rep[2]
            data = {'user1': user1, 'user2': user2, 'dolg': result}
            dolg_col.insert_one(data)
            bot.reply_to(message, "Done")
        else:
            bot.send_message(message.chat.id, "Not allowed")


@bot.message_handler(commands=['delete', 'удалить'])
def delete(message):
    mes = message.text[8:]
    mes = mes.lower()
    rep = mes.split()
    if len(rep) < 3:
        bot.reply_to(message, "Wrong input")
    else:
        user_id = find_id(rep[1])
        user1 = find_name(rep[0])
        user2 = find_name(rep[1])
        if str(message.from_user.id) == config.user_id['misha'] or str(message.from_user.id) == user_id:
            if dolg_col.find_one_and_delete({'user1': user1, 'user2': user2, 'dolg': rep[2]}):
                bot.reply_to(message, "Done")
            else:
                bot.reply_to(message, "Wrong string")
        else:
            bot.send_message(message.chat.id, "Not allowed")

@bot.message_handler(commands=['add_music'])
def add_music(message):
    user_access.update_one({'user_id': message.from_user.id}, {"$set": {'access': 1}}, upsert=True)
    t = Timer(90, deny, [message.from_user.id]) #call deny func, user.id is param
    t.start()
    bot.send_message(message.chat.id, "Send me some music")

@bot.message_handler(commands=['get_music'])
def get_music(message):
    for music in music_col.find():
        bot.send_message(message.chat.id, music['music_id'])

@bot.message_handler(content_types=['audio'])
def add_music_in_db(message):
    for user in user_access.find():
        if user['user_id'] == message.from_user.id and user['access'] == 1:
            music_col.update_one({'music_id': message.audio.file_id},
                             {"$set": {'title': message.audio.performer + ' - ' + message.audio.title}}, upsert=True)


@bot.message_handler(func=lambda message: True)  # content_types=["text"]
def repeat_all_messages(message):
    bot.send_message(message.chat.id, "Not understandable")


def find_id(name_str):
    for name, arr in config.user_name.items():
        if name_str in arr:
            return config.user_id[name]
    return ' '


def find_name(name_str):
    for name in config.user_name.values():
        if name_str in name:
            return name[0]
    return ' '


def deny(arg):
    user_access.update_one({'user_id': arg}, {"$set": {'access': 0}})


if __name__ == '__main__':
    bot.polling(none_stop=True)
