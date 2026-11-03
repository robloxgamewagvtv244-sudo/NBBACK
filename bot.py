import os, random, asyncio, time
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from database import DB
load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")
db=DB(os.getenv("DB_PATH","nbback.db"))
intents=discord.Intents.default()
intents.message_content=True
intents.members=True
bot=commands.Bot(command_prefix="!",intents=intents,help_command=None)

async def log(guild,text):
    cid=db.setting(guild.id,"logs")
    ch=guild.get_channel(int(cid)) if cid else None
    if ch:
        try: await ch.send("📝 "+text)
        except discord.HTTPException: pass

@bot.event
async def on_ready():
    await bot.tree.sync()
    bot.add_view(TicketView())
    print("NBBACK online:",bot.user)

@bot.event
async def on_message(m):
    if m.guild and not m.author.bot:
        now=int(time.time())
        if now-db.last(m.guild.id,m.author.id)>=60:
            db.xp(m.guild.id,m.author.id,random.randint(8,15),now)
    await bot.process_commands(m)

@bot.event
async def on_member_join(m):
    cid=db.setting(m.guild.id,"welcome")
    ch=m.guild.get_channel(int(cid)) if cid else None
    if ch: await ch.send(f"👋 Chào mừng {m.mention} đến {m.guild.name}!")
    await log(m.guild,f"{m} đã tham gia.")
@bot.event
async def on_member_remove(m): await log(m.guild,f"{m} đã rời server.")
@bot.event
async def on_message_delete(m):
    if m.guild and not m.author.bot: await log(m.guild,f"Tin nhắn của {m.author} bị xóa.")

@bot.tree.command(name="ping",description="Kiểm tra bot")
async def ping(i): await i.response.send_message(f"Pong `{round(bot.latency*1000)} ms`")
@bot.tree.command(name="setup_logs",description="Chọn kênh nhật ký")
@app_commands.checks.has_permissions(manage_guild=True)
async def setup_logs(i,channel:discord.TextChannel):
    db.set(i.guild_id,"logs",channel.id); await i.response.send_message(f"Đã đặt {channel.mention}",ephemeral=True)
@bot.tree.command(name="setup_welcome",description="Chọn kênh chào mừng")
@app_commands.checks.has_permissions(manage_guild=True)
async def setup_welcome(i,channel:discord.TextChannel):
    db.set(i.guild_id,"welcome",channel.id); await i.response.send_message(f"Đã đặt {channel.mention}",ephemeral=True)
@bot.tree.command(name="ban",description="Ban thành viên")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(i,member:discord.Member,reason:str="Không nêu lý do"):
    await member.ban(reason=reason); await i.response.send_message(f"Đã ban {member}.")
    await log(i.guild,f"{member} bị ban bởi {i.user}: {reason}")
@bot.tree.command(name="kick",description="Kick thành viên")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(i,member:discord.Member,reason:str="Không nêu lý do"):
    await member.kick(reason=reason); await i.response.send_message(f"Đã kick {member}.")
@bot.tree.command(name="timeout",description="Timeout theo phút")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(i,member:discord.Member,minutes:app_commands.Range[int,1,40320],reason:str="Không nêu lý do"):
    from datetime import timedelta
    await member.timeout(discord.utils.utcnow()+timedelta(minutes=minutes),reason=reason)
    await i.response.send_message(f"Đã timeout {member} {minutes} phút.")
class TicketView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Đóng ticket",style=discord.ButtonStyle.danger,custom_id="nbback:close")
    async def close(self,i,b):
        if not i.user.guild_permissions.manage_channels and not i.channel.name.startswith("ticket-"):
            return await i.response.send_message("Không có quyền.",ephemeral=True)
        await i.response.send_message("Đang đóng ticket...")
        await asyncio.sleep(2); await i.channel.delete()
@bot.tree.command(name="ticket",description="Mở ticket hỗ trợ")
async def ticket(i):
    g=i.guild
    ow={g.default_role:discord.PermissionOverwrite(view_channel=False),i.user:discord.PermissionOverwrite(view_channel=True,send_messages=True),g.me:discord.PermissionOverwrite(view_channel=True,send_messages=True,manage_channels=True)}
    ch=await g.create_text_channel("ticket-"+i.user.name[:15],overwrites=ow)
    await ch.send(f"{i.user.mention}, hãy mô tả vấn đề của bạn.",view=TicketView())
    await i.response.send_message(f"Đã tạo {ch.mention}",ephemeral=True)
@bot.tree.command(name="rank",description="Xem XP")
async def rank(i,member:discord.Member=None):
    m=member or i.user; x=db.total(i.guild_id,m.id)
    await i.response.send_message(f"{m.mention}: Level {int((x/100)**0.5)} · {x} XP")
@bot.tree.command(name="leaderboard",description="Top XP")
async def leaderboard(i):
    rows=db.top(i.guild_id)
    await i.response.send_message("🏆 Bảng XP\n"+("\n".join(f"{n}. <@{u}> — {x} XP" for n,(u,x) in enumerate(rows,1)) or "Chưa có dữ liệu."))
@bot.tree.command(name="guess",description="Đoán số 1-20")
async def guess(i,n:app_commands.Range[int,1,20]):
    s=random.randint(1,20); await i.response.send_message("🎉 Đúng!" if n==s else f"Chưa đúng, số là {s}.")
@bot.tree.command(name="coinflip",description="Tung đồng xu")
async def coinflip(i): await i.response.send_message(random.choice(["🪙 Ngửa!","🪙 Sấp!"]))
@bot.tree.command(name="giveaway",description="Giveaway theo phút")
@app_commands.checks.has_permissions(manage_guild=True)
async def giveaway(i,minutes:app_commands.Range[int,1,10080],prize:str):
    await i.response.send_message(f"🎉 **{prize}** — react 🎉 để tham gia, kết thúc sau {minutes} phút.")
    msg=await i.original_response(); await msg.add_reaction("🎉")
    await asyncio.sleep(minutes*60)
    msg=await i.channel.fetch_message(msg.id); users=[]
    for r in msg.reactions:
        if str(r.emoji)=="🎉":
            async for u in r.users():
                if not u.bot: users.append(u)
    await i.channel.send(f"Người thắng: {random.choice(users).mention}" if users else "Không có người tham gia.")
async def main():
    if not TOKEN: raise RuntimeError("Thiếu DISCORD_TOKEN trong Secrets/.env")
    async with bot: await bot.start(TOKEN)
if __name__=="__main__": asyncio.run(main())
