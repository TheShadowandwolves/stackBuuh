import discord
from discord.ext import commands
# import tracemalloc
# tracemalloc.start()

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # on_ready() is a special function that is called when the bot is ready
        print('Ping cog is ready.')



    @commands.command(name='ping', help='Returns the bot\'s latency.')
    async def ping(self, ctx, time: str = None):
        if time == 'sec':
            await self.ping_sec(ctx)
        else:
            await self.ping_ms(ctx)

    async def ping_sec(self, ctx):
        await ctx.reply(f'Pong! {float(self.bot.latency)}s')

    async def ping_ms(self, ctx):
        await ctx.reply(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def pong(self, ctx, user: discord.User = None, private_message: str = False):
        """Ping everyone in the server or a specific user"""
        if user is not None:
            # Send a private message to the specified user
            await ctx.message.delete()
            await user.send(f"You've been pinged by {ctx.author.name} in {ctx.guild.name}! with the message: {private_message}")
        else:
            # Send a private message to everyone in the server
            for member in ctx.guild.members:
                # Make sure not to send a message to the bot itself
                if member != commands.user:
                    await ctx.message.delete()
                    await member.send(f"You've been pinged by {ctx.author.name} in {ctx.guild.name}! with the message: {private_message}")
            
            

async def setup(bot):
    await bot.add_cog(ping(bot))