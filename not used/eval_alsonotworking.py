from time import time
from nextcord.ext import commands
from inspect import getsource
import os
import nextcord

class EvalC(commands.Cog):
  
  def __init__(self, client):
    self.client=client
    
    def resolve_variable(self, variable):
        if hasattr(variable, "__iter__"):
            var_length = len(list(variable))
            if (var_length > 100) and (not isinstance(variable, str)):
                return f"<a {type(variable).__name__} iterable with more than 100 values ({var_length})>"
            elif (not var_length):
                return f"<an empty {type(variable).__name__} iterable>"
        
        if (not variable) and (not isinstance(variable, bool)):
            return f"<an empty {type(variable).__name__} object>"
        return (variable if (len(f"{variable}") <= 1000) else f"<a long {type(variable).__name__} object with the length of {len(f'{variable}'):,}>")
    
    def prepare(self, string):
        arr = string.strip("```").replace("py\n", "").replace("python\n", "").split("\n")
        if not arr[::-1][0].replace(" ", "").startswith("return"):
            arr[len(arr) - 1] = "return " + arr[::-1][0]
        return "".join(f"\n\t{i}" for i in arr)
    
    @commands.command(hidden=True, aliases=['eval', 'exec', 'evel'])
    @commands.is_owner()
    async def evaluate(self, ctx, *, code: str):
        silent = ("-s" in code)
        
        code = self.prepare(code.replace("-s", ""))
        args = {
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
            "os": os,
            "suace": getsource,
            "imp": __import__
        }
        try:
            exec(f"async def func():{code}", args)
            a = time()
            response = await eval("func()", args)
            if silent or (response is None) or isinstance(response, nextcord.Message):
                del args, code
                return
            
            await ctx.send(f"```py\n{self.resolve_variable(response)}````{type(response).__name__} | {(time() - a) / 1000} ms`")
        except Exception as e:
            await ctx.send(f"Error occurred:```\n{type(e).__name__}: {str(e)}```")
        
        del args, code, silent
        
def setup(client):
  client.add_cog(EvalC(client))