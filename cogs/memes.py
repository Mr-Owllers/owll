import praw
import os
import nextcord

SECRET = os.environ['SECRET']

ID = os.environ['ID']

reddit = praw.Reddit(client_id= ID, client_secret= SECRET, user_agent= "owllAPI", check_for_async=False)

import random
from nextcord.ext import commands

class Memes(commands.Cog):
  
  def __init__(self, client):
    self.client=client  

  @commands.command(help="search memes from reddit")
  async def reddit(self, ctx, *, subred="memes"):
    async with ctx.typing():
      sub = reddit.subreddit(subred)
      all_subs = []

      top = sub.top(limit = 50)

      for submission in top:
        all_subs.append(submission)

      random_sub = random.choice(all_subs)

      name = random_sub.title
      url = random_sub.url
      op = reddit.config.reddit_url + submission.permalink

      em = nextcord.Embed(title = name, url = op)
      em.set_image(url = url)
      em.set_footer(text=f"posted in r/{subred} | requested by {ctx.author.name}")

      if submission.over_18:
        await ctx.send("the post is nsfw")
      else:
        await ctx.send(embed = em)
    


def setup(client):
  client.add_cog(Memes(client))