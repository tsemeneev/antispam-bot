import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class TelegramBot:
        
    spam_base = True
    frod = False
    multifrod = False
    resend = False
    urls = False
    hidden_text = True
    text_check_count = 20
    log_chat_id = -1002230567948
    

def set_language_kb():
    keyb = InlineKeyboardMarkup(row_width=1)
    keyb.add(InlineKeyboardButton('Русский', callback_data='ru'),
             InlineKeyboardButton('English', callback_data='eng'))
    return keyb


        
        
def menu_kb(sp_bot: TelegramBot) -> InlineKeyboardMarkup:
    spam_base = '✅' if sp_bot.spam_base else '❌'
    frod = '✅' if sp_bot.frod else '❌'
    multifrod = '✅' if sp_bot.multifrod else '❌'
    resend = '✅' if sp_bot.resend else '❌'
    urls = '✅' if sp_bot.urls else '❌'
    hidden_text = '✅' if sp_bot.hidden_text else '❌'
    keyb = InlineKeyboardMarkup(row_width=1)
    keyb.add(InlineKeyboardButton(f'Спам база({spam_base})', callback_data='spam_base'),
                # InlineKeyboardButton(f'Рассылка({frod})', callback_data='frod'),
                # InlineKeyboardButton(f'Рассылка с разных аккаунтов({multifrod})', callback_data='multifrod'),
                InlineKeyboardButton(f'Пересланные сообщения({resend})', callback_data='resend'),
                InlineKeyboardButton(f'Ссылки({urls})', callback_data='urls'),
                InlineKeyboardButton(f'Скрытый текст({hidden_text})', callback_data='hidden_text'),
                InlineKeyboardButton(f'Изменить основной чат', callback_data='main_chat'),
                InlineKeyboardButton(f'Изменить мин. кол-во символов фильтрации рассылки({sp_bot.text_check_count})', callback_data='text_check_count'),
                InlineKeyboardButton('Изменить каналы для обязательной подписки', callback_data='check_follow_channels'),
                InlineKeyboardButton('Изменить id администраторов', callback_data='admin_ids'),
                InlineKeyboardButton('Изменить сообщение о необходимости подписки', callback_data='check_follow_text'),
                InlineKeyboardButton('Изменить чат для логов', callback_data='change_log_chat'))
    return keyb


def change_main_chat_kb() -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup(row_width=1)
    keyb.add(InlineKeyboardButton('Список основных чатов', callback_data='list_main_chats'),
            InlineKeyboardButton('Добавить чат', callback_data='add_main_chat'),
            InlineKeyboardButton('Удалить чат', callback_data='del_main_chat'),
            InlineKeyboardButton('Назад', callback_data='menu'))
    return keyb

def list_main_chats_kb(main_chats: list) -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup(row_width=1)
    for main_chat in main_chats:
        url = main_chat["id"][1:]
        keyb.add(InlineKeyboardButton(main_chat['username'], url=f'https://t.me/{url}'))
    keyb.add(InlineKeyboardButton('Назад', callback_data='main_chat'))
    return keyb


def delete_main_chat_kb(main_chats: list) -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup(row_width=1)
    for main_chat in main_chats:
        keyb.add(InlineKeyboardButton('Удалить чат ' + main_chat['username'], callback_data=f'delete_chat_{main_chat["username"]}'))
    keyb.add(InlineKeyboardButton('Назад', callback_data='main_chat'))
    return keyb


def get_main_chats() -> list:
    with open('admin_data.json' ) as f:
        data = json.load(f)
    return data[0]['main_chats']


