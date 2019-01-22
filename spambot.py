#!/usr/bin/python
# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, Handler
from telegram import ParseMode
import re
import logging

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOKEN = "796287471:AAGxBMXrTXHgRhRV9dZaiB_7Hv4Stw13AZQ"
updater = Updater(token=TOKEN)

HELP_TEXT = """
    Привет, я бот для рассылки сообщений по чатам. Я буду слать сообщения во все чаты, в которые ты меня добавишь.

    Сообщения можно форматировать с помощью markdown - https://gist.github.com/Jekins/2bf2d0638163f1294637 

    *Доступные команды:*
    - /new_post {text} - отправит по всем добавленным чатам сообщение. 
    - /test_post {text} - отправит тебе сообщение чтобы ты мог увидеть, как оно выглядит перед постом в чаты.
    - /added_chats - отображает информацию о добавленных чатах
    - /help - увидеть этот текст
"""

ALLOWED_USERS = [397351, 203562902]

dispatcher = updater.dispatcher

def new_member(bot, update):
    for member in update.message.new_chat_members:
        if member.username == 'Kolya71Bot':
            with open("./data/chat_ids.txt", "a") as chats_file:
                chats_file.write(str(update.message.chat.id))
            with open("./data/chat_infos.txt", "a") as chats_file:
                chat_info = '{} - {} (added {})'.format(update.message.chat.id, update.message.chat.title, update.message.date.strftime("%d/%m/%y %H:%M"))
                chats_file.write(chat_info)

def new_post(bot, update):
    if update.message.from_user.id in ALLOWED_USERS:
        with open("./data/chat_ids.txt", "r") as chats_file:
            chat_ids = set([re.sub('\n+', '', s) for s in chats_file.readlines()])
            for chat_id in chat_ids:
                text = update.message.text.replace('/new_post', '').strip()
                bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=update.message.chat.id, text='Сори чувак, но я общаюсь только со своими братишками @danonechik94, @Thunderbirddd')

def test_post(bot, update):
    if update.message.from_user.id in ALLOWED_USERS:
        text = update.message.text.replace('/test_post', '').strip()
        bot.send_message(chat_id=update.message.chat.id, text=text, parse_mode=ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=update.message.chat.id, text='Сори чувак, но я общаюсь только со своими братишками @danonechik94, @Thunderbirddd')

def help(bot, update):
    if update.message.from_user.id in ALLOWED_USERS:
        bot.send_message(chat_id=update.message.chat.id, text=HELP_TEXT)
    else:
        bot.send_message(chat_id=update.message.chat.id, text='Сори чувак, но я общаюсь только со своими братишками @danonechik94, @Thunderbirddd')

def added_chats(bot, update):
    if update.message.from_user.id in ALLOWED_USERS:
        with open("./data/chat_infos.txt", "r") as chats_infos_file:
            bot.send_message(chat_id=update.message.chat.id, text=chats_infos_file.read(), parse_mode=ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=update.message.chat.id, text='Сори чувак, но я общаюсь только со своими братишками @danonechik94, @Thunderbirddd')


new_post_handler = CommandHandler("new_post", new_post)
test_post_handler = CommandHandler("test_post", test_post)
help_handler = CommandHandler("help", help)
added_chats_handler = CommandHandler("added_chats", added_chats)
dispatcher.add_handler(new_post_handler)
dispatcher.add_handler(test_post_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(added_chats_handler)
updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))

updater.start_polling()
updater.idle()

