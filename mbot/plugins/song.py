
from __future__ import unicode_literals



import asyncio

import math

import os

import time

from random import randint

from urllib.parse import urlparse

import aiofiles

import aiohttp

import requests

import wget

import yt_dlp

from pyrogram import Client, filters

from pyrogram.errors import FloodWait, MessageNotModified

from pyrogram.types import Message

from youtube_search import YoutubeSearch

from yt_dlp import YoutubeDL
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ydl_opts = {

    'format': 'best',

    'keepvideo': True,

    'prefer_ffmpeg': False,

    'geo_bypass': True,

    'outtmpl': '%(title)s.%(ext)s',

    'quite': True

}

ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"

@Client.on_message(filters.command(["song", "mp3"]))

def song(_, message):

    query = " ".join(message.command[1:])

    ydl_ops = {"format": "bestaudio[ext=m4a]"}

    try:

        results = YoutubeSearch(query, max_results=1).to_dict()

        link = f"https://youtube.com{results[0]['url_suffix']}"

        title = results[0]["title"][:40]

        duration = results[0]["duration"]

        channel = results[0]["channel"]

        thumbnail = results[0]["thumbnails"][0]

        thumb_name = f"{title}.jpg"

        thumb = requests.get(thumbnail, allow_redirects=True)

        open(thumb_name, "wb").write(thumb.content)

        duration = results[0]["duration"]

    except Exception as e:

        message.reply_text(f"👋Hey  {message.from_user.first_name}  its very easy to request music here\n\nRequest - Examples:\n➲ /song Srivalli Malayalam\n➲ /song Darshana hridayam\n➲ /song Alone - Marshmallow\n➲ /song Aathmavile anandhame\n➲ /song Parayathe vannnen\n\nHope You Understood 🙂\n🍒")

        print(str(e))

        return

    try:

        with yt_dlp.YoutubeDL(ydl_ops) as ydl:

            info_dict = ydl.extract_info(link, download=False)

            audio_file = ydl.prepare_filename(info_dict)

            ydl.process_info(info_dict)

        rep = f"⍟ <code> {title} </code>\n⍟Dᴜʀᴀᴛɪᴏɴ:{duration}\n⍟ Sᴏɴɢ Lɪɴᴋ:<a href={link}>Cʟɪᴄᴋ Hᴇʀᴇ </a>\n⍟ Uᴘʟᴏᴀᴅᴇᴅ Bʏ:<a href=https://t.me/kerala_music_group_2>Kᴇʀᴀʟᴀ Mᴜsɪᴄ</a>"
        
        
                        
                    

        secmul, dur, dur_arr = 1, 0, duration.split(":")

        for i in range(len(dur_arr) - 1, -1, -1):

            dur += int(float(dur_arr[i])) * secmul

            secmul *= 60



    

        m=message.reply_text("<code> ✨ Fetching... </code>")

        message.reply_audio(

            audio_file,

            caption=rep,

            thumb=thumb_name,

            title=title,

            duration=dur,

        )

        m.delete()

    except Exception as e:

        message.reply_text("#ERROR, ᴛʜᴇʀᴇ ɪs sᴏᴍᴇ ᴇʀʀᴏʀ. ᴘʟs ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ...")

        print(e)

    try:

        os.remove(audio_file)

        os.remove(thumb_name)

    except Exception as e:

        print(e)
