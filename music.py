# Music requires a separately hosted Lavalink server.
import os, discord, wavelink
from discord.ext import commands
class Music(commands.Cog):
 def __init__(self,bot): self.bot=bot
 async def cog_load(self):
  uri=os.getenv('LAVALINK_URI'); password=os.getenv('LAVALINK_PASSWORD')
  if uri and password: await wavelink.Pool.connect(nodes=[wavelink.Node(uri=uri,password=password)],client=self.bot)
 @discord.app_commands.command(name='play',description='Phát nhạc (cần Lavalink)')
 async def play(self,i:discord.Interaction,query:str):
  if not i.user.voice: return await i.response.send_message('Vào voice channel trước.',ephemeral=True)
  await i.response.defer()
  player=i.guild.voice_client or await i.user.voice.channel.connect(cls=wavelink.Player)
  tracks=await wavelink.Playable.search(query)
  if not tracks: return await i.followup.send('Không tìm thấy bài.')
  await player.play(tracks[0]); await i.followup.send('▶️ Đang phát: '+tracks[0].title)
 @discord.app_commands.command(name='stop',description='Dừng nhạc')
 async def stop(self,i):
  p=i.guild.voice_client
  if p: await p.disconnect(); await i.response.send_message('Đã dừng.')
  else: await i.response.send_message('Bot chưa ở voice.',ephemeral=True)
async def setup(bot): await bot.add_cog(Music(bot))
