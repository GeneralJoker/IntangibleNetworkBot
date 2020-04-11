import discord
from discord.ext import commands

from cogs.utils.checks import is_bot_owner_check

import git

# AUTHORED BY : GreatGeneral#6688

# @commands.Cog.listener() = @client.event

class SpamProtection(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # THIS IS AN EVENT FOR SPAM
    @commands.Cog.listener()
    async def on_message(self, message):
        messages = {}
        count = 1
        if message.author == commands.Cog.user:
            return
        if '' in message.content:
            messages[message.content] = message.author, count
            if message.content == messages.get(message.author.id, {}).get('message'):
                messages[message.author.id]['count'] += 1
            else:
                messages[message.author.id] = {
                    'message': message.content,
                    'count': 1
                }
            if messages[message.author.id]['count'] >= 3:
                await message.delete()
                await message.channel.send(f'{message.author.mention} has spammed!')
        await commands.Cog.process_commands(message)

    @commands.command(name='softban')
    async def soft_ban(self, ctx, member : discord.Member):
        if not member:
            return await ctx.send("you must specify a user")

        try:
            await member.ban(reason=None)
            await member.unban()
            await ctx.send(f'{member.mention} has been banned & unbanned')
        except discord.Forbidden:
            return await ctx.send("forbidden")


def setup(bot):
    bot.add_cog(SpamProtection(bot))