import discord
from discord.ext import commands
import asyncio
import os
from collections import deque

intents = discord.Intents.all()
intents.members = True

TOKEN = "TOKEN HERE"
MUSIC_DIR = "PATH/music" # Replace with your music directory path
VC_NAME = "VOICE CHANNEL NAME"
TXT_CHANNEL_ID = TEXT CHANNEL ID# Replace with your text channel ID

bot = commands.Bot(command_prefix='!', intents=intents)

music_queue = deque()
voice_client = None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_voice_state_update(member, before, after):
    global music_queue, voice_client
    if before.channel != after.channel:
        if after.channel is not None and after.channel.name == VC_NAME:
            if voice_client is None:
                voice_client = await after.channel.connect()
                await bot.get_channel(TXT_CHANNEL_ID).send(f"{member.mention} is feeling lonely and joined {VC_NAME}.")
            while len(music_queue) > 0 or any(m.voice != None and m.voice.channel == voice_client.channel for m in voice_client.guild.members):
                if len(music_queue) == 0:
                    for file in os.listdir(MUSIC_DIR):
                        if file.endswith(".mp3"):
                            music_queue.append(os.path.join(MUSIC_DIR, file))
                file = music_queue.popleft()
                voice_client.play(discord.FFmpegPCMAudio(file))
                while voice_client.is_playing():
                    await asyncio.sleep(1)
            await asyncio.sleep(1)
            if len(voice_client.channel.members) == 1:
                await voice_client.disconnect()
                voice_client = None
                await bot.get_channel(TXT_CHANNEL_ID).send(f"I'm leaving {VC_NAME} since I'm alone.")
        elif before.channel is not None and before.channel.name == VC_NAME and len(before.channel.members) == 1:
            await bot.get_channel(TXT_CHANNEL_ID).send(f"{member.mention}  i hope that you left happy or better 💕❤.")
            music_queue = deque()
            await asyncio.sleep(1)
            if len(voice_client.channel.members) == 1:
                await voice_client.disconnect()
                voice_client = None

bot.run(TOKEN)
