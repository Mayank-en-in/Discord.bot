import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os
from discord import app_commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

numbers=[1,2,3,4,5,6,7,8,9,0]
command_prefix='!'
target_user_id = 821736045322174475
# bot = commands.Bot(command_prefix='!', intents=intents)
bot = commands.Bot(command_prefix='!',
                   status=discord.Status.idle,
                   activity=discord.Game(name="Reacting to Your Message"),
                   intents=intents)


####################################### MUSIC SECTION ##########################################
queued_song = []
looping = False  # Track whether the current song should be looped

# Define the command to join the voice channel
@bot.tree.command(name="join", description="Bot joins the voice channel")
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
        else:
            await channel.connect()
        await interaction.response.send_message(f"Joined {channel}")
    else:
        await interaction.response.send_message("You are not connected to a voice channel.")

# Function to play the next song in the queue
async def play_next_song(interaction: discord.Interaction):
    global looping

    if looping and queued_song:
        # Re-add the last played song to the front of the queue if looping is enabled
        queued_song.insert(0, queued_song[-1])

    if queued_song:
        next_song = queued_song.pop(0)
        # Get the 'play' command and pass the required arguments
        play_command = interaction.client.tree.get_command("play")
        if play_command:
            await play_command.callback(interaction, next_song, True)

# Define the command to play a song
@bot.tree.command(name="play", description="Play a song in the voice channel")
@app_commands.describe(song_name="The name of the song to play")
async def play(interaction: discord.Interaction, song_name: str, from_queue: bool = False):
    global looping

    # Defer the response to give time for processing
    if not from_queue:
        await interaction.response.defer()

    voice_client = interaction.guild.voice_client
    
    if voice_client and voice_client.is_playing() and not from_queue:
        queued_song.append(song_name)
        await interaction.followup.send(f"Added to queue: {song_name}")
        return
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                video = info['entries'][0]
                formats = video['formats']
                audio_url = None
                
                for f in formats:
                    if 'acodec' in f and f['acodec'] != 'none':
                        audio_url = f['url']
                        break

                if not audio_url:
                    if not from_queue:
                        await interaction.followup.send("Could not find an audio format.")
                    return

                title = video['title']
                
                # Log URL and other details
                print(f"Audio URL: {audio_url}")
                print(f"Video Title: {title}")

                if not voice_client:
                    if interaction.user.voice:
                        channel = interaction.user.voice.channel
                        voice_client = await channel.connect()
                    else:
                        if not from_queue:
                            return await interaction.followup.send("You need to be in a voice channel first.")

                source = discord.FFmpegPCMAudio(source=audio_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn")
                voice_client.play(source, after=lambda e: bot.loop.create_task(play_next_song(interaction)) if e is None else print(f'Player error: {e}'))

                if not from_queue:
                    await interaction.followup.send(f"Playing {title}")
            else:
                if not from_queue:
                    await interaction.followup.send("Could not find the song.")
        except Exception as e:
            logging.error(f"Error: {e}")
            if not from_queue:
                try:
                    await interaction.followup.send(f"An error occurred: {e}")
                except discord.errors.NotFound:
                    logging.error("Interaction no longer valid, failed to send error message.")

# Define the command to loop the current song
@bot.tree.command(name="loop", description="Loop the current song")
async def loop(interaction: discord.Interaction):
    global looping
    looping = not looping
    if looping:
        await interaction.response.send_message("Looping the current song.")
    else:
        await interaction.response.send_message("Stopped looping the current song.")

@bot.tree.command(name="stop", description="Stop the song that is currently playing")
async def stop(interaction: discord.Interaction):
    global looping
    looping = False
    if interaction.guild.voice_client:
        interaction.guild.voice_client.stop()
        queued_song.clear()
        await interaction.response.send_message("Stopped the song and cleared the queue.")
    else:
        await interaction.response.send_message("Bot is not playing any song.")

@bot.tree.command(name="leave", description="Bot leaves the voice channel")
async def leave(interaction: discord.Interaction):
    global looping
    looping = False
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        queued_song.clear()
        await interaction.response.send_message("Left the voice channel and cleared the queue.")
    else:
        await interaction.response.send_message("Bot is not connected to a voice channel.")

@bot.tree.command(name="queue", description="Display the current song queue")
async def queue(interaction: discord.Interaction):
    if len(queued_song) > 0:
        queue_list = "\n".join([f"{i+1}. {song}" for i, song in enumerate(queued_song)])
        await interaction.response.send_message(f"**Current Queue:**\n{queue_list}")
    else:
        await interaction.response.send_message("The queue is empty.")

##################################################### MUSIC END ############################################################


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

    if 'hi' == message.content.lower() or 'baii' in message.content.lower() or 'hello' in message.content.lower() or 'bye' in message.content.lower() or 'Welcome' in message.content.lower() or 'Left' in message.content.lower():
        await message.add_reaction('👋')

    if 'ok' == message.content.lower() or 'okii' == message.content.lower():
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
        
    if '<@821736045322174475>' in message.content.lower():
        await message.add_reaction(':ridercatsleep:1222471552080281660')

    if  (message.content.lower()).isdigit():
        #await message.add_reaction('🔢')
        await message.add_reaction(':verifiedverificasdo:1220294706240552990')

     # Check if the target user is mentioned in the message
    if target_user_id in [mention.id for mention in message.mentions] and message.reference is None and client.get_user(821736045322174475).status != discord.Status.online:
        # Replace the 'busy_message' string with the desired message
        busy_message = "I'm sorry, The 'LordNightRider' is gone for sleep in the Server's Darkest Room. Please Let him Sleep Right now and try messaging later."
        await message.channel.send(busy_message)

        
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.tree.sync()


class ReactionBot():
    def __init__(self,):
        self.token=str(os.environ.get('TOKEN'))

    def runBot(self):
        bot.run(token=self.token)
