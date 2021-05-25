import asyncio
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from emilia.events import register
from emilia import client, dispatcher
import sys
import shutil
from re import findall
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *
import html2text

from telegram.ext import CommandHandler , run_async
from emilia.modules.helper_funcs.chat_status import user_admin
from emilia.modules.helper_funcs.alternate import send_message





@run_async
@user_admin
def google(update,context):

    # SHOW_DESCRIPTION = False
    args = context.args
    information = str(args)
    input_str = information # + " -inurl:(htm|html|php|pls|txt) intitle:index.of \"last modified\" (mkv|mp4|avi|epub|pdf|mp3)"
    input_url = "https://bots.shrimadhavuk.me/search/?q={}".format(input_str)
    headers = {"USER-AGENT": "UniBorg"}
    response = requests.get(input_url, headers=headers).json()
    output_str = " "
    for result in response["results"]:
        text = result.get("title")
        url = result.get("url")
        description = result.get("description")
        last = html2text.html2text(description)
        output_str += "[{}]({})\n{}\n".format(text, url, last)       
    send_message(update.effective_message,"{}".format(output_str), link_preview=False, parse_mode='Markdown')


__help__ = """
 ➩ /google <text input> Gets google search result
 ➩ /img <object> Gets google image results
 ➩ /reverse : Reverse searches image or stickers on google.
 ➩ /gps <location> Get gps location
"""

__mod_name__ = "GOOGLE"

GOOGLE_HANDLER = CommandHandler('google', google)

dispatcher.add_handler(GOOGLE_HANDLER)


__command_list__ = ["google"]
__handlers__ = [
    GOOGLE_HANDLER
]
