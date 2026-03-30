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
        url = "https://streaming.hitfm.rs/hit.mp3"
        vc.play(discord.FFmpegPCMAudio(url))

client.run(token)