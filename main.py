import os
import discord

token = os.getenv("TOKEN")
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Ulogovan kao {client.user}")
    channel = client.get_channel(844879816196882462)
    if channel and not client.voice_clients:
        vc = await channel.connect()
        url = "http://stream.radiostanica.com/live"
        vc.play(discord.FFmpegPCMAudio(url))

client.run(token)