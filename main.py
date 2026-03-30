import os
import discord
from discord import FFmpegPCMAudio
import asyncio

# Tvoj bot token iz Railway env var
token = os.getenv("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# ID voice kanala gde će bot ući
VOICE_CHANNEL_ID = 1193137115387678761

# Direktan stream URL koji radi
RADIO_URL = "https://stream.playradio.rs:8001/play.mp3"

@client.event
async def on_ready():
    print(f"Ulogovan kao {client.user}")
    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel and not client.voice_clients:
        vc = await channel.connect()
        print("Povezan u kanal. Pustam muziku...")

        # Pusti radio stream
        vc.play(FFmpegPCMAudio(RADIO_URL), after=lambda e: print("Stream završen", e))

        # Održava vezu dok se muzika pušta
        while vc.is_playing():
            await asyncio.sleep(1)

client.run(token)