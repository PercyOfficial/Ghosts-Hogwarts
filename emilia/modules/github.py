from telegram import ParseMode, Update, Bot
from telegram.ext import run_async

from emilia.modules.disable import DisableAbleCommandHandler
from emilia import dispatcher
from emilia.modules.helper_funcs.alternate import send_message

from requests import get


@run_async
def github(update,context):
    message = update.effective_message
    text = message.text[len('/git '):]
    usr = get(f'https://api.github.com/users/{text}').json()
    if usr.get('login'):
        reply_text = (f"""*Name:* `{usr['name']}`"
*Username:* `{usr['login']}`
*Account ID:* `{usr['id']}`
*Account type:* `{usr['type']}`
*Location:* `{usr['location']}`
*Bio:* `{usr['bio']}`
*Followers:* `{usr['followers']}`
*Following:* `{usr['following']}`
*Hireable:* `{usr['hireable']}`
*Public Repos:* `{usr['public_repos']}`
*Public Gists:* `{usr['public_gists']}`
*Email:* `{usr['email']}`
*Company:* `{usr['company']}`
*Website:* `{usr['blog']}`
*Last updated:* `{usr['updated_at']}`
*Account created at:* `{usr['created_at']}`
""")

        
    else:
    
        reply_text = "User not found. Make sure you entered valid username!"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)


__help__ = """
 - /git:{GitHub username} Returns info about a GitHub user or organization.
"""



github_handle = DisableAbleCommandHandler("git", github)

dispatcher.add_handler(github_handle)

__mod_name__ = "Github"
__command_list__ = ["git"]
__handlers__ = [
    github_handle
]
