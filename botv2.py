import asyncio
import discord
import os
from discord.ext import commands
import key as key

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
native_thumbnail = 'https://img.freepik.com/free-vector/glitch-error-404-page_23-2148105404.jpg?w=2000'

def run_discord_bot():

    async def load():#
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded {filename}')

    async def main():
        await load()
        print('Bot is ready')
        await bot.start(key.key())
        

    asyncio.run(main())
