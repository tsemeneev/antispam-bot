from telebot import TeleBot


bot = TeleBot('7113011095:AAHPiIoO6S9Dk4PURppX9lWKtyZZuir0tYc')



@bot.message_handler()
def get_channel_info(channel_id):
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



info = get_channel_info('@test_cha33')
print(info)