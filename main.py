import os
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp

TOKEN = os.getenv("TOKEN")  # TOKEN mora biti u Environment Var na Railway
PREFIX = "!"

intents = discord.Intents.default()
intents.message_content = True  # da bot može čitati komande
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# FFmpeg opcije za reconnect (za dugotrajne streamove)
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f"Ulogovan kao {bot.user}")

@bot.command(name="play")
async def play(ctx, *, url: str):
    voice = ctx.author.voice
    if not voice:
        await ctx.send("Moraš biti u glasovnom kanalu da pustiš muziku!")
        return

    channel = voice.channel

    # Ako bot nije povezan, poveži ga
    if not ctx.guild.voice_client:
        await channel.connect()

    vc = ctx.guild.voice_client

    # Ako već svira nešto, zaustavi
    if vc.is_playing():
        vc.stop()

    # Preuzimanje direktnog audio URL‑a sa YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']

    source = FFmpegPCMAudio(audio_url, **ffmpeg_options)
    vc.play(source)

    await ctx.send(f"Pustam muziku 🎧: {url}")

@bot.command(name="stop")
async def stop(ctx):
    vc = ctx.guild.voice_client
    if vc and vc.is_connected():
        await vc.disconnect()
        await ctx.send("Bot je izašao iz glasovnog kanala.")
    else:
        await ctx.send("Bot nije povezan u kanal.")

bot.run(TOKEN)