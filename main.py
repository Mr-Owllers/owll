import nextcord
import json
import os
import datetime, time
from webserver import keep_alive
from nextcord.ext import commands

help_command = commands.DefaultHelpCommand(no_category="Other Commands")

intents = nextcord.Intents.default()
intents.members = True

def get_prefix(client, message):
    with open("prefix.json", "r") as file:
        prefixes = json.load(file)

    guild_id = str(message.guild.id)
    if guild_id in prefixes:
        prefix = prefixes[guild_id]
    else:
        prefix = "owl."  # Prefix defaults to this if none is set for the server
    return prefix

client = commands.AutoShardedBot(
  shard_count = 11,
  command_prefix = get_prefix,
  help_command = help_command,
  intents = intents
)

owners = [759850502661472321, 225685670788726784]
start_time = time.time()


@client.event
async def on_ready():
    print("owll is alive!")
    await client.change_presence(
          status=nextcord.Status.online,
          activity=nextcord.Game(f"eating mice | 11 shards | in {len(client.guilds)} servers | owl.help"))


@client.command(help="change the prefix", aliases=["pre", "setprefix", "prfx"])
@commands.has_permissions(administrator=True)
async def prefix(ctx, *args):
    async with ctx.typing():
        if len(args) < 1:
            await ctx.send("No prefix specified!")
            return

        prefix = args[0]

        if len(prefix) > 6:
            await ctx.send(
                "Prefix has more characters than the character limit! (6)")
            return

        with open("prefix.json", "r") as file:
            prefixes = json.load(file)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefix.json", "w") as file:
            file.write(json.dumps(prefixes, indent=4))

        await ctx.send(f"Prefix set to {prefix}")
        new_nickname = f"[{prefix}] owll"
        await ctx.guild.get_member(client.user.id).edit(nick=new_nickname)
        await ctx.send(
            f"Changed nickname to {new_nickname}")

@client.command(hidden=True)
async def load(ctx, extension):
    async with ctx.typing():
        if ctx.message.author.id not in owners:
            return await ctx.send("you can't do that")
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} loaded")


@client.command(hidden=True)
async def unload(ctx, extension):
    async with ctx.typing():
        if ctx.message.author.id not in owners:
            return await ctx.send("you can't do that")
        else:
            client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} unloaded")


@client.command(hidden=True)
async def reload(ctx, extension):
    async with ctx.typing():
        if ctx.message.author.id not in owners:
            return await ctx.send("you can't do that")
        else:
            client.reload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} reloaded")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.command(help="Shows the ping/latency of the bot in miliseconds.",
                brief="Shows ping")
async def ping(ctx):
    async with ctx.typing():
        await ctx.send(f"🏓 Pong!\n{round(client.latency * 1000)}ms")


@client.command(help="see how many servers the bot is in")
async def bot_in(ctx):
    async with ctx.typing():
        await ctx.send(f"I'm in {len(client.guilds)} servers")


@client.command(hidden=True)
async def bot_in_o(ctx):
    async with ctx.typing():
        if ctx.message.author.id not in owners:
            return
        await ctx.send("\n".join(guild.name for guild in client.guilds))

@client.command(help="see the bot uptime", aliases=["up", "uptimebot", "botuptime", "uptimerobot"])
async def uptime(ctx):
  async with ctx.typing():
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed = nextcord.Embed(title="Uptime", colour=ctx.message.author.top_role.colour)
    embed.add_field(name="hazy view", value=text)
    embed.add_field(name="detailed view", value="click [here](https://stats.uptimerobot.com/MKAjKH2k8q/788949943)")
    embed.set_footer(text="Note- The hazy view restarts when the bot get restarted")
    try:
        await ctx.send(embed=embed)
    except nextcord.HTTPException:
        await ctx.send(f"Current uptime\nhazy view: {text}\ndetailed view: https://stats.uptimerobot.com/MKAjKH2k8q/788949943")



#Error Handler by MustafaTheCoder
@client.event  #Making an event for out error handler.
async def on_command_error(
    ctx, error
):  #This is what we use "in_command_error" for to check if there is any error while running the cmds.
    if isinstance(error, commands.CommandOnCooldown
                  ):  #The first error which is if your command is on cooldown.
        msg = "Still on cooldown, please try again in {:.2f}s.".format(  #this is the error msg that will be shown when there is an error.
            error.retry_after)
        em13 = nextcord.Embed(
            title="**Error Block**",  #making an embed for our error.
            color=nextcord.Color.red())
        em13.add_field(name="__Slowmode Error:__", value=msg)
        await ctx.send(embed=em13
                       )  #finally sending the "CommandOnCooldown error".
    if isinstance(
            error, commands.MissingRequiredArgument
    ):  #this is the second error which is missing required arguments.
        msg2 = "Please enter all the required arguments!"  #if you have an ban command and you have not mentioned a user then this error will be thrown.
        em14 = nextcord.Embed(title = f"**{msg2}**")
        em14.add_field(name = "__Expected Arguments:__", value=msg2)
        await ctx.send(embed = em14)
    if isinstance(
            error, commands.MissingPermissions
    ):  #missing permissions like with the ban command if you dont have ban_members perm.
        msg3 = "You are missing permissions to use that command!"
        em15 = nextcord.Embed(title = "**Missing permissions**")
        
        em15.add_field(name = "__Missing Permissions:__", value=msg3)
        await ctx.send(embed = em15)
    if isinstance(
            error, commands.CommandNotFound
    ):  #this error is thrown when the thing you type with the bot"s prefix is not a command.
        msg4 = "No command found!"
        em16 = nextcord.Embed(title = f"**{msg4}**")
        em16.add_field(name = "__Command Not Found:__", value=msg4)
        await ctx.send(embed = em16)
    if isinstance( 
            error, commands.CommandInvokeError
    ):  #this error is thrown when the argument is not valid. #this part is coded by me
        msg5 = "Invocation error"
        em17 = nextcord.Embed(title = msg5)
        em17.add_field(name = "__Invocation error__", value = str(error))
        await ctx.send(embed = em17)

keep_alive()
TOKEN = os.getenv("DISCORD_TOKEN")

client.run(TOKEN)
