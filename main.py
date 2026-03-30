import os
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio

# Tvoj bot token iz Railway env var
TOKEN = os.getenv("TOKEN")

# ID voice kanala gde bot ulazi
VOICE_CHANNEL_ID = 1193137115387678761

# Direktan TOP FM stream (128 kbps)
RADIO_URL = "https://topfm128ssl.streaming.rs:9282/;stream.mp3"

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Ulogovan kao {client.user}")

    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel is None:
        print("Voice kanal nije pronađen!")
        return

    if not channel.guild.voice_client:
        vc = await channel.connect()
        print("Povezan u kanal. Pustam TOP FM...")

        # FFmpeg opcije da stream ne stane
        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        vc.play(FFmpegPCMAudio(RADIO_URL, **ffmpeg_opts))
        print("Muzika se pušta...")

        # Čuvamo petlju dok muzika svira
        while vc.is_playing():
            await asyncio.sleep(1)

client.run(TOKEN)