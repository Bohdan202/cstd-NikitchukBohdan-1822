import traceback
import sys, os

from config import bot
from telegram import game
from telegram import weather
from telegram.functions import log
from telegram.localization import texts
from other.firebase import firebase
from music import youtube_downloader

from telebot import types
from googletrans import Translator
translator = Translator(service_urls=['translate.googleapis.com'])

import random
import time

import json
import codecs


print('test bot start')

@bot.message_handler(commands=['start'])
def start_handler(message):
    # bot.send_message(message.chat.id, '')
    pass


@bot.message_handler(commands=['ruhelp', 'uahelp', 'enhelp'])
def help_handler(message):
    language = message.text[1:3]
    print(language)
    bot.send_message(message.chat.id, texts[language]['help'])


@bot.message_handler(content_types=['text'])
def text_handler(message):
    # print(message, message.chat.id)

    try:
        if message.text == 'Привет' or message.text == 'привет':
            bot.send_message(message.chat.id, 'Привет')

        elif message.text == 'Пока' or message.text == 'пока':
            bot.send_message(message.chat.id, 'Прощай')

        elif message.text == '!error':
            temp = None
            print(temp.temp)

        elif message.text == 'Кнопки' or message.text == 'кнопки':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Кнопка 1', callback_data='button_0.1'))
            markup.add(types.InlineKeyboardButton(text='Кнопка 2', callback_data='button_0.2'))
            markup.add(types.InlineKeyboardButton(text='Кнопка 3', callback_data='button_0.3'))
            # markup.add(types.InlineKeyboardButton(text='Кнопка 4', url='https://www.google.com.ua'))
            # markup.add(types.InlineKeyboardButton(text='Кнопка 5', callback_data='button_0.5'))
            bot.send_message(message.chat.id, text='Кнопки', reply_markup=markup)

        elif len(message.text) > 2 and message.text.find('t ') == 0:
            result = translator.translate(message.text[2:], src='en', dest='ru')

            bot.reply_to(message, result.text)
            log(message, 'translate', result.text)

        elif len(message.text) > 2 and message.text.find('т ') == 0:
            result = translator.translate(message.text[2:], scr='ru', dest='en')

            bot.reply_to(message, result.text)
            log(message, 'translate', result.text)

        elif len(message.text) > 2 and (message.text.find('r ') == 0 or message.text.find('р ') == 0):
            result = message.text[2:]
            result = result.split(' ')
            if (len(result) == 1):
                result = result[0]
            i = random.randint(0, len(result)-1)
            result = result[i]

            bot.reply_to(message, result)
            log(message, 'random', result)

        elif len(message.text) > 2 and (message.text.find('p ') == 0 or message.text.find('п ') == 0):
            arg = message.text[2:]
            arg = arg.split(' ')

            if len(arg) == 2 and (int(arg[1]) > 0 and int(arg[1]) <= 10):
                result = weather.get_weather_fordays('ua', arg[0], int(arg[1]))
                bot.send_message(message.chat.id, result, parse_mode="HTML")
            elif len(arg) == 1:
                result = weather.get_weather_fordays('ua', arg[0])
                bot.send_message(message.chat.id, result, parse_mode="HTML")

            log(message, 'weather', '')

        elif message.text == 'get_id' or message.text == 'гони айди':
            bot.send_message(message.chat.id, message.from_user.id)
            log(message, 'get id', str(message.from_user.id))

        elif message.text.find('set_playlist ') == 0:
            arg = message.text[13:]
            arg = arg.split('\n')
            
            songs = {}

            for i, song in enumerate(arg[1:]):
                songs[i] = song

            firebase.set_playlist(arg[0], songs)

            log(message, 'firebase set_playlist', '')

        elif message.text.find('get_playlist ') == 0:
            arg = message.text[13:]
            songs = firebase.get_playlist(arg)

            result = ''
            for song in songs:
                result += song + '\n'

            bot.send_message(message.chat.id, result)

            log(message, 'firebase get_playlist', '')

        elif message.text.find('add_in_playlist ') == 0:
            arg = message.text[16:]
            arg = arg.split('\n')

            songs = firebase.get_playlist(arg[0])
            songs += arg[1:]

            result = {}

            for i, song in enumerate(songs[1:]):
                result[i] = song

            firebase.set_playlist(arg[0], result)

            log(message, 'firebase add_in_playlist', '')

        elif message.text.find('get_yt ') == 0:
            arg = message.text[7:]
            title, file_name = youtube_downloader.get_music(arg)
            
            try:
                audio = open(file_name, 'rb')
                bot.send_audio(message.chat.id, audio=audio, title=title)
                audio.close()
            except:
                pass

            os.remove(file_name)
            
    
    except:
        print(traceback.format_exc())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        # print(call)

        # Если сообщение из чата с ботом
        if call.message:
            if call.data == "button_0.1":
                bot.answer_callback_query(call.id, "Хорошо", show_alert=True)
            if call.data == "button_0.2":
                bot.answer_callback_query(call.id, "Хорошо", show_alert=False)
            if call.data == "button_0.3":
                bot.answer_callback_query(callback_query_id=call.id, url='https://www.google.com.ua')
            if call.data == "button_0.5":
                pass

                
        # Если сообщение из инлайн-режима
        elif call.inline_message_id:
            if call.data == "cерии":
                bot.send_message(call.inline_message_id, text="C1")
    
    except:
        print(traceback.format_exc())


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    print(message)
    # file_info = bot.get_file(message.voice.file_id)


@bot.message_handler(content_types=['audio'])
def audio_processing(message):
    try:
        song = message.audio.performer + ' ' + message.audio.title
        firebase.add_song(message.chat.id, song)
    except:
        print(traceback.format_exc())


import threading

def start_telethread(bot):
    while True:
        try:
            firebase.report("telegram bot started")
            bot.polling()
        except:
            print(traceback.format_exc())
            firebase.report('telegram: error')
            time.sleep(1)

thread = threading.Thread(target=start_telethread, args=[bot])
thread.start()