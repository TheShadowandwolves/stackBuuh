import discord
from discord.ext import commands
import random
import re

class roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # on_ready() is a special function that is called when the bot is ready
        print('Roll cog is ready.')



    @commands.command(name='roll')
    async def roll(self, ctx, *, message:str):
        """Rolls a dice with a specified number of sides"""
        #print(message)
        try:
            #_, command = message.split(' ', 1)
            command = message.replace(' ', '')  # Remove any spaces in the command

            match = re.match(r"(\d*)d(\d+)([+-]\d+)?", command)
            if match:
                rolls = int(match.group(1)) if match.group(1) else 1
                limit = int(match.group(2))
                modifier = int(match.group(3)) if match.group(3) else 0

                results = [random.randint(1, limit) for _ in range(rolls)]
                total = sum(results) + modifier

                await ctx.send(f"Rolling {rolls}d{limit} + {modifier}: {results}\nTotal: {total}")
                
            else:
                raise ValueError
        except (ValueError, ZeroDivisionError):
            await ctx.send('Invalid command. Please use the format `!r NdM +/- X` or a valid mathematical expression.')

    @commands.command(name='r')
    async def r(self, ctx, *, message:str):
        """Rolls a dice with a specified number of sides"""
        self.roll(ctx, message)

async def setup(bot):
    await bot.add_cog(roll(bot))