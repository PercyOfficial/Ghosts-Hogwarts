from telegram import ChatAction
import html
import urllib.request
import re
import json
from typing import Optional, List
import time
import urllib
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote_plus, urlencode
import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from emilia import dispatcher
from emilia.__main__ import STATS, USER_INFO
from emilia.modules.disable import DisableAbleCommandHandler
import wikipedia

def wiki(update, context):
    args=context.args
    args=str(args)
    args="dictionary " + args
    reply = "".join(args)
    summary = '{}'
    update.message.reply_text(summary.format(wikipedia.summary(reply, sentences=10), wikipedia.page(reply).url))
		
__help__ = """
 Ever stumbled upon a word that you didn't know of and wanted to look it up?
With this module, you can find the definitions of words without having to leave the app!
*Available commands:*
 - /define <word>: returns the definition of the word.
"""
__mod_name__ = "DICTIONARY"
WIKI_HANDLER = DisableAbleCommandHandler("define", wiki, pass_args=True)
dispatcher.add_handler(WIKI_HANDLER)
