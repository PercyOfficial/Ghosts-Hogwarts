from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

from emilia import dispatcher
from emilia.modules.helper_funcs.alternate import send_message
from emilia.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
import os
import json
import requests
from tabulate import tabulate
from urllib.request import urlopen

def sign_delta(delta_var):
    if delta_var < 0:
        delta_var = str(format(delta_var, ',d'))
    else:
        delta_var = '+' + str(format(delta_var, ',d'))
    return delta_var

@run_async
def cov(update, context):
    message = update.effective_message
    confirmed = 0
    confirmed_delta = 0
    deceased = 0
    deceased_delta = 0
    active = 0
    active_delta = 0
    recovered = 0
    recovered_delta = 0
    mortality_rate = 0
    recovery_rate = 0
    country_input = ''
    state_input = ''
    district_input = ''

    loc_input = message.text.split(',')
    if len(loc_input) > 2:
        district_input = loc_input[2].strip()
    if len(loc_input) > 1:
        state_input = loc_input[1].strip()
    if len(loc_input) > 0:
        country_input = loc_input[0][4:].strip()

    try:
        url_global = "https://bing.com/covid/data"
        json_response = requests.get(url_global)
        global_dict = json.loads(json_response.text)
        
        target = {}

        if country_input:
            for country in global_dict['areas']:
                if country['displayName'].lower() == country_input.lower():
                    if state_input:
                        for state in country['areas']:
                            if state['displayName'].lower() == state_input.lower():
                                if district_input:
                                    for district in state['areas']:
                                        if district['displayName'].lower() == district_input.lower():
                                            target = district
                                else:
                                    target = state
                    else:
                        target = country
        else:
            target = global_dict

        if not target:
            message.reply_text(
                'Data unavailable for %s!' % (message.text[4:].strip()))
            
            return

        confirmed = int(target['totalConfirmed'] or 0)
        confirmed_delta = int(target['totalConfirmedDelta'] or 0)
        deceased = int(target['totalDeaths'] or 0)
        deceased_delta = int(target['totalDeathsDelta'] or 0)
        recovered = int(target['totalRecovered'] or 0)
        recovered_delta = int(target['totalRecoveredDelta'] or 0)
        active = confirmed - deceased - recovered
        active_delta = confirmed_delta - deceased_delta - recovered_delta

        mortality_rate = (deceased / confirmed) * 100
        recovery_rate = (recovered / confirmed) * 100

        location = target['displayName'].upper()
        message.reply_text(
            '`COVID-19 Tracker:` *%s*\n\n' % location.upper() +
            '*Confirmed:* %s _(%s)_\n' % (format(confirmed, ',d'), sign_delta(confirmed_delta)) +
            '*Active:* %s _(%s)_\n' % (format(active, ',d'), sign_delta(active_delta)) +
            '*Deceased:* %s _(%s)_\n' % (format(deceased, ',d'), sign_delta(deceased_delta)) +
            '*Recovered:* %s _(%s)_\n\n' % (format(recovered, ',d'), sign_delta(recovered_delta)) +
            '*Mortality rate:* %s%%\n' % round(mortality_rate, 2) +
            '*Recovery rate:* %s%%\n\n' % round(recovery_rate, 2) +
            '[Powered by Bing.](https://bing.com/covid)',
            parse_mode = ParseMode.MARKDOWN,
            disable_web_page_preview = True)

        
        return

    except:
        message.reply_text(
            'Unable to contact the Bing COVID-19 Data API. Try again in a while.')
        
        return


__help__ = """
 - /covid <country> <state> <locality>: Get real time COVID-19 stats for the input location.
 - /covid : Gives Covid world stats.
"""



COV_HANDLER = CommandHandler('cov', cov)

dispatcher.add_handler(COV_HANDLER)

__mod_name__ = "COVID-19 Tracker"
__command_list__ = ["cov"]
__handlers__ = [
    COV_HANDLER
]
