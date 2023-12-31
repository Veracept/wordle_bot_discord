import logging
import os
from typing import Optional

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

from utils import (
    daily_puzzle_id,
    generate_info_embed,
    generate_puzzle_embed,
    process_message_as_guess,
    random_puzzle_id,
)

intents = nextcord.Intents.default()
intents.message_content = True

load_dotenv()

activity = nextcord.Activity(type=nextcord.ActivityType.listening, name="/play")

bot = commands.Bot(command_prefix=commands.when_mentioned_or("w?"), activity=activity, intents=intents)

GUILD_IDS = (
    [int(guild_id) for guild_id in os.getenv("GUILD_IDS", "").split(",")]
    if os.getenv("GUILD_IDS", None)
    else nextcord.utils.MISSING
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.slash_command(name="play", description="Играть в Wordle", guild_ids=GUILD_IDS)
async def slash_play(interaction: nextcord.Interaction):
    """This command has subcommands for playing a game of Wordle Clone."""
    pass


@slash_play.subcommand(name="random", description="Сыграйте в случайную игру Wordle")
async def slash_play_random(interaction: nextcord.Interaction):
    embed = generate_puzzle_embed(interaction.user, random_puzzle_id())
    await interaction.send(embed=embed)


@slash_play.subcommand(name="id", description="Сыграйте в игру Wordle по его id")
async def slash_play_id(
    interaction: nextcord.Interaction,
    puzzle_id: int = nextcord.SlashOption(description="Введите ID(всего 2990)"),
):
    embed = generate_puzzle_embed(interaction.user, puzzle_id)
    await interaction.send(embed=embed)


@slash_play.subcommand(name="daily", description="Сыграйте в ежедневное загаданное слово")
async def slash_play_daily(interaction: nextcord.Interaction):
    embed = generate_puzzle_embed(interaction.user, daily_puzzle_id())
    await interaction.send(embed=embed)


@bot.slash_command(name="info", description="Инфромация о боте", guild_ids=GUILD_IDS)
async def slash_info(interaction: nextcord.Interaction):
    await interaction.send(embed=generate_info_embed())


@bot.group(invoke_without_command=True)
async def play(ctx: commands.Context, puzzle_id: Optional[int] = None):
    """Play a game of Wordle Clone"""
    embed = generate_puzzle_embed(ctx.author, puzzle_id or random_puzzle_id())
    await ctx.reply(embed=embed, mention_author=False)


@play.command(name="random")
async def play_random(ctx: commands.Context):
    """Play a random game of Wordle Clone"""
    embed = generate_puzzle_embed(ctx.author, random_puzzle_id())
    await ctx.reply(embed=embed, mention_author=False)


@play.command(name="id")
async def play_id(ctx: commands.Context, puzzle_id: int):
    """Play a game of Wordle Clone by its ID"""
    embed = generate_puzzle_embed(ctx.author, puzzle_id)
    await ctx.reply(embed=embed, mention_author=False)


@play.command(name="daily")
async def play_daily(ctx: commands.Context):
    """Play the daily game of Wordle Clone"""
    embed = generate_puzzle_embed(ctx.author, daily_puzzle_id())
    await ctx.reply(embed=embed, mention_author=False)


@bot.command()
async def info(ctx: commands.Context):
    """Info about Discord Wordle Clone"""
    await ctx.reply(embed=generate_info_embed(), mention_author=False)


@bot.event
async def on_message(message: nextcord.Message):
    """
    When a message is sent, process it as a guess.
    Then, process any commands in the message if it's not a guess.
    """
    processed_as_guess = await process_message_as_guess(bot, message)
    if not processed_as_guess:
        await bot.process_commands(message)


bot.run("")
