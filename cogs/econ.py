import json
import nextcord
from nextcord.ext import commands

class Economy(commands.Cog):
  
  def __init__(self, client):
    self.client=client  

  async def open_account(self, user):
    users = await self.get_bank_data()

    if str(user.id) in users:
      return False
    else:
      users[str(user.id)]["wallet"] = 0
      users[str(user.id)]["bank"] = 100

    with open("bank.json", "w") as file:
      json.dump(users, file, indent=4)
    return True

  async def get_bank_data(self):
    with open("bank.json", "r") as file:
      users = json.load(file)

    return users

  async def update_bank(self, user, change=0, mode="wallet"):
    user = await self.get_bank_data()

    user[str(user.id)][mode] += change

    with open("bank.json", "w") as file:
      json.dump(user, file, indent=4)

    bal = [user[str(user.id)]["wallet"], user[str(user.id)]["bank"]]
    return bal

  @commands.command(help="check your balance", aliases=["bal"])
  async def balance(self, ctx):
      users = await self.get_bank_data()
      wallet_amount = users[str(ctx.author.id)]["wallet"]
      bank_amount = users[str(ctx.author.id)]["bank"]
      em=nextcord.Embed(title=f"{ctx.author.name}'s Balance", color= nextcord.Color.green())
      em.add_field(name="wallet", value=wallet_amount)
      em.add_field(name="bank", value=bank_amount)
      await ctx.send(embed=em)


def setup(client):
  client.add_cog(Economy(client))