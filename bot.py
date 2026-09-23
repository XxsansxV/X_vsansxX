# This bot is officially She/her and Lesbian.

import asyncio
import os
import random
import subprocess

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="//", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}, (ID = {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands!")
    except Exception as e:
        print(f"failed to sync commands: {e}")


@bot.tree.command(
    name="ping",
    description="Pings the bot and calculates the latency between the bot and the user",
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"**Pong!!!!** my latency is roughly {round(bot.latency * 1000, 2)}ms right now!\n-# pssst, get me good wifi pls!!!"
    )


greetings = (
    "Hello, {name} :)",
    "Привет, {name} )))",
    "Guten tag, {name}. Ich wuensch sie guten lebens.",
    "Yo {name}, what's good?",
    "Hey there! Glad to see you, {name}.",
    "Wazzup {name}.",
    "你好，{name}.",
    "喂，{name}，你在吗？",
    "नमस्ते, {name}",
)


@bot.tree.command(name="greet", description="Greets <name>")
async def greet(interaction: discord.Interaction, name: str):
    chosen_greeting = random.choice(greetings)
    await interaction.response.send_message(chosen_greeting.format(name=name))


@bot.tree.command(name="gap", description="prints <lines> amounts of gaps")
async def gap(
    interaction: discord.Interaction, lines: app_commands.Range[int, 1, 1000]
):
    emptychar = "‎"
    tosend = ""
    tosend = (emptychar + "\n") * lines
    await interaction.response.send_message(tosend)


@bot.tree.command(name="fortune", description="Random fortune-mod messages")
async def fortune(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        fortune_result = await asyncio.to_thread(
            subprocess.run, ["fortune"], capture_output=True, text=True, check=True
        )
        fortune_result_output = fortune_result.stdout
        await interaction.followup.send(fortune_result_output)
    except FileNotFoundError:
        await interaction.followup.send(
            "The laptop the bot runs on doesn't have fortune-mod installed!"
        )
    except Exception as e:
        await interaction.followup.send(
            "Something went hborribly wrong. don't worry, it's never being resolved ;)"
        )
        print(e)


eightball_superanswers = (
    # eightball_superanswers[0] would print the respond, while [1] should use the color, neat, huh?
    # ("RESPOND","COLOR")
    ("DEFINITELY.", discord.Color.green()),
    ("Surely", discord.Color.green()),
    ("Evaluates to ```True ```", discord.Color.green()),
    (
        "According to my calculations, it is the **highly likely**.",
        discord.Color.green(),
    ),
    ("Highly likely ;)", discord.Color.green()),
    ("Why would't it be that way?", discord.Color.green()),
    ("Hell yeah!", discord.Color.green()),
    (
        "We must be optimistic and assume that the answer is **YES**",
        discord.Color.green(),
    ),
    ("yes, indeed.", discord.Color.green()),
    ("Eh.... Maybe?", discord.Color.yellow()),
    ("Possibly", discord.Color.yellow()),
    ("Perhaps???", discord.Color.yellow()),
    ("That too I wonder of", discord.Color.yellow()),
    (
        "We must be optimistic enough to assume that it's true but also realistic enough to know it's likely false. So in conclusion: **Perchance**",
        discord.Color.yellow(),
    ),
    ("¯\\_(ツ)_/¯", discord.Color.yellow()),
    ("Absolutely no.", discord.Color.red()),
    ("Nah.", discord.Color.red()),
    ("No.", discord.Color.red()),
    ("Everythings points to this:\n**NO**.", discord.Color.red()),
    ("Nope, no shot.", discord.Color.red()),
    ("Why... would it ever be that way?", discord.Color.red()),
    ("Stop delulu. **NO**", discord.Color.red()),
    ("We should be realistic. **Nope**", discord.Color.red()),
    ("Never!!!!!!!", discord.Color.red()),
    ("Ask later", discord.Color.blue()),
    ("Oops! try again later", discord.Color.blue()),
    ("-_-", discord.Color.blue()),
    ("0_o?", discord.Color.blue()),
    ("Probably", discord.Color.yellow()),
)


@bot.tree.command(
    name="eightball", description="Responds yes/no questions with a random answer"
)
async def eightball(interaction: discord.Interaction, question: str):
    picked_eightball = random.randrange(0, len(eightball_superanswers))
    embed = discord.Embed(
        title="🎱 8ball",
        description=f"Here's your response, {interaction.user.mention}",
        color=eightball_superanswers[picked_eightball][1],
    )
    embed.add_field(name="Question", value=question)
    embed.add_field(name="Response", value=eightball_superanswers[picked_eightball][0])
    embed.set_footer(text=f"Requested by {interaction.user.name}")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="help", description="Print out the help message.")
async def help(interaction: discord.Interaction):
    slash_commands = [cmd.name for cmd in bot.tree.walk_commands()]
    slash_descriptions = [cmd.description for cmd in bot.tree.walk_commands()]

    # legacy, used when i didn't want to show descriptions
    # commands_toprint = "\n".join([f"- **{s}**" for s in slash_commands])

    commands_toprint: str = ""
    for name, description in zip(slash_commands, slash_descriptions):
        commands_toprint += f"- **{name}** : {description}\n"

    slash_commands_count = len(slash_commands)

    embed = discord.Embed(
        title="❓ Help",
        description="X_vsansxX the pointless silly discord bot(tm)(r)(c)pte ltd",
        color=discord.Color.green(),
    )
    embed.add_field(
        name="List of commands : \n",
        value=f"{commands_toprint}Currently **{slash_commands_count}** commands.",
    )
    await interaction.response.send_message(embed=embed)


bot.run(TOKEN)
