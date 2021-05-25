# Simple lyrics module using tswift by @TheRealPhoenix

from tswift import Song

from telegram import Bot, Update, Message, Chat
from telegram.ext import run_async

from emilia import dispatcher
from emilia.modules.disable import DisableAbleCommandHandler
from emilia.modules.helper_funcs.alternate import send_message


@run_async
def lyrics(update, context):
    args = context.args
    msg = update.effective_message
    query = " ".join(args)
    song = ""
    if not query:
        msg.reply_text("You haven't specified which song to look for!")
        return
    else:
        song = Song.find_song(query)
        if song:
            if song.lyrics:
                reply = song.format()
            else:
                reply = "Couldn't find any lyrics for that song!"
        else:
            reply = "Song not found!"
        if len(reply) > 4090:
            with open("lyrics.txt", 'w') as f:
                f.write(f"{reply}\n\n\nOwO UwU OmO")
            with open("lyrics.txt", 'rb') as f:
                msg.reply_document(document=f,
                caption="Message length exceeded max limit! Sending as a text file.")
        else:
            msg.reply_text(reply)
                
        
                
__help__ = """
Want to get the lyrics of your favorite songs straight from the app? This module is perfect for that!
*Available commands:*
 - /lyrics <song>: returns the lyrics of that song.
 You can either enter just the song name or both the artist and song name.
"""





LYRICS_HANDLER = DisableAbleCommandHandler("lyrics", lyrics, pass_args=True)

dispatcher.add_handler(LYRICS_HANDLER)

__mod_name__ = "Songslyrics"
__command_list__ = ["lyrics"]
__handlers__ = [
    LYRICS_HANDLER
]
