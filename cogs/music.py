# import asyncio
# import nextcord

import pafy

from nextcord.ext import commands


ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0" # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    "options": "-vn"
}


# class YTDLSource(nextcord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)

#         self.data = data

#         self.title = data.get("title")
#         self.url = data.get("url")

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

#         if "entries" in data:
#             # take first item from a playlist
#             data = data["entries"][0]

#         filename = data["url"] if stream else ytdl.prepare_filename(data)
#         return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class SongInQueueException(Exception):
  def __init__(self, message):
    super(message)

class GuildQuery:
  def __init__(self, vc, text_channel):
    self.vc = vc
    self.current_song = 0
    self.text_channel = text_channel
    self.songs = []
  
  def add_song(self, song):
    if song in self.songs:
      raise SongInQueueException(f"{song} is already in the queue")

    self.songs.append(song)

    self.play(len(self.songs) - 1)

  def has_song(self, song):
    for s in self.songs:
      if s.name is song.name:
        return True
    
    return False
  
  def play(self, index):
    self.current_song = index
    song = self.songs[self.current_song]
    self.vc.play(song.getbestaudio())
    self.text_channel.send(f"Now playing: {song.title}")

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queries = []

    def has_query(self, guild):
      for query in self.queries:
        if query.vc.guild.id == guild.id:
          return True
      
      return False

    def get_query(self, guild) -> GuildQuery:
      for query in self.queries:
        if query.vc.guild.id == guild.id:
          return query
      
      return None
    
    def set_query(self, query):
      for index in range(len(self.queries)):
        if self.queries[index].guild.id == query.guild.id:
          self.queries[index] = query
          return True
      
      return False

    @commands.command(help="Make the bot join a voice channel", aliases=["j"])
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"joined {channel}")

    @commands.command(help="Make the bot leave a voice channel", aliases=["f-off", "bye", "get-out", "l", "disconect", "d"])
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send(":+1:")

    @commands.command()
    async def play(self, ctx, *, url):
      guild = ctx.channel.guild

      if self.has_query(guild):
        query = self.get_query(guild)

        song = pafy.new(url)
      else:
        query = GuildQuery(ctx.author.voice.channel, ctx.channel)
        
        song = pafy.new(url)
        
      try:
        query.add_song(song)
      except Exception as e:
        await ctx.send(e.message)

    # @commands.command()
    # async def yt(self, ctx, *, url):
    #   """Plays from a url (almost anything youtube_dl supports)"""

    #   async with ctx.typing():
    #       player = await YTDLSource.from_url(url, loop=self.client.loop)
    #       ctx.voice_client.play(player, after=lambda e: print(f"Player error: {e}") if e else None)

    #   await ctx.send(f"Now playing: {player.title}")

    # @commands.command()
    # async def stream(self, ctx, *, url):
    #   """Streams from a url (same as yt, but doesn"t predownload)"""

    #   async with ctx.typing():
    #       player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
    #       ctx.voice_client.play(player, after=lambda e: print(f"Player error: {e}") if e else None)

    #   await ctx.send(f"Now playing: {player.title}")

    # @commands.command()
    # async def volume(self, ctx, volume: int):
    #   """Changes the player"s volume"""

    #   if ctx.voice_client is None:
    #       return await ctx.send("Not connected to a voice channel.")

    #   ctx.voice_client.source.volume = volume / 100
    #   await ctx.send(f"Changed volume to {volume}%")

    # @play.before_invoke
    # @yt.before_invoke
    # @stream.before_invoke
    # async def ensure_voice(self, ctx):
    #   if ctx.voice_client is None:
    #       if ctx.author.voice:
    #           await ctx.author.voice.channel.connect()
    #       else:
    #           await ctx.send("You are not connected to a voice channel.")
    #           raise commands.CommandError("Author not connected to a voice channel.")
    #   elif ctx.voice_client.is_playing():
    #       ctx.voice_client.stop()

def setup(client):
  client.add_cog(Music(client))