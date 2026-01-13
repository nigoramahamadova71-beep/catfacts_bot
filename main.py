import requests
import os
from telebot import telebot, types
from dotenv import load_dotenv
from deep_translator import GoogleTranslator


load_dotenv()

TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    text = "хотите узнать интересные факты о кошках?"

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="да", callback_data="yes")
    keyboard.add(key_yes)
    # key_no = types.InlineKeyboardButton(text="нет", callback_data="no")
    # keyboard.add(key_no)

    bot.send_message(chat_id, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    chat_id = call.message.chat.id
    if call.data == "yes":
        data = requests.get("https://catfact.ninja/fact").json()
        text_to_translate = data["fact"]
        translation = GoogleTranslator(source="en", target="ru").translate(
            text_to_translate
        )

        bot.send_message(chat_id, text=translation)


bot.polling(none_stop=True, interval=0)
