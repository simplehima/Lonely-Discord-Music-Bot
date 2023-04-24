import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
from collections import deque

load_dotenv()

TOKEN = os.getenv('TOKEN')
MUSIC_DIR = os.getenv('MUSIC_DIR')
VC_NAME = os.getenv('VC_NAME')
TXT_CHANNEL_ID = int(os.getenv('TXT_CHANNEL_ID'))

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

music_queue = deque()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return # Ignore updates caused by the bot itself
    if before.channel != after.channel:
        if after.channel is not None and after.channel.name == VC_NAME:
            voice = discord.utils.get(bot.voice_clients, guild=after.channel.guild)
            if voice and voice.is_connected():
                await voice.move_to(after.channel)
            else:
                voice = await after.channel.connect()
            await bot.get_channel(TXT_CHANNEL_ID).send(f"{member.mention} is feeling lonely and joined {VC_NAME}.")
            while len(music_queue) > 0 or any(m.voice != None and m.voice.channel == voice.channel for m in voice.guild.members):
                if len(music_queue) == 0:
                    for file in os.listdir(MUSIC_DIR):
                        if file.endswith(".mp3"):
                            music_queue.append(os.path.join(MUSIC_DIR, file))
                file = music_queue.popleft()
                voice.play(discord.FFmpegPCMAudio(file))
                while voice.is_playing():
                    await asyncio.sleep(1)
            if len(voice.channel.members) == 1:
                await voice.disconnect()
                music_queue.clear()
            else:
                await bot.get_channel(TXT_CHANNEL_ID).send(f"I am leaving 🥺・Lonely People.")
        elif before.channel is not None and before.channel.name == VC_NAME:
            if len(before.channel.members) == 1:
                voice = discord.utils.get(bot.voice_clients, guild=before.channel.guild)
                if voice and voice.is_connected():
                    await voice.disconnect()
                    music_queue.clear()
                await bot.get_channel(TXT_CHANNEL_ID).send(f"{member.mention} i hope that you left happy or better 💕❤.")
            else:
                await bot.get_channel(TXT_CHANNEL_ID).send(f"{member.mention} left {VC_NAME}.")
                
bot.run(TOKEN)
