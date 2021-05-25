import requests
import bs4 
import re
from telethon import *
from emilia import client
from emilia.events import register

from emilia import client, dispatcher
from emilia.events import register
from telegram.ext import CommandHandler , run_async
from emilia.modules.helper_funcs.chat_status import user_admin
from emilia.modules.helper_funcs.alternate import send_message

@run_async
@user_admin



def apk(update,context):
    
    try:
        args=context.args
        app_name = args[1]
        remove_space = app_name.split(' ')
        final_name = '+'.join(remove_space)
        page = requests.get("https://play.google.com/store/search?q="+final_name+"&c=apps")
        lnk = str(page.status_code)
        soup = bs4.BeautifulSoup(page.content,'lxml', from_encoding='utf-8')
        results = soup.findAll("div","ZmHEEd")
        app_name = results[0].findNext('div', 'Vpfmgd').findNext('div', 'WsMG1c nnK0zc').text
        app_dev = results[0].findNext('div', 'Vpfmgd').findNext('div', 'KoLSrc').text
        app_dev_link = "https://play.google.com"+results[0].findNext('div', 'Vpfmgd').findNext('a', 'mnKHRc')['href']
        app_rating = results[0].findNext('div', 'Vpfmgd').findNext('div', 'pf5lIe').find('div')['aria-label']
        app_link = "https://play.google.com"+results[0].findNext('div', 'Vpfmgd').findNext('div', 'vU6FJ p63iDd').a['href']
        app_icon = results[0].findNext('div', 'Vpfmgd').findNext('div', 'uzcko').img['data-src']
        app_details = "<a href='"+app_icon+"'>📲&#8203;</a>"
        app_details += " <b>"+app_name+"</b>"
        app_details += "\n\n<code>Developer :</code> <a href='"+app_dev_link+"'>"+app_dev+"</a>"
        app_details += "\n<code>Rating :</code> "+app_rating.replace("Rated ", "⭐ ").replace(" out of ", "/").replace(" stars", "", 1).replace(" stars", "⭐ ").replace("five", "5")
        app_details += "\n<code>Features :</code> <a href='"+app_link+"'>View in Play Store</a>"
        app_details += "\n\n 🍀 @MissDaisyRobot 🍀"
        asend_message(update.effective_message,app_details, link_preview = True, parse_mode = 'HTML')
    except IndexError:
        send_message(update.effective_message,"No result found in search. Please enter **Valid app name**")
    except Exception as err:
        send_message(update.effective_message,"Exception Occured:- "+str(err))
        
APK_HANDLER = CommandHandler('app', apk)

dispatcher.add_handler(APK_HANDLER)


__command_list__ = ["app"]
__handlers__ = [
    APK_HANDLER
]
