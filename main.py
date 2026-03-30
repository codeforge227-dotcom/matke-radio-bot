import os
import discord
from discord import FFmpegOpusAudio
import asyncio

# Bot token iz Railway env var
TOKEN = os.getenv("TOKEN")

# ID voice kanala gde bot ulazi
VOICE_CHANNEL_ID = 1193137115387678761

# Direktan radio stream koji radi
RADIO_URL = "https://naxi128.streaming.rs:9152/;*.mp3"  # testiran, radi sa botom

# Kreiramo client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Ulogovan kao {client.user}")
    
    # Pronađi kanal
    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel is None:
        print("Voice kanal nije pronađen!")
        return

    # Ako bot još nije u kanalu
    if not client.voice_clients:
        vc = await channel.connect()
        print("Bot povezan u kanal. Pustam muziku...")

        # Opcije za reconnect da stream ne stane
        before_opts = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        audio_source = FFmpegOpusAudio(RADIO_URL, before_options=before_opts)

        vc.play(audio_source, after=lambda e: print("Stream završen", e))

        # Čuvamo petlju da bot ostane povezan i muzika se pušta
        while vc.is_playing():
            await asyncio.sleep(1)

# Start bota
client.run(TOKEN)