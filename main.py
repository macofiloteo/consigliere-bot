from discord import Intents, Interaction
from discord.ext import commands
from discord.utils import get

from config import DISCORD_TOKEN

from bll.audio import get_audio_path
from dal.database import create_session
from exceptions import NoWorkerExists
from workers.streamer_thread import AudioStreamerManager


client = commands.Bot(command_prefix='/', intents=Intents(guilds=True, guild_messages=True, voice_states=True))
audio_worker = AudioStreamerManager()

async def get_voice_client(interaction: Interaction):
    user_voice = interaction.user.voice
    if not user_voice:
        # user is not in a voice channel - exit
        await interaction.response.send_message("You are not in a voice channel", ephemeral=True)
        return
    bot_voice = get(client.voice_clients, guild=interaction.guild)
    if bot_voice:
        # we're in a channel already
        if bot_voice.channel.id != user_voice.channel.id:
            await bot_voice.move_to(user_voice.channel)
        voice_client = bot_voice
    else:
        await user_voice.channel.connect()
        voice_client = get(client.voice_clients, guild=interaction.guild)
    return voice_client


@client.event
async def on_ready():
	guild_count = 0
	for guild in client.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1
	print("Consigliere is in " + str(guild_count) + " guilds.")


@client.tree.command(name='ping', description='Replies with PONG and syncs the tree.')
async def ping(interaction):
    await client.tree.sync(guild=interaction.guild)
    await interaction.response.send_message('PONG!')


@client.tree.command(name='skip', description='Skips the currently playing audio')
async def skip(interaction: Interaction):
    # Validate user is in a voice channel
    await get_voice_client(interaction)

    try:
        audio_worker.skip_now_playing(interaction.guild)
        await interaction.response.send_message('Skipped!')
    except NoWorkerExists:
        await interaction.response.send_message("No audio is currently playing or you are not in a voice channel", ephemeral=True)


@client.tree.command(name='play', description='Searches for a song and plays it in the voice channel the current user is in')
async def play(interaction: Interaction):
    db_session = create_session() # temporarily here, will move it to a better place
    voice_client = await get_voice_client(interaction)    
    params = interaction.data['options']
    if not params:
        await interaction.response.send_message("No parameters provided", ephemeral=True)
        return
    if not params[0]['value']:
        await interaction.response.send_message("No search query provided", ephemeral=True)
    
    search_query = params[0]['value']
    await interaction.response.send_message(f"Searching for {search_query}...", ephemeral=True)
    try:
        dl_file_path = get_audio_path(db_session, search_query)
    except FileNotFoundError as e:
        await interaction.edit_original_response(content=f"Could not find audio for {search_query}")
        return
    audio_worker.queue_audio_file(interaction.guild, voice_client, dl_file_path)
    db_session.commit()
    db_session.close()
    return

@client.tree.command(name='stop')
async def stop(interaction: Interaction):
    await interaction.response.send_message('Stopping...')

client.run(DISCORD_TOKEN)