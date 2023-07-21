import discord
from discord.ext import commands

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # on_ready() is a special function that is called when the bot is ready
        print('character cog is ready.')



    @commands.command(name='character')
    async def character(self, ctx, action: str = None, name: str = None, *, data_list: str = None):
        """Sets up a character sheet"""
        if action == 'new':
            await self.new_character(ctx, name, data_list)
        elif action == 'delete':
            await self.delete_character(ctx, name)
        elif action == 'list':
            await self.list_characters(ctx)
        elif action == 'set':
            await self.set_character(ctx, name, data_list)
        else:
            await self.get_character(ctx, action)

    async def new_character(self, ctx, name, data_list):
        pass

    async def delete_character(self, ctx, name):
        pass

    async def list_characters(self, ctx):
        pass

    async def set_character(self, ctx, name, data_list):
        pass

    async def get_character(self, ctx, name):
        pass



            

async def setup(bot):
    await bot.add_cog(Character(bot))