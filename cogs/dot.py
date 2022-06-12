import nextcord
from nextcord.ext import commands
icon = "https://cdn.discordapp.com/avatars/875328150165413918/4929f1614bfb400508e644e90b2b4555.png?size=256"
author = "Owll"
footer = "luv ya!"

class Dot(commands.Cog, description="dootle ville (https://discord.gg/mdghWS8Smt)"):
  def __init__(self, client):
    self.client = client

  @commands.command(
    help = "find ppl with the same prefix",
    name = "finddot",
    aliases = [
      "findprefix",
      "finduserswithprefix"
    ]
  )
  async def find_dot(self, ctx, *args):
    if not args: args = ["."]

    async with ctx.typing():
      prefix = " ".join(args)

      dots = []

      for member in ctx.guild.members:
        if not member.nick: member.nick = member.name

        if member.nick.startswith(prefix):
          dots.append(f"{member.name}#{member.discriminator}")

      if dots:
        amount = len(dots)

        plural = amount > 1
        
        if not plural:
          message = f"{amount} user with prefix \"{prefix}\" is in this server"
        else:
          message = f"{amount} users with prefix \"{prefix}\" are in this server"

        await ctx.send(message)
          
        await ctx.send(
          embed = nextcord.Embed(
            title = f"All the \"{prefix}\"s",
            description = "\n".join(dots),
            color = ctx.author.color
          )
        )
      else: 
        message = f"No users with prefix \"{prefix}\" found"

        await ctx.send(message)

  @commands.has_permissions(manage_nicknames=True)
  @commands.command()
  async def undot(self, ctx):
    async with ctx.typing():

      for member in ctx.guild.members:
        nick = member.name
        
        try:
          await member.edit(nick = nick)
        except:
          pass
          
      await ctx.send(f"unprefixed everyone")

  @commands.command(
    help = "prefix everyone in the server",
    aliases = ["prefix_all"]
  )
  @commands.has_permissions(manage_nicknames=True)
  async def dot(self, ctx, *args):
    if not args: args = ["."]

    async with ctx.typing():
      prefix = " ".join(args)

      for member in ctx.guild.members:
        nick = f"{prefix} but {member.name}"
        try:
          await member.edit(nick=nick)
        except:
          pass
          
      await ctx.send(f"prefixed everyone with {prefix}")

  @commands.command(help="why dot??")
  async def whydot(self, ctx):
    async with ctx.typing():
      em = nextcord.Embed(title="why dot???", description="in order to praise [dottle ville](https://discord.gg/mdghWS8Smt)", color = ctx.author.color)
      em.set_author(name = author, icon_url = icon)
      em.set_footer(text = footer)
      await ctx.send(embed = em)

def setup(client):
  client.add_cog(Dot(client))