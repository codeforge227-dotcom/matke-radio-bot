import os
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp as youtube_dl  # nova zamena za youtube_dl
import asyncio

TOKEN = os.getenv("TOKEN")
VOICE_CHANNEL_ID = 1193137115387678761

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

# Tvoj YouTube live radio link
MUSIC_URL = "https://www.youtube.com/live/8V5EWDtA474?si=saGuH_01iOB7juEw"

@client.event
async def on_ready():
    print(f"Ulogovan kao {client.user}")

    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel is None:
        print("Voice kanal nije pronađen!")
        return

    if not channel.guild.voice_client:
        vc = await channel.connect()
        print("Bot povezan u kanal. Pustam muziku...")

        # yt-dlp opcije
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extractaudio': True,
            'audioformat': "mp3",
        }

        # preuzimanje direktnog audio streama
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(MUSIC_URL, download=False)
            url2 = info['url']

        # pustanje muzike preko FFmpeg
        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        vc.play(FFmpegPCMAudio(url2, **ffmpeg_opts))
        print("Muzika se pušta...")

        # čekanje dok se muzika pušta
        while vc.is_playing():
            await asyncio.sleep(1)

client.run(TOKEN)