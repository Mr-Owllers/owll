import nextcord
from nextcord.ext import commands
import aiohttp

icon = "https://cdn.discordapp.com/avatars/875328150165413918/4929f1614bfb400508e644e90b2b4555.png?size=256"
author = "Owll"
footer = "luv ya!"
hug = ["https://c.tenor.com/bFZKN-tlQP4AAAAC/love-you-my-best-friend.gif", "https://c.tenor.com/KlkE8vt8gOIAAAAM/love-is-the-answer-to-everything-hug.gif", "https://c.tenor.com/OkpKo5iPu-8AAAAM/huge-hug.gif", "https://c.tenor.com/BW8ZMOHHrgMAAAAM/friends-joey-tribbiani.gif", "https://c.tenor.com/ut3cq1GezaoAAAAM/hug-hugs.gif", "https://media1.tenor.com/images/8ac5ada8524d767b77d3d54239773e48/tenor.gif?itemid=16334628", "https://c.tenor.com/0gz0aKX9vcQAAAAC/owl-hug-sweet.gif"]
import random

class general(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Invite me!", aliases=["inv", "i"])
    async def invite(self, ctx):
      async with ctx.typing():
        embed = nextcord.Embed( 
            title="Invite me!",
            description="Invite me by pressing [here](https://dsc/owll)",
            color=ctx.author.color
        )
        embed.set_author(name = author, icon_url = icon)
        embed.set_footer(text = footer)

        await ctx.message.reply(embed=embed)

    @commands.command(help="get a link to the support server", aliases=["xtrahelp", "extrahelp", "helpme"])
    async def support(self, ctx):
      async with ctx.typing():
        embed = nextcord.Embed(
            title="Support server",
            description="You may join our [support server](https://dsc.gg/goldwilde) :D",
            color=ctx.author.color
        )
        embed.set_author(name = author, icon_url = icon)
        embed.set_footer(text = footer)

        await ctx.message.reply(embed=embed)

    @commands.command(help="hug someone!", aliases=["hog"])
    async def hug(self, ctx, members: commands.Greedy[nextcord.Member]):
        async with aiohttp.ClientSession() as cs:
          async with ctx.typing():
            async with cs.get("https://some-random-api.ml/animu/hug") as r:
                js = await r.json()
                
                if not members:
                    return await ctx.send("Please specify someone to hug.")

                if ctx.author in members:
                  return await ctx.send("do you... need a hug?")
                

                e = nextcord.Embed(color=0xff0000, description=f"**{ctx.author.name}** hugs "+ "**" + '**, **'.join(x.display_name for x in members) + "**! Awwww!")
                
                manual = hug
                manual.append(js['link'])
                image = random.choice(manual)

                e.set_image(url=image)
                await ctx.send(embed=e)

def setup(client):
    client.add_cog(general(client))