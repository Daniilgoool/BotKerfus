!pip install pytelegrambotapi -q
!pip install diffusers -q
!pip install deep-translator -q

!pip install -U g4f --quiet
!pip install browser-cookie3 --quiet
!pip install aiohttp_socks --quiet

import telebot;
bot = telebot.TeleBot('TOKEN'); 
from telebot import types
from deep_translator import GoogleTranslator
import g4f
from g4f.Provider import (
    GeekGpt,
    Liaobots,
    Phind,
    Raycast,
    RetryProvider)
from g4f.client import Client
import nest_asyncio
from diffusers import DiffusionPipeline
import torch

def send_request(message):
    global chat_history
    chat_history[0]["content"] += message + " "

    try:
        response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=chat_history
    )
    except Exception as err:
        print("Все провайдеры не отвечают, попробуйте пойзже")
    chat_history[0]["content"] += response + " "
    return response


# Запуск бота, с зацикливанием, для постоянной работы
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Приветствие")
    btn2 = types.KeyboardButton(" Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Привет! Можешь спрашивать меня! Что тебя интересует?', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Приветствие"):
        bot.send_message(message.chat.id, text="Привет! Спасибо, что восьпользовался мною <3")
    elif (message.text == " Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как тебя зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif (message.text == "Как тебя зовут?"):
        bot.send_message(message.chat.id, "Меня зовут, Керфус ")

    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id,
                         text="Я могу рассказать о любом предмете")

    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(" Приветствие")
        button2 = types.KeyboardButton(" Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        inp = GoogleTranslator(source='auto', target='en').translate(message.text)
        inp1 = "Tell me about of " + inp
        print(inp1)
        # Отправка текста
        bot.send_message(message.chat.id, out)
        


bot.polling(none_stop=True, interval=0)
