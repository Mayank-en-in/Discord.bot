import discord
from discord.ext import commands
import youtube_dl
import os

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

numbers=[1,2,3,4,5,6,7,8,9,0]
command_prefix='!'

# bot = commands.Bot(command_prefix='!', intents=intents)
bot = commands.Bot(command_prefix='!',
                   status=discord.Status.idle,
                   activity=discord.Game(name="Reacting to Your Message"),
                   intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.tree.sync()

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send('Joined! Use ```!play #Your Music``` to play Music')    

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch',  # Add this line
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        await ctx.send(f"Now playing: {info['title']}")
    
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        url2 = info['formats'][0]['url']
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn',
        }
        ctx.voice_client.play(discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS))

    

@bot.tree.command(name="avatar",description="Get user avatar")
async def avatar(interaction:discord.Interaction,member:discord.Member):
    await interaction.response.send_message(member.display_avatar)

@bot.event
async def on_message(message):
    print(message.content)
    if message.author == bot.user:  # Avoid reacting to own messages
        return

    if bot.user.mentioned_in(message):
        await message.add_reaction('👀')

    if 'python' in message.content.lower():
        await message.add_reaction('🐍')

    if '69' == message.content.lower():
        await message.add_reaction('😒')
        await message.add_reaction('🙄')
        await message.add_reaction('😏')

    if 'snake' in message.content.lower():
        await message.add_reaction('🐍')      

    if command_prefix + 'join' == message.content.lower() or command_prefix + 'play' == message.content.lower() or command_prefix + 'leave' == message.content.lower():
        await message.add_reaction('🇩')
        await message.add_reaction('🇴')
        await message.add_reaction('🇳')
        await message.add_reaction('🇪')
        await message.add_reaction('✅')

    if 'hi' == message.content.lower() or 'baii' in message.content.lower() or 'hello' in message.content.lower() or 'bye' in message.content.lower():
        await message.add_reaction('👋')

    if 'ok' in message.content.lower() or 'okii' == message.content.lower():
        await message.add_reaction('🆗')
        await message.add_reaction('👍')

    if 'what' in message.content.lower() or 'wat' in message.content.lower() or 'wht' in message.content.lower() or 'why' in message.content.lower():
        await message.add_reaction('❓')

    if 'lol' in message.content.lower() or 'lmao' in message.content.lower():
        await message.add_reaction('😂')
        await message.add_reaction('🤣')

    if 'fun' in message.content.lower():
        await message.add_reaction('😉')
        await message.add_reaction('🤣')

    if  '<@&1180172147600130159>' in message.content.lower() or '<@926135282582044692>' in message.content.lower():
        await message.add_reaction('👑')
        await message.add_reaction(':jeb_KING_FYPER_756:1220373874923798670')
        #await message.add_reaction(':7041darkbluecrown:1220373871803371642')

    if 'damm' in message.content.lower() or 'dem' in message.content.lower() or 'damn' in message.content.lower():
        await message.add_reaction('🇩')
        await message.add_reaction('🇦')
        await message.add_reaction('🇲')
        await message.add_reaction('🇳')

    if 'sad' in message.content.lower():
        await message.add_reaction('😭')

    if 'happy' in message.content.lower():
        await message.add_reaction('😁')

    if 'angry' in message.content.lower():
        await message.add_reaction('😡')

    if 'nice' in message.content.lower():
        await message.add_reaction('🙃')

    if 'cool' in message.content.lower():
        await message.add_reaction('🆒')
        await message.add_reaction('🧊')

    if message.content.lower().isdigit():
        #await message.add_reaction('🔢')
        await message.add_reaction(':verifiedverificado:1220294706240552990')
        

    await bot.process_commands(message)

class ReactionBot():
    def __init__(self,):
        self.token=str(os.environ.get('TOKEN'))

    def runBot(self):
        bot.run(token=self.token)
