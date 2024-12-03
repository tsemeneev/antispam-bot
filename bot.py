import time
import requests
from telebot import TeleBot
from telebot import StateMemoryStorage, types
from keyboards import (TelegramBot, add_admin_id, add_channel_to_list, add_main_chat_to_list, admin_kb, 
    change_follow_channels_kb, change_follow_text_kb, change_log_chat_kb, change_main_chat_kb, delete_admin_id, delete_admins_kb, 
    delete_channel_from_list, delete_channels_kb, delete_main_chat_from_list, delete_main_chat_kb, get_admin_ids, get_list_channels, get_main_chats, get_text, 
    list_channels_kb, list_main_chats_kb, menu_kb, set_text)
from utils import (check_frod, check_hidden_text, check_multifrod,
            check_spam_base, check_urls, delete_msg_from_file, get_check_follow_channels, get_log_chat_id, get_update_spam_base, load_entities_from_json_file, save_entities_to_json_file, send_follow_message, set_log_chat_id, write_msg)
import logging

logging.basicConfig(filename='bot_log.log', level=logging.INFO)


# Ссылка на спам базу: https://www.npoint.io/docs/aab91686ac4741cc778b
storage = StateMemoryStorage()
bot = TeleBot('6499941275:AAGy0nmX8iqjkQao2rK2hEva-lLPA6q5hqo', state_storage=storage)
sp_bot = TelegramBot()



def delete_msg(message: types.Message, filter_name: str) -> None:
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    send_log_message(message, filter_name)
    
def delete_msg_frod(chat_id: int, message_id: int) -> None:
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass
    

def send_log_message(message: types.Message, filter_name: str) -> None:
    log_chat_id = get_log_chat_id()
    message_text = message.text if message.text else message.caption
    text = f'<b>ID:</b> {message.from_user.id}\n'
    text += f'➖➖➖➖➖➖➖➖➖\n'
    text += f'<b>Chat ID:</b> {message.chat.id}\n'
    text += f'➖➖➖➖➖➖➖➖➖\n'
    text += f'<b>Классификация удаления:</b> {filter_name}\n\n'
    text += f'<b>Отправил пользователь:</b> @{message.from_user.username}\n'
    text += f'<b>Отправлено из чата:</b> {message.chat.title}\n'
    text += f'➖➖➖➖➖➖➖➖➖\n'
    text += f'<b>Текст сообщения:</b> {message_text}\n'
    
    bot.send_message(chat_id=log_chat_id, text=text, parse_mode='html')
    

@bot.message_handler(commands=['start'])
def start(message):
    admin_ids = get_admin_ids()
    if message.from_user.id in admin_ids:
        bot.send_message(message.chat.id, 'Привет. Я антиспам бот.\nДля управления ботом используй команду /menu')
        
        
@bot.message_handler(commands=['menu'])
def menu(message):
    admin_ids = get_admin_ids()
    if message.from_user.id in admin_ids:
        bot.send_message(message.chat.id, 'Активируйте нужные опции', reply_markup=menu_kb(sp_bot=sp_bot))
        
        

@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def menu(call):
    bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции', message_id=call.message.message_id, reply_markup=menu_kb(sp_bot=sp_bot))

@bot.message_handler(commands=['update'])
def update_spam_base(message):
    if message.from_user.id in get_admin_ids():
        res = requests.get('https://api.npoint.io/aab91686ac4741cc778b').json()
        get_update_spam_base(res['spam_base'])
        bot.reply_to(message, 'База обновлена') 
        
@bot.callback_query_handler(func=lambda call: call.data == 'spam_base')
def spam_base(call):
    if sp_bot.spam_base == True:
        sp_bot.spam_base = False
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, inline_message_id=call.inline_message_id, reply_markup=menu_kb(sp_bot=sp_bot))
    else:
        sp_bot.spam_base = True
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, reply_markup=menu_kb(sp_bot=sp_bot), inline_message_id=call.inline_message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'frod')
def frod(call):
    if sp_bot.frod == True:
        sp_bot.frod = False
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, inline_message_id=call.inline_message_id, reply_markup=menu_kb(sp_bot=sp_bot))
    else:
        sp_bot.frod = True
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, reply_markup=menu_kb(sp_bot=sp_bot), inline_message_id=call.inline_message_id)



@bot.callback_query_handler(func=lambda call: call.data == 'multifrod')
def multifrod(call):
    if sp_bot.multifrod == True:
        sp_bot.multifrod = False
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, inline_message_id=call.inline_message_id, reply_markup=menu_kb(sp_bot=sp_bot))
    else:
        sp_bot.multifrod = True
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, reply_markup=menu_kb(sp_bot=sp_bot), inline_message_id=call.inline_message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'resend')
def resend(call):
    if sp_bot.resend == True:
        sp_bot.resend = False
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, inline_message_id=call.inline_message_id, reply_markup=menu_kb(sp_bot=sp_bot))
    else:
        sp_bot.resend = True
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, reply_markup=menu_kb(sp_bot=sp_bot), inline_message_id=call.inline_message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'urls')
def urls(call):
    if sp_bot.urls == True:
        sp_bot.urls = False
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, inline_message_id=call.inline_message_id, reply_markup=menu_kb(sp_bot=sp_bot))
    else:
        sp_bot.urls = True
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, reply_markup=menu_kb(sp_bot=sp_bot), inline_message_id=call.inline_message_id)
        
