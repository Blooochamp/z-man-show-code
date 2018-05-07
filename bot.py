import discord
from discord.ext import commands
import config

# this specifies what extensions to load when the bot starts up
startup_extensions = ["cogs.avatar", "cogs.verify"]

bot = commands.Bot(command_prefix=config.prefix)
owner = "252216078359330817"

@bot.event
async def on_ready():
    print ("Running!")
    print ("Username is: %s" % bot.user.name)
    print ("ID is: %s" % bot.user.id)
    print ("Prefix is: %s" % config.prefix)
    await bot.change_presence(game=discord.Game(type=0, name = "In testing | Prefix: " + config.prefix))

#---------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------
@bot.command(pass_context=True)
async def load(ctx, extension_name : str):
    """Loads an extension."""
    Author_id = ctx.message.author.id
    Channel = ctx.message.channel
    if Author_id == owner:
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await bot.send_message(Channel, "```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await bot.send_message(Channel, "{} loaded.".format(extension_name))

@bot.command(pass_context=True)
async def unload(ctx, extension_name : str):
    """Unloads an extension."""
    Author_id = ctx.message.author.id
    Channel = ctx.message.channel
    if Author_id == owner:
        bot.unload_extension(extension_name)
        await bot.send_message(Channel, "{} unloaded.".format(extension_name))

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

#---------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------

bot.run(config.token)
