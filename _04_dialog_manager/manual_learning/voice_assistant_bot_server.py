import telebot
from voice_assistant_helper import read_from_file
from decouple import config

API_KEY = read_from_file(file_path = config('TELEGRAM_BOT_KEY'))

bot = telebot.TeleBot(API_KEY)
registered_user_id = list()

@bot.message_handler(commands = ['help'])
def help(message):
    """
    sends overview of all available commands
    """
    response = read_from_file(config('BOT_HELP'))
    chat_id = message.chat.id
    bot.send_message(chat_id, response)
    

@bot.message_handler(commands = ['register'])
def register(message):
    """
    stores users chat id in list
    @params message: message sent
    """
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    
    if chat_id not in registered_user_id:
        registered_user_id.append(chat_id)
        bot.send_message(chat_id, f"User {user_name} succesfully registered!")
    else:
        bot.send_message(chat_id, f"User {user_name} is already registered!")


bot.polling()