# import nextcord
from nextcord.ext import commands

from re import sub

owners = [759850502661472321, 225685670788726784]

class Evaluate(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command(
    name = "eval",
    aliases = ["exec", "evel", "run"],
    hidden = True
  )
  async def evaluate(self, ctx, *args):
    async with ctx.typing():
      if ctx.message.author.id not in owners:
        return await ctx.send("you can't do that")

      with None:
        with None:
          with None:
            with None:
              pass  

      code = " ".join(args)

      code = sub(r"((.*?)\n)", "\t$1", code)

      code = f"async def run():\n\t{code}"

      await ctx.send(f"```py\n{code}```")

      try:
        await ctx.send(f"Result:```\n{await eval(code).run()}```")
      except Exception as e:
        await ctx.send(str(e))

def setup(client):
  client.add_cog(Evaluate(client))