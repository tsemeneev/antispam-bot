from datetime import datetime
import json
import re
import time 
from telebot import types


def check_spam_base(text: str) -> bool:
    spam_base = read_admin_data()[0]['spam_base']
    for w in spam_base:
        if w.lower() in text.lower():
            return True


def save_entities_to_json_file(entities, filename='entities.json'):
    entities_list = [
        {
            'type': entity.type,
            'offset': entity.offset,
            'length': entity.length,
            'url': getattr(entity, 'url', None),  # Только для 'text_link'
            'user': getattr(entity, 'user', None)  # Только для 'text_mention'
        } for entity in entities if isinstance(entity, types.MessageEntity)
    ]
    
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(entities_list, jsonfile, indent=2)
        
def load_entities_from_json_file(filename='entities.json'):
    with open(filename, 'r', encoding='utf-8') as jsonfile:
        entities_data = json.load(jsonfile)
        
    entities = []
    for entity_data in entities_data:
        if entity_data['type'] == 'text_mention' and entity_data['user']:
            user_data = entity_data['user']
            user = types.User(user_data['id'], user_data['is_bot'],
                              user_data.get('first_name', ''),
                              user_data.get('last_name', ''),
                              user_data.get('username', ''),
                              user_data.get('language_code', ''))
            entities.append(types.MessageEntity(entity_data['type'],
                                                entity_data['offset'],
                                                entity_data['length'],
                                                user=user))
        elif entity_data['type'] == 'text_link' and entity_data['url']:
            entities.append(types.MessageEntity(entity_data['type'],
                                                entity_data['offset'],
                                                entity_data['length'],
                                                url=entity_data['url']))
        else:
            entities.append(types.MessageEntity(entity_data['type'],
                                                entity_data['offset'],
                                                entity_data['length']))
        
    return entities
      
    
def get_update_spam_base(update: list) -> bool:
    admin_data = read_admin_data()
    admin_data[0]['spam_base'] = update
    with open('admin_data.json', 'w',  encoding='utf-8') as f:
        json.dump(admin_data, f, indent=4, ensure_ascii=False)
            
def check_frod(message: object) -> bool:
    messages = read_msg()
    message_text = message.text if message.text else message.caption
    finded_messages = [msg for msg in messages if msg['user_id'] == message.from_user.id and msg['message'] == message_text]
    return finded_messages if len(finded_messages) > 0 else False


def check_multifrod(message: object) -> bool:
    messages = read_msg()
    message_text = message.text if message.text else message.caption
    finded_messages = [msg for msg in messages if msg['message'] == message_text]
    if len(finded_messages) > 0:
        return finded_messages
    return False


def check_urls(message: object) -> bool:
    message_text = message.text if message.text else message.caption
    pattern = r'\b(?:https?://)?(?:www\.)?[a-zA-Zа-яА-Я0-9]+\.[a-zA-Zа-яА-Я]{2,}\b'
    match = re.search(pattern, message_text)
    if match:
        return True
    match = re.search(r'@', message_text)
    if match:
        return True
    return False
                

def check_hidden_text(message: object) -> bool:
    if message.entities:  # Если в сообщении есть сущности
        for entity in message.entities:
            if entity.type == 'spoiler':  # Проверяем на наличие спойлера
                return True
    return False

        
        
def write_msg(message: object) -> None:
    time = datetime.now().strftime('%H:%M')
    now = datetime.now().time()
    message_text = message.text if message.text else message.caption
    data = {
        "chat_id": message.chat.id,
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "time": time,
        "message": message_text,
        "message_id": message.message_id
    }
    
    with open('messages.json', 'r+', encoding='utf-8') as f:
        messages = json.load(f)
        messages.append(data)
        messages = [i for i in messages if (datetime.combine(datetime.min, now) - datetime.combine(datetime.min, datetime.strptime(i['time'], "%H:%M").time())).total_seconds() / 60 < 15]
        f.seek(0)
        json.dump(messages, f, indent=4, ensure_ascii=False)
        f.truncate()

def delete_msg_from_file(messages: list[dict]) -> None:
    for msg in messages:
        with open('messages.json', 'r+', encoding='utf-8') as f:
            messages = json.load(f)
            messages = [i for i in messages if i['message_id'] != msg['message_id']]
            f.seek(0)
            json.dump(messages, f, indent=4, ensure_ascii=False)
            f.truncate()
        
def read_msg() -> list[dict]:
    with open('messages.json', 'r', encoding='utf-8') as f:
        return json.load(f)
        
def read_admin_data() -> list[dict]:
    with open('admin_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)
        
def get_check_follow_channels(message: object, bot: object) -> bool:
    channels = read_admin_data()[0]['channels']
    if len(channels) == 0:
        return True
    print('tut')
    user_id = message.from_user.id
    try:
        return all(bot.get_chat_member(chat_id=channel['id'], user_id=user_id).status != 'left' for channel in channels)
    except Exception as e:
        if e.result_json['error_code'] == 400 and 'user not found' in e.result_json['description']:
            print(e)
            return False
        

def read_user_warnings() -> list[dict]:
    with open('user_warnings.json', 'r', encoding='utf-8') as f:
        return json.load(f)    

# def check_follow_channels_message(message: object, bot: object) -> bool:
#     user_warnings = read_user_warnings()
#     print('user_warnings')
#     user_id: int = message.from_user.id
#     now = datetime.now().time()
#     for warning in user_warnings[0]['user']:
#         if warning['user_id'] == user_id:
#             if (datetime.combine(datetime.min, now) - datetime.combine(datetime.min, datetime.strptime(warning['time'], "%H:%M").time())).total_seconds() / 60 < 1:
#                 return
#             warning['count'] += 1
#             if warning['count'] < 6:
#                 write_user_warnings(user_warnings)
#                 send_follow_message(message, bot)
#             return

#     user_warnings[0]['user'].append({
#         'user_id': user_id,
#         'count': 1,
#         'time': datetime.now().strftime('%H:%M')
#     })
#     write_user_warnings(user_warnings)
#     send_follow_message(message, bot)
    

    
def write_user_warnings(user_warnings: list[dict]) -> None:
    with open('user_warnings.json', 'w',  encoding='utf-8') as f:
        json.dump(user_warnings, f, indent=4, ensure_ascii=False)
        
        
def send_follow_message(message: object, bot: object) -> None:
    data = read_admin_data()
    text = data[0]['text']
    entities = load_entities_from_json_file()
    buttons = types.InlineKeyboardMarkup()
    for channel in data[0]['channels']:
        buttons.add(types.InlineKeyboardButton(text=f'{channel['name']}', url=f'https://t.me/{channel["username"]}'))
    sent = bot.send_message(message.chat.id, text=text, entities=entities, reply_markup=buttons, )
    time.sleep(15)
    bot.delete_message(chat_id=message.chat.id, message_id=sent.message_id)
    
def set_log_chat_id(log_chat_id: int) -> None:
    data = read_admin_data()
    data[0]['log_chat_id'] = log_chat_id
    with open('admin_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        

def get_log_chat_id() -> int:
    data = read_admin_data()
    return data[0]['log_chat_id']

def click_spam_base(value):
    with open('admin_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[0]['spam_base_'] = value
    with open('admin_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
def click_resend(value):
    with open('admin_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[0]['resend'] = value
    with open('admin_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
def click_hidden_text(value):
    with open('admin_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[0]['hidden_text'] = value
    with open('admin_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
        
def click_frod(value):
    with open('admin_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[0]['frod'] = value
    with open('admin_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
        
def click_urls(value):
    with open('admin_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[0]['urls'] = value
    with open('admin_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
        
def click_text_check_count(value):
    with open('admin_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[0]['text_check_count'] = value
    with open('admin_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
