import nextcord
from nextcord.ext import commands
from traceback import format_exception
import io
import textwrap
import contextlib
#from nextcord.ext.buttons import Paginator
import os

class Pag(nextcord.ui.Button):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except nextcord.HTTPException:
            pass


def clean_code(content):
    if content.startswith("```py") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content

def is_dev():
    def predicate(ctx):
        return ctx.message.author.id == 759850502661472321, 225685670788726784
    return commands.check(predicate)

class EvalCMD(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="eval", aliases=["exec", "evel", "run"], hidden=True)
    @is_dev()
    async def _eval(self, ctx, *, code):
      async with ctx.typing():
        code = clean_code(code)

        local_variables = {
            "nextcord": nextcord,
            "commands": commands,
            "client": self.client,
            "owl": self.client,
            "bot": self.client,
            "ctx": ctx,
            "send": ctx.send,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "self": self,
            "os": os
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )

                obj = await local_variables["func"]()
                result = str(stdout.getvalue())
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        if len(result) > 0:
            pager = Pag(
                timeout=100,
                entries=[result[i: i + 2000]
                         for i in range(0, len(result), 2000)],
                length=1,
                prefix="```py\n",
                suffix="```"
            )

            await pager.start(ctx)


def setup(client):
    client.add_cog(EvalCMD(client))