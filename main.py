import requests
import os
from telebot import telebot, types
from dotenv import load_dotenv
from deep_translator import GoogleTranslator


load_dotenv()

TOKEN = os.getenv("API_TOKEN")
API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(TOKEN)


def set_Cat(chat_id):
    with open("media/cat.jpg", "rb") as img:
        bot.send_photo(chat_id, photo=img)


def fatch_cats(chat_id):
    data = requests.get("https://api.thecatapi.com/v1/images/search", timeout=5).json()
    for el in data:
        url = el.get("url")

        if url.endswith(".gif"):
            bot.send_animation(chat_id, animation=url)
        else:
            bot.send_photo(chat_id, photo=el["url"])
            key_btn = types.InlineKeyboardButton(
                text="random cat image", callback_data="random"
            )
            bot.send_message(chat_id, text="хотите еще фото?", reply_markup=key_btn)


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    text = "хотите узнать интересные факты о кошках?"

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="да", callback_data="yes")
    key_no = types.InlineKeyboardButton(text="нет", callback_data="no")
    key_random = types.InlineKeyboardButton(
        text="рандомная фото", callback_data="random"
    )
    keyboard.add(key_yes, key_no, key_random)

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
    elif call.data == "no":
        set_Cat(chat_id)

    elif call.data == "random":
        fatch_cats(chat_id)
    bot.answer_callback_query(call.id)


@bot.message_handler(content_types=["text"])
def text_handler(message):
    chat_id = message.chat.id
    if message.text in ["да", "yes"]:
        print("yes")
        fatch_cats(chat_id)
    elif message.text in ["нет", "no"]:
        set_Cat(chat_id)


if __name__ == "__main__":
    print("running bot")
    bot.infinity_polling(none_stop=True, interval=0)