def add_main_chat_to_list(chat: list) -> None:
    chat_data = {
        "username": chat[0].strip(),
        "id": chat[1].strip()
    }
    with open('admin_data.json') as f:
        data = json.load(f)
    data[0]['main_chats'].append(chat_data)
    with open('admin_data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
        
def delete_main_chat_from_list(name: str) -> None:
    with open('admin_data.json') as f:
        data = json.load(f)
    for chat in data[0]['main_chats']:
        if chat['username'] == name.split('_')[-1]:
            data[0]['main_chats'].remove(chat)
            break
    with open('admin_data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        


def change_follow_channels_kb() -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup(row_width=1)
    keyb.add(InlineKeyboardButton('Список каналов', callback_data='list_channels'),
            InlineKeyboardButton('Добавить канал', callback_data='add_channel'),
            InlineKeyboardButton('Удалить канал', callback_data='del_channel'),
            InlineKeyboardButton('Назад', callback_data='menu'))
    return keyb


def list_channels_kb(channels: list) -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        keyb.add(InlineKeyboardButton(channel['name'], url=f'https://t.me/{channel["username"]}'))
    keyb.add(InlineKeyboardButton('Назад', callback_data='check_follow_channels'))
    return keyb


def delete_channels_kb(channels: list) -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        keyb.add(InlineKeyboardButton('Удалить канал ' + channel['name'], callback_data=f'delete_channel_{channel["username"]}'))
    keyb.add(InlineKeyboardButton('Назад', callback_data='check_follow_channels'))
    return keyb


def admin_kb() -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup(row_width=1)
    keyb.add(InlineKeyboardButton('Добавить администратора', callback_data='add_admin'),
            InlineKeyboardButton('Удалить администратора', callback_data='del_admin'),
            InlineKeyboardButton('Назад', callback_data='menu'))
    return keyb

def delete_admins_kb(admin_ids: list) -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup(row_width=1)
    for admin_id in admin_ids:
        keyb.add(InlineKeyboardButton('Удалить администратора ' + str(admin_id), callback_data=f'delete_admin_{admin_id}'))
    keyb.add(InlineKeyboardButton('Назад', callback_data='admin_ids'))
    return keyb

def change_follow_text_kb() -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup(row_width=1)
    keyb.add(InlineKeyboardButton('Изменить текст', callback_data='change_text'),
            InlineKeyboardButton('Посмотреть текст', callback_data='view_text'),
            InlineKeyboardButton('Назад', callback_data='menu'))
    return keyb

def change_log_chat_kb() -> InlineKeyboardMarkup:
    keyb = InlineKeyboardMarkup(row_width=1)
    keyb.add(InlineKeyboardButton('Изменить чат', callback_data='change_log_chat_id'),
            InlineKeyboardButton('Назад', callback_data='menu'))
    return keyb


def get_list_channels() -> list:
    with open('admin_data.json' ) as f:
        data = json.load(f)
    return data[0]['channels']


def get_channel_info(channel_id, bot):
    try:
        # Получаем информацию о канале
        chat = bot.get_chat(channel_id)
        # Возвращаем ID, название и username канала
        return {
            'id': chat.id,
            'name': chat.title,
            'username': chat.username
        }
    except Exception as e:
        # Если произошла ошибка, возвращаем сообщение об ошибке
        return {'error': str(e)}

def add_channel_to_list(channel, bot) -> None:
    channel_data = get_channel_info(channel, bot)
    with open('admin_data.json') as f:
        data = json.load(f)
    data[0]['channels'].append(channel_data)
    with open('admin_data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
        
def delete_channel_from_list(name: str) -> None:
    with open('admin_data.json') as f:
        data = json.load(f)
    for channel in data[0]['channels']:
        if channel['username'] == name.split('_')[-1]:
            data[0]['channels'].remove(channel)
            break
    with open('admin_data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
        
def get_admin_ids() -> list:
    with open('admin_data.json' ) as f:
        data = json.load(f)
    return data[0]['admins']

def add_admin_id(id: str) -> None:
    with open('admin_data.json') as f:
        data = json.load(f)
    data[0]['admins'].append(id)
    with open('admin_data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    
def delete_admin_id(id: str) -> None:
    admin_id = int(id.split('_')[-1])
    with open('admin_data.json') as f:
        data = json.load(f)
    data[0]['admins'].remove(admin_id)
    with open('admin_data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
        
def get_text() -> str:
    with open('admin_data.json' ) as f:
        data = json.load(f)
    return data[0]['text']


def set_text(text: str) -> None:
    with open('admin_data.json') as f:
        data = json.load(f)
    data[0]['text'] = text
    with open('admin_data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)