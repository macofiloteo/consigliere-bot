from discord import Intents, Interaction, app_commands
from discord.ext import commands
from discord.utils import get

from bll.network import is_ip_address_online, list_uphosts, wake_host
from config import DISCORD_TOKEN

from workers.streamer_thread import AudioStreamerManager


client = commands.Bot(command_prefix='/', intents=Intents(guilds=True, guild_messages=True))
audio_worker = AudioStreamerManager()

@client.event
async def on_ready():
	guild_count = 0
	for guild in client.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")
		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1
	await client.tree.sync()
	print("Consigliere is in " + str(guild_count) + " guilds.")


@client.tree.command(name='ping', description='Check if a machine is online based on IP address.')
@app_commands.describe(ip_address="The IP address of the machine you want to check")
async def ping(interaction: Interaction, ip_address: str):
    response = f"The IP Address {ip_address} is"
    if is_ip_address_online(ip_address):
        response = response + " online!"
    else:
        response = response + " offline!"
    await interaction.response.send_message(response)


@client.tree.command(name='wake')
@app_commands.describe(mac_address="The MAC Address of the machine you want to turn on")
async def wake(interaction: Interaction, mac_address: str):
    try:
        wake_host(mac_address)
        await interaction.response.send_message(f"WOL Magic Packet sent successfully.")
    except:
        await interaction.response.send_message(f"Failed to send the WOL Magic Packet.")


client.run(DISCORD_TOKEN)