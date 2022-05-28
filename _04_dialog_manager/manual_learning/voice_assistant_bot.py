import telebot
from voice_assistant_helper import read_from_file, read_json_file, write_json_file
from decouple import config

API_KEY = read_from_file(file_path = config('TELEGRAM_BOT_KEY'))
JSON_FILE_OUTPUT_PATH = config('BOT_ENTRIES')

bot = telebot.TeleBot(API_KEY)
registered_user_id = list()
commands = ['help', 'subscribe', 'unsubscribe', 'improve']

@bot.message_handler(commands = [commands[0]])
def help(message):
    """
    sends overview of all available commands
    """
    response = read_from_file(config('BOT_HELP'))
    chat_id = message.chat.id
    bot.send_message(chat_id, response)
    

@bot.message_handler(commands = [commands[1]])
def subscribe(message):
    """
    subscribes user by adding chat id to list
    @params message: message sent
    """
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    
    if chat_id not in registered_user_id:
        registered_user_id.append(chat_id)
        bot.send_message(chat_id, f"User {user_name} succesfully subscribed!")
    else:
        bot.send_message(chat_id, f"User {user_name} is already subscribed!")

@bot.message_handler(commands = [commands[2]])
def unsubscribe(message):
    """
    unsubscribes user by removing chat id from list
    @params message: message sent
    """
    chat_id = message.chat.id
    user_name = message.from_user.first_name

    if chat_id in registered_user_id:
        registered_user_id.remove(chat_id)
        bot.send_message(chat_id, f"User {user_name} succesfully unsubscribed!")
    else:
        bot.send_message(chat_id, f"User {user_name} is not subscribed!")

@bot.message_handler(commands = [commands[3]])
def improve(message):
    chat_id = message.chat.id

    # check if its a reply to a message sent by the bot
    if message.reply_to_message is not None and message.reply_to_message.from_user.is_bot is True:
        replied_message = message.reply_to_message.text

        bot.send_message(chat_id, f"Succesfully improved {replied_message}!")

        intent, slot, recognized_value = replied_message.split(": ")
        improved_value = message.text.replace("/improve ", "")

        store_entry((intent, slot, recognized_value, improved_value))
    else:
        bot.send_message(chat_id, f"Use by replying to a message sent by the voice assistant bot then type /{commands[3]} followed by your improvement")

def store_entry(entry):
    """
    writes new entry to json file
    @param entry: entry to write to file as tuple(intent, slot, replied_message, improved_message)
    """
    intent, slot, recognized_value, improved_value = entry
    print(f"intent: {intent}, slot: {slot}, recognized_value: {recognized_value}, improved_value: {improved_value}")

    # read json
    entries = read_json_file(file_path = JSON_FILE_OUTPUT_PATH)

    # retrieve entry
    entry = entries[intent][slot]

    # append new key value pair
    kv = {recognized_value : improved_value}
    entry['values'] = kv

    write_json_file(file_path = JSON_FILE_OUTPUT_PATH, json_object = entries)

bot.polling()