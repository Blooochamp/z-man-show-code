import discord
from discord.ext import commands

class Avatar:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def avatar(self, ctx, user : discord.User):
        url = user.avatar_url
        await self.bot.send_message(ctx.message.author, "%s" % url)
        await self.bot.send_message(ctx.message.channel, "%s" % url)


def setup(bot):
    bot.add_cog(Avatar(bot))
