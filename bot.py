import os
import telebot
from telebot import types

# Загрузка токена из переменной окружения
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Привет')
    btn2 = types.KeyboardButton('Как дела?')
    btn3 = types.KeyboardButton('Что делаешь?')
    markup.row(btn1)
    markup.add(btn2, btn3)
    
    # Отправляем фото (проверяем, существует ли файл)
    try:
        file = open('./photo.png', 'rb')
        bot.send_photo(message.chat.id, file)
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'Фото временно недоступно')
    
    bot.send_message(
        message.chat.id,
        'Добро пожаловать. Это мой первый бот!',
        reply_markup=markup
    )
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Как дела?':
        bot.send_message(message.chat.id, 'Все хорошо')
    elif message.text == 'Что делаешь?':
        bot.send_message(message.chat.id, 'Пишу в бота')
    elif message.text == 'Привет':
        bot.send_message(message.chat.id, 'Привет, привет, ознакомься с моим функционалом!')


@bot.message_handler(commands=['main', 'hello'])
def main(message):
    first_name = message.from_user.first_name or ''
    last_name = message.from_user.last_name or ''
    bot.send_message(
        message.chat.id,
        f'Привет, {first_name} {last_name}'.strip()
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        '<b>Help</b> <em><u>information</u></em>',
        parse_mode='html'
    )


@bot.message_handler()
def info(message):
    if message.text and message.text.lower() == 'привет':
        first_name = message.from_user.first_name or ''
        bot.send_message(
            message.chat.id,
            f'Привет привет, мой милый друг {first_name}'.strip()
        )
    elif message.text and message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com')
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn1)
    markup.add(btn2, btn3)
    bot.reply_to(message, 'Какое красивое фото!', reply_markup=markup)


# Обработка callback функций
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        except Exception:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'edit':
        try:
            bot.edit_message_text(
                'Edit text',
                callback.message.chat.id,
                callback.message.message_id
            )
        except Exception:
            pass


if __name__ == '__main__':
    print('Бот запущен...')
    bot.polling(none_stop=True)
