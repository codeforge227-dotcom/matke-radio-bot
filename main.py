import os
import discord

token = os.getenv("TOKEN")
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Ulogovan kao {client.user}")
    channel = client.get_channel(1193137115387678761)
    if channel and not client.voice_clients:
        vc = await channel.connect()
        # Direktan MP3 stream koji radi
        url = "https://stream.playradio.rs:8001/play.mp3"
        vc.play(discord.FFmpegPCMAudio(url))
        print("Pustam muziku...")

client.run(token)