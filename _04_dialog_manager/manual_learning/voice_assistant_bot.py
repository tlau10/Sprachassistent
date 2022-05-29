import telebot
from voice_assistant_helper import read_from_file, read_from_file_by_line, write_to_file
from voice_assistant_bot_helper import store_entry
from decouple import config
import re

REQUEST_INPUT_FILE = config('BOT_REQUESTS')
API_KEY = read_from_file(file_path = config('TELEGRAM_BOT_KEY'))
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands = ['help'])
def help(message):
    """
    sends overview of all available commands
    @param message: message sent by user
    """
    response = read_from_file(config('BOT_HELP'))
    chat_id = message.chat.id
    bot.send_message(chat_id, response)

@bot.message_handler(commands = ['request'])
def get_request(message):
    """
    sends first line from requests file to user then removes line
    @param message: message sent by user
    """
    chat_id = message.chat.id

    # get all lines from file
    requests = read_from_file_by_line(file_path = REQUEST_INPUT_FILE)

    # check if file is empty
    if len(requests) == 0:
        bot.send_message(chat_id, "No request available!")
        return

    # get first line from file and send message
    request = requests[0].split(" ") 
    bot.send_message(chat_id, f"Intent: {request[0]} Slot: {request[1]} Value: {request[2]}")

    # remove first line from file
    del requests[0]
    write_to_file(file_path = REQUEST_INPUT_FILE, text = "".join(requests))
    
@bot.message_handler(commands = ['improve'])
def improve(message):
    """
    used to improve line from requests file, needs to be called on a reply to a message sent by the bot
    @param message: message sent by user
    """
    chat_id = message.chat.id

    # format of replied bot message
    request_regex = "Intent: .* Slot: .* Value: .*"

    # check if its a reply to a message sent by the bot and if the message sent by the bot has the correct format
    if message.reply_to_message is not None and \
        message.reply_to_message.from_user.is_bot is True and \
            re.match(request_regex, message.reply_to_message.text):

        # get replied message and message text
        replied_message_text = message.reply_to_message.text
        replied_message = replied_message_text.split(" ")
        improved_value = message.text.replace("/improve ", "")

        # save entry to json file
        store_entry((replied_message[1], replied_message[3], replied_message[5], improved_value))

        bot.send_message(chat_id, f"Succesfully improved {replied_message_text} with value: {improved_value}!")
    else:
        bot.send_message(chat_id, "Use by replying to a message sent by the voice assistant bot then type /improve followed by your improvement")

bot.polling()
