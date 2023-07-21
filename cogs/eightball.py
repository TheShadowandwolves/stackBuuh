import discord
from discord.ext import commands
import random

class eightball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # on_ready() is a special function that is called when the bot is ready
        print('8ball cog is ready.')

    @commands.command(name='test', help='Returns an answer of type yes/no back.')
    async def eightball(self, ctx, *, question):
        responses = ["As I see it, yes.", "Ask again later.", "Detter not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
                     "Don't count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "my reply is no.", "ny sources say no.",
                    "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "signs point to yes.", "very doubtful.", "Without a doubt.",
                    "yes.", "yes - definitely.", "You may rely on it."]
        try:
            await ctx.reply(f"**Question: ** {question}\n**Answers:** {random.choice(responses)}")
        except:
            await ctx.reply("No question has been asked")
        
async def setup(bot):
    await bot.add_cog(eightball(bot))