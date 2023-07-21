import discord
from discord.ext import commands
import os
import sys


def restart_bot(): 
    os.execv(sys.executable, ['python'] + sys.argv)

class server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): # on_ready() is a special function that is called when the bot is ready
        print('server cog is ready.')


    @commands.has_permissions(administrator=True)
    @commands.command(name='server')
    async def ping(self, ctx, action: str = None):
        """Server commands"""
        if action == 'restart':
            await self.restart(ctx)
        elif action == None:
            await self.info(ctx)
        elif action == 'members':
            await self.members(ctx)
        else:
            await ctx.reply(f'Wrong action!')

    async def restart(self, ctx):
        """Restarts the bot"""
        await ctx.send("Restarting bot")
        restart_bot()

    async def members(self, ctx):
        """Lists all members in the server"""
        guild = ctx.guild
        members = guild.members
        member_list = []
        for member in members:
            member_list.append(member.name)
        await ctx.message.delete()
        await ctx.send(f"{member_list}")

    async def info(self, ctx):
        """Lists server information"""
        guild = ctx.guild

        # Get general server information
        server_name = guild.name
        server_id = guild.id
        server_owner = guild.owner.name
        server_member_count = guild.member_count

        roles = [role.name for role in guild.roles[1:]]  # Exclude @everyone role

        # Create an embedded message
        embed = discord.Embed(title="Server Information", color=discord.Color.green())
        embed.add_field(name="Server Name", value=server_name, inline=True)
        embed.add_field(name="Server ID", value=server_id, inline=True)
        embed.add_field(name="Server Owner", value=server_owner, inline=True)
        embed.add_field(name="Server Roles", value=", ".join(roles) if roles else "No Roles", inline=True)
        embed.add_field(name="Member Count", value=server_member_count, inline=True)
        await ctx.message.delete()
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(server(bot))