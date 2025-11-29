import discord
from discord.ext import commands
import yt_dlp
import asyncio

# --- AYARLAR ---
# Tokenini Replit'e aktardıktan sonra buraya yazacaksın!
TOKEN = "TOKEN_BURAYA_GELECEK" 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

yt_dl_opts = {'format': 'bestaudio/best', 'noplaylist': True}
ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
ffmpeg_options = {'options': '-vn'}

@bot.event
async def on_ready():
    print(f'{bot.user} Müzik için hazır!')

@bot.command()
async def gir(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("🔊 Kanala girdim.")
    else:
        await ctx.send("⚠️ Önce ses kanalına gir.")

@bot.command()
async def cik(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Çıktım.")

@bot.command()
async def cal(ctx, *, arama):
    if not ctx.author.voice:
        return await ctx.send("Ses kanalına girmen lazım!")
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    
    await ctx.send(f"🔎 **{arama}** aranıyor...")
    
    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{arama}", download=False))
        
        if 'entries' in data:
            data = data['entries'][0]
            
        song_url = data['url']
        title = data['title']
        
        player = await discord.FFmpegOpusAudio.from_probe(song_url, **ffmpeg_options)
        ctx.voice_client.stop()
        ctx.voice_client.play(player)
        await ctx.send(f"🎶 Çalınıyor: **{title}**")
        
    except Exception as e:
        print(e)
        await ctx.send("❌ Hata oluştu veya YouTube engelledi.")

bot.run(TOKEN)
