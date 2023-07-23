import discord
from discord.ext import commands
import db

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # on_ready() is a special function that is called when the bot is ready
        print('character cog is ready.')



    @commands.command(name='character')
    async def character(self, ctx, action:str= None, name: str = None, *, data_list: str = None):
        """Sets up a character sheet"""
        if action != 'new' and action != 'delete' and action != 'list' and action != 'set':
            name = action
            action = None
        if action == 'new':
            await self.new_character(ctx, name)
        elif action == 'delete':
            await self.delete_character(ctx, name)
        elif action == 'list':
            await self.list_characters(ctx)
        elif action == 'set':
            await self.set_character(ctx, name, data_list)
        elif action == None and name != None:
            await self.get_character(ctx, name)
        else:
            await ctx.reply(f'Wrong action!')

    async def new_character(self, ctx, name):
        try:
            print(f"{ctx.author.id}, {name}, {ctx.guild.id}")
            mes = db.new_character( name, ctx.author.name, str(ctx.guild.id))
            embed = discord.Embed(title=name, color=discord.Color.random())
            embed.add_field(name=mes, value="", inline=True)
            await ctx.reply(embed=embed)
        except:
            await ctx.reply("Character already exists or invalid data")

    async def delete_character(self, ctx, name):
        try:
            if name == "all":
                mes = db.delete_all_characters(ctx.author.name)
            mes = db.delete_character(ctx.author.id, name)
            embed = discord.Embed(title=name, color=discord.Color.random())
            embed.add_field(name=mes, value="", inline=True)
            await ctx.reply(embed=embed)
        except:
            await ctx.reply("Character not found")


    async def list_characters(self, ctx):
        try:
            mes = db.list_characters(ctx.author.name)
            embed = discord.Embed(title="Characters", color=discord.Color.random())
            for i in mes:
                embed.add_field(name=i[0], value="", inline=True)
            await ctx.reply(embed=embed)
        except:
            await ctx.reply("No characters found")

    async def set_character(self, ctx, name, data_list):
        try:
            mes = db.set_character( name, data_list)
            embed = discord.Embed(title=name, color=discord.Color.random())
            embed.add_field(name=mes, value="", inline=True)
            await ctx.reply(embed=embed)
        except:
            await ctx.reply("Character not found")

    async def get_character(self, ctx, name):
        try:
            mes = db.get_character(name)
            embed = discord.Embed(title=name, color=discord.Color.random())
            j = 0
            for i in mes:
                if j < 25:
                    j += 1
                    embed.add_field(name=i[0], value=i[1], inline=True)
                else:
                    j = 0
                    await ctx.reply(embed=embed)
                    embed = discord.Embed(title=name, color=discord.Color.random())
                    embed.add_field(name=i[0], value=i[1], inline=True)
            await ctx.reply(embed=embed)
        except:
            await ctx.reply("Character not found")


            

async def setup(bot):
    await bot.add_cog(Character(bot))