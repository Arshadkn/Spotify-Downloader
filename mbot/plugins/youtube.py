"""MIT License

Copyright (c) 2022 Daniel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from os import mkdir
from random import randint
from mbot import AUTH_CHATS, LOG_GROUP, LOGGER, Mbot
from pyrogram import filters
from mbot.utils.ytdl import getIds,ytdl_down,audio_opt,thumb_down
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Mbot.on_message(filters.regex(r'(https?://)?.*you[^\s]+') | filters.command(["yt","ytd","ytmusic"]) & filters.regex(r'https?://.*you[^\s]+') & filters.chat(AUTH_CHATS))
async def _(_,message):
    m = await message.reply_text("<code> ✨ Fetching... </code>")
    link = message.matches[0].group(0)
    if link in [
        "https://youtube.com/",
        "https://youtube.com",
        "https://youtu.be/",
        "https://youtu.be",
    ]:

        return await m.edit_text("Please send a valid playlist or video link.")
    elif "channel" in link or "/c/" in link:
        return await m.edit_text("**Channel** Download Not Available. ")
    try:
        ids = await getIds(message.matches[0].group(0))
        videoInPlaylist = len(ids)
        randomdir = "/tmp/"+str(randint(1,100000000))
        mkdir(randomdir)
        for id in ids:
            fileLink = await ytdl_down(audio_opt(randomdir,id[2]),id[0])
            thumnail = await thumb_down(id[0])
            AForCopy = await message.reply_audio(fileLink,caption=f"[{id[3]}](https://youtu.be/{id[0]}) - {id[2]}",title=id[3].replace("_"," "),performer=id[2],thumb=thumnail,duration=id[4])
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("✨ Send - Personally ✨", callback_data=f'sendpm')
                    ]
                ]
            ),
            reply_to_message_id=message.message_id

        
        await m.delete()
    except Exception as e:
        LOGGER.error(e)
        await m.edit_text(e)

@Client.on_callback_query(filters.regex(r"^sendpm"))
async def callback_handler(client, query):
    data = query.data
    sng = data.split("#")[1]
    audio_file = AUDIO[sng]["audio_file"]  
    duration = AUDIO[sng]["duration"]
    title = AUDIO[sng]["title"]    
    link = AUDIO[sng]["link"]
    performer = f"[@AnnabenbotZ]"
    thumb_name = AUDIO[sng]["thumb_name"]
    rep = f'<a>{title}</a>\n\n❍ <b>Duration:</b> <code>{duration}</code>\n❍ <b>Uploaded By:</b> <a href="https://t.me/Edit_Repo">BenbotZ</a>\n<b>❍ Source:</b> <a href="{link}">Click Here</a>'  
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        user_id = query.from_user.id        
        await client.send_audio(user_id, audio_file, caption=rep, parse_mode='HTML', title=title, duration=dur, performer=performer, thumb=thumb_name, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ɢʀᴏᴜᴘ ✨🌟", url="https://t.me/+BzleUoO-duFmODRl")]]))
        await query.answer("Audio Send Successfully", show_alert=True)
    except ChatWriteForbidden:
        print("Cannot send a message to this user.")     
        await query.answer("Start The Bot!", show_alert=True)

    
            
