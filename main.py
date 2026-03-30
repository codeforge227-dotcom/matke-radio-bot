import os
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

TOKEN = os.getenv("TOKEN")  # Token stavi u Railway Environment Variables
PREFIX = "!"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# FFmpeg opcije
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f"Ulogovan kao {bot.user}")

# Komanda za puštanje lokalnog MP3 ili HTTPS audio
@bot.command(name="play")
async def play(ctx, *, url_or_file: str):
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

    # Ako je URL HTTPS, FFmpeg može direktno da pusti
    # Ako je lokalni fajl, stavi putanju relativno projektu
    audio_source = FFmpegPCMAudio(url_or_file, **ffmpeg_options)
    vc.play(audio_source)

    await ctx.send(f"Pustam muziku 🎧: {url_or_file}")

# Komanda za stop / disconnect
@bot.command(name="stop")
async def stop(ctx):
    vc = ctx.guild.voice_client
    if vc and vc.is_connected():
        await vc.disconnect()
        await ctx.send("Bot je izašao iz glasovnog kanala.")
    else:
        await ctx.send("Bot nije povezan u kanal.")

bot.run(TOKEN)