import discord
from discord.ext import commands
import random
import re
import sqlite3
import db

class roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # on_ready() is a special function that is called when the bot is ready
        print('Roll cog is ready.')



    @commands.command(name='roll')
    async def roll(self, ctx, *, message):
        """Rolls a dice with a specified number of sides"""
        print(message)
        id, mesg = message.split(' ', 1)
        if mesg == "strength" or mesg == "str" or mesg == "dexterity" or mesg == "dex" or mesg == "constitution" or mesg == "con" or mesg == "intelligence" or mesg == "int" or mesg == "wisdom" or mesg == "wis" or mesg == "charisma" or mesg == "cha":
            return await self.roll_stats(ctx, id, mesg)
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
    async def r(self, ctx, dice:str, *, modifier:str = ''):
        """Rolls a dice with a specified number of sides"""
        mesg = f'{dice}{modifier}'
        print(mesg)
        await self.roll(ctx, message=mesg)

    @commands.command(name='rollinit')
    async def rollinit(self, ctx, action: str, *, message:str = None):
        """Rolls the initiative for a specified number of players"""
        if action == 'add':
            await self.add_players(ctx, message)
        elif action == 'clear':
            await self.clear_players(ctx)
        elif action == 'list':
            await self.list_players(ctx)
        elif action == 'start':
            await self.roll_initiative(ctx)
        else:
            await ctx.reply(f'Wrong action!')


    async def roll_stats(self, ctx, ability):
        dice = 20
        modifier = 0
        print(ctx.author.name)
        name = ctx.author.name
        character_id = db.get_character_id(name)
        await ctx.send(f"Hello {name} {character_id} ! Rolling {ability}...")
        try:
            character_data = db.search_character(character_id)
        except:
            await ctx.reply(f'You have not created a character yet!')

        if character_data:
            if ability.lower() == "strength" or ability.lower() == "str":
                modifier = character_data[23]
            elif ability.lower() == "dexterity" or ability.lower() == "dex":
                modifier = character_data[24]
            elif ability.lower() == "constitution" or ability.lower() == "con":
                modifier = character_data[25]
            elif ability.lower() == "intelligence" or ability.lower() == "int":
                modifier = character_data[26]
            elif ability.lower() == "wisdom" or ability.lower() == "wis":
                modifier = character_data[27]
            elif ability.lower() == "charisma" or ability.lower() == "cha":
                modifier = character_data[28]
            print(modifier)
            roll_result = random.randint(1, dice)
            total = roll_result + modifier
            await ctx.send(f"Rolling 1d{dice} + {modifier}: {roll_result}\nTotal: {total}")
        else:
            await ctx.reply(f'You have not created a character yet!')


async def setup(bot):
    await bot.add_cog(roll(bot))