@bot.callback_query_handler(func=lambda call: call.data == 'hidden_text')
def hidden_text(call):
    if sp_bot.hidden_text == True:
        sp_bot.hidden_text = False
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, inline_message_id=call.inline_message_id, reply_markup=menu_kb(sp_bot=sp_bot))
    else:
        sp_bot.hidden_text = True
        bot.edit_message_text(chat_id=call.message.chat.id, text='Активируйте нужные опции',
                              message_id=call.message.message_id, reply_markup=menu_kb(sp_bot=sp_bot), inline_message_id=call.inline_message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'text_check_count')
def text_check_count(call):
    bot.edit_message_text(chat_id=call.message.chat.id, text='Введите новое значение', message_id=call.message.message_id)
    bot.set_state(call.from_user.id, 'text_check_count', call.message.chat.id)
    
@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id, message.chat.id) == 'text_check_count', content_types=['text'])
def text_check_count(message):
    
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Это не число. Попробуйте ещё раз')
        return
    sp_bot.text_check_count = int(message.text.strip())
    bot.send_message(chat_id=message.chat.id, text='Активируйте нужные опции', reply_markup=menu_kb(sp_bot=sp_bot))
    bot.delete_state(message.from_user.id, message.chat.id)
    

@bot.callback_query_handler(func=lambda call: call.data == 'check_follow_channels')
def check_follow_channels(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите действие', reply_markup=change_follow_channels_kb())
    
@bot.callback_query_handler(func=lambda call: call.data == 'main_chat')
def change_main_chats(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите действие', reply_markup=change_main_chat_kb())

    
    
@bot.callback_query_handler(func=lambda call: call.data == 'list_main_chats')
def list_main_chats(call):
    chats_list = get_main_chats()
    bot.edit_message_text(chat_id=call.message.chat.id, text='Список чатов', message_id=call.message.message_id, reply_markup=list_main_chats_kb(chats_list))


@bot.callback_query_handler(func=lambda call: call.data == 'add_main_chat')
def add_main_chat(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          text='Введите название и юзернэйм нового чата\nНапример: Название канала, @my_chat', 
                          message_id=call.message.message_id)
    bot.set_state(call.from_user.id, 'add_chat', call.message.chat.id)
    
    
@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id, message.chat.id) == 'add_chat')
def add_chat(message):
    add_main_chat_to_list(message.text.split(','))
    bot.send_message(chat_id=message.chat.id, text='Чат добавлен')
    bot.send_message(chat_id=message.chat.id, text='Выберите действие', reply_markup=change_main_chat_kb())
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'del_main_chat')
def delete_chat(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите чат для удаления', reply_markup=delete_main_chat_kb(get_main_chats()))
    

@bot.callback_query_handler(func=lambda call: 'delete_chat' in call.data)
def delete_chat(call):
    delete_main_chat_from_list(call.data)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Чат удален', reply_markup=delete_main_chat_kb(get_main_chats()))
   
    
    
    
    
    
@bot.callback_query_handler(func=lambda call: call.data == 'list_channels')
def list_channels(call):
    channels_list = get_list_channels()
    bot.edit_message_text(chat_id=call.message.chat.id, text='Список каналов', message_id=call.message.message_id, reply_markup=list_channels_kb(channels_list))


@bot.callback_query_handler(func=lambda call: call.data == 'add_channel')
def add_channel(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          text='Введите юзернейм и id нового канала\nНапример: @my_channel, -100123456789', 
                          message_id=call.message.message_id)
    bot.set_state(call.from_user.id, 'add_channel', call.message.chat.id)
    
    
@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id, message.chat.id) == 'add_channel')
def add_channel(message):
    add_channel_to_list(message.text.split(','))
    bot.send_message(chat_id=message.chat.id, text='Канал добавлен')
    bot.send_message(chat_id=message.chat.id, text='Выберите действие', reply_markup=change_follow_channels_kb())
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'del_channel')
def delete_channel(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите канал для удаления', reply_markup=delete_channels_kb(get_list_channels()))
    

@bot.callback_query_handler(func=lambda call: 'delete_channel' in call.data)
def delete_channel(call):
    delete_channel_from_list(call.data)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Канал удален', reply_markup=delete_channels_kb(get_list_channels()))

@bot.callback_query_handler(func=lambda call: call.data == 'admin_ids')
def admin_ids(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          text='Введите выберите действие', 
                          message_id=call.message.message_id, 
                          reply_markup=admin_kb())
    

@bot.callback_query_handler(func=lambda call: call.data == 'add_admin')
def add_admin(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите id нового администратора')
    bot.set_state(call.from_user.id, 'add_admin', call.message.chat.id)
    
@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id, message.chat.id) == 'add_admin')
def add_admin(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'ID должен состоять только из цифр. Попробуйте ещё раз')
        return
    add_admin_id(int(message.text.strip()))
    bot.send_message(chat_id=message.chat.id, text='Администратор добавлен')
    bot.send_message(chat_id=message.chat.id, text='Выберите действие', reply_markup=admin_kb())
    bot.delete_state(message.from_user.id, message.chat.id)
    
    
@bot.callback_query_handler(func=lambda call: call.data == 'del_admin')
def del_admin(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text='Выберите администратора для удаления', 
                          reply_markup=delete_admins_kb(get_admin_ids()))
    bot.set_state(call.from_user.id, 'add_admin', call.message.chat.id)
    
@bot.callback_query_handler(func=lambda call: 'delete_admin' in call.data)
def del_admin(call):
    delete_admin_id(call.data)
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text='Администратор удален', 
                          reply_markup=delete_admins_kb(get_admin_ids()))
    
@bot.callback_query_handler(func=lambda call: call.data == 'check_follow_text')
def check_follow_text(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text='Выберите действие', 
                          reply_markup=change_follow_text_kb())
    
@bot.callback_query_handler(func=lambda call: call.data == 'change_text')
def change_text(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text='Введите и отправьте новый текст')
    bot.set_state(call.from_user.id, 'change_text', call.message.chat.id)
    
@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id, message.chat.id) == 'change_text')
def change_text(message):
    set_text(message.text)
    if message.entities:
        save_entities_to_json_file(message.entities)
    bot.send_message(chat_id=message.chat.id, text='Текст изменен')
    bot.send_message(chat_id=message.chat.id, text='Выберите действие', reply_markup=change_follow_text_kb())
    bot.delete_state(message.from_user.id, message.chat.id)
    
@bot.callback_query_handler(func=lambda call: call.data == 'view_text')
def view_text(call):
    entities = load_entities_from_json_file()
    
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=get_text(), entities=entities)
    bot.send_message(chat_id=call.message.chat.id,
                          text='Выберите действие', 
                          reply_markup=change_follow_text_kb())

@bot.callback_query_handler(func=lambda call: call.data == 'change_log_chat')
def change_log_chat(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text='Выберите действие',
                          reply_markup=change_log_chat_kb())

@bot.callback_query_handler(func=lambda call: call.data == 'change_log_chat_id')
def change_log_chat(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text='Введите и отправьте новый id чата для логов')
    bot.set_state(call.from_user.id, 'change_log_chat_id', call.message.chat.id)
    
@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id, message.chat.id) == 'change_log_chat_id')
def change_log_chat_id(message):
    set_log_chat_id(message.text)
    bot.send_message(chat_id=message.chat.id, text='Лог чата изменен')
    bot.send_message(chat_id=message.chat.id, text='Выберите действие', reply_markup=change_log_chat_kb())
    bot.delete_state(message.from_user.id, message.chat.id)
    



@bot.message_handler(content_types=['text', 'photo'])
def in_message(message):
    main_chats = [chat['id'][1:] for chat in get_main_chats()]
    
    if message.chat.username in main_chats:
        text = message.text if message.text else message.caption
        if message.from_user.id not in get_admin_ids():
            if get_check_follow_channels(message, bot):
                print('ok')
            else:
                delete_msg(message, 'Не подписан на каналы из списка')
                send_follow_message(message, bot)
                return
            if sp_bot.spam_base == True:
                if check_spam_base(text):
                    delete_msg(message, 'Спам База')
                    return
            if sp_bot.resend == True:
                if message.forward_from or message.forward_from_chat:
                    delete_msg(message, 'Пересылка')
                    return
            if sp_bot.frod == True:
                if len(message.text) > sp_bot.text_check_count:
                    messages = check_frod(message)
                    if messages:
                        for msg in messages:
                            delete_msg_frod(msg['chat_id'], msg['message_id'])
                        delete_msg_from_file(messages)
                        delete_msg(message, 'Рассылка')
                        return
            if sp_bot.multifrod == True:
                if len(message.text) > sp_bot.text_check_count:
                    messages = check_multifrod(message)
                    if messages:
                        for msg in messages:
                            delete_msg_frod(msg['chat_id'], msg['message_id'])
                        delete_msg_from_file(messages)
                        delete_msg(message, 'Рассылка с разных аккаунтов')
                        return
            if sp_bot.urls == True:
                if check_urls(message):
                    delete_msg(message, 'Ссылки')
                    return
            if sp_bot.hidden_text == True:
                if check_hidden_text(message):
                    delete_msg(message, 'Скрытый текст')
                    return
                        
            write_msg(message)
            
                

if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print(e)
            time.sleep(3)
