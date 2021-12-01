from discord.ext import commands
import json

class Stats:
  xp = 0
  level = 0

class Level(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return
    
    with open("levels.json", "r") as file:
      levels = json.load(file)
    
    stats = levels[str(message.author.id)]
    if not stats:
      stats = Stats()
    

def setup(client):
  client.add_cog(Level(client))
