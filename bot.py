import discord
from discord.ext import commands
import asyncio
import os
from collections import deque

intents = discord.Intents.all()
intents.members = True

TOKEN = "YOUR BOT TOKEN"
MUSIC_DIR = "PATH/music" # Replace with your music directory path
VC_NAME = "VOICE CHANNEL NAME"
TXT_CHANNEL_ID = 123456789 # Replace with your text channel ID

bot = commands.Bot(command_prefix='!', intents=intents)

music_queue = deque()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return # Ignore updates caused by the bot itself
    global music_queue
    if before.channel != after.channel:
        if after.channel is not None and after.channel.name == VC_NAME:
            voice = await after.channel.connect()
            while len(music_queue) > 0 or any(m.voice != None and m.voice.channel == voice.channel for m in voice.guild.members):
                if len(music_queue) == 0:
                    for file in os.listdir(MUSIC_DIR):
                        if file.endswith(".mp3"):
                            music_queue.append(os.path.join(MUSIC_DIR, file))
                file = music_queue.popleft()
                voice.play(discord.FFmpegPCMAudio(file))
                while voice.is_playing():
                    await asyncio.sleep(1)
            await voice.disconnect()
            await bot.get_channel(TXT_CHANNEL_ID).send(f"{member.mention} is feeling lonely and joined {VC_NAME}.")
        elif before.channel is not None and before.channel.name == VC_NAME and len(before.channel.members) == 1:
            voice = discord.utils.get(bot.voice_clients, guild=before.channel.guild)
            if voice.is_connected():
                await voice.disconnect()
            await bot.get_channel(TXT_CHANNEL_ID).send(f"{member.mention} i hope that you left happy or better 💕❤.")
            music_queue = deque()

bot.run(TOKEN)
