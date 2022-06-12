import nextcord, json, os
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# from pretty_help import DefaultMenu, PrettyHelp

# menu = DefaultMenu(page_left=":up_vote:869793180718100500", page_right=":down_vote:869793180625801266", remove=":no:869793180151873607")

help_command = commands.DefaultHelpCommand(no_category="General")

# help_command = PrettyHelp(menu=menu, no_category="General")

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="owl.", intents=intents, help_command=help_command)

owners = json.loads(open("owners.json", "r").read())

@client.event
async def on_ready():
    print("owll is alive!")
    await client.change_presence(
        status=nextcord.Status.online,
        activity=nextcord.Game("in development, do not use | owl.help")
    )

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
        guild_amount = 0
      
        async for _ in client.fetch_guilds(): guild_amount += 1
        
        await ctx.send(f"I'm in {guild_amount} servers")


@client.command(hidden=True)
async def bot_in_o(ctx):
  async with ctx.typing():
    if ctx.message.author.id not in owners: return

    names = []
    guild_id = []
    async for guild in client.fetch_guilds(): names.append(guild.name)
    async for guild in client.fetch_guilds(): guild_id.append(guild.id)
    
    await ctx.send("\n".join(names) + " " + "\n".join(guild_id))

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

TOKEN = os.getenv("DISCORD_TOKEN")

client.run(TOKEN)
