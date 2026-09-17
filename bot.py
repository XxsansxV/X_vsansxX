import os
import subprocess
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="//", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}, (ID = {bot.user.id})')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash commands!')
    except Exception as e:
        print(f'failed to sync commands: {e}')

@bot.tree.command(name="ping", description="just pings the bot, really.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!!!!",ephemeral=True)

@bot.tree.command(name="greet", description="Greets the user of this command, maybe.")
async def greet(interaction: discord.Interaction, name:str):
    await interaction.response.send_message(f'Hello, {name}')

@bot.tree.command(name="gap",description="prints lines amounts of gaps")
async def gap(interaction: discord.Interaction, lines:app_commands.Range[int, 1, 1000]):
    emptychar = '‎'
    tosend = f''
    for x in range(lines):
        tosend = f'{tosend}{emptychar}\n'
    await interaction.response.send_message(tosend)

@bot.tree.command(name="fortune", description="fortune messages")
async def fortune(interaction: discord.Interaction):
    try:
        fortune_result = subprocess.run(['fortune'], capture_output=True, text=True, check=True)
        fortune_result_output = fortune_result.stdout
        await interaction.response.send_message(fortune_result_output)
    except FileNotFoundError:
        await interaction.response.send_message("The laptop the bot runs on doesn't have fortune-mod installed!")

bot.run(TOKEN)
