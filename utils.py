import datetime
import random
import re
from typing import List, Optional

import nextcord

popular_words = open("dict-popular.txt").read().splitlines()
all_words = set(word.strip() for word in open("dict-sowpods.txt"))

EMOJI_CODES = {
    "green": {
        "a": "<:1f1e6:1126859397910507610> ",
        "b": "<:1f1e7:1126859400351592619> ",
        "c": "<:1f1e8:1126859402088022077> ",
        "d": "<:1f1e9:1126859405783220305> ",
        "e": "<:1f1ea:1126859407297363998> ",
        "f": "<:1f1eb:1126859409969139873> ",
        "g": "<:1f1ec:1126859412296966275> ",
        "h": "<:1f1ed:1126859415191044206> ",
        "i": "<:1f1ee:1126859418617794612> ",
        "j": "<:1f1ef:1126859423139250248> ",
        "k": "<:1f1f0:1126859424611438733> ",
        "l": "<:1f1f1:1126859427111256096> ",
        "m": "<:1f1f2:1126859429745283225> ",
        "n": "<:1f1f3:1126859432605778040> ",
        "o": "<:1f1f4:1126859435831214160> ",
        "p": "<:1f1f5:1126859437970305156> ",
        "q": "<:1f1f6:1126859441023746148> ",
        "r": "<:1f1f7:1126859442521112606> ",
        "s": "<:1f1f8:1126859446023368824> ",
        "t": "<:1f1f9:1126859447852073020> ",
        "u": "<:1f1fa:1126859451245273159> ",
        "v": "<:1f1fb:1127677314474463313> ",
        "w": "<:1f1fc:1126859456634966147> ",
        "x": "<:1f1fd:1126859459617116180> ",
        "y": "<:1f1fe:1126859461500358698> ",
        "z": "<:1f1ff:1126859468609699880> ",
    },
    "yellow": {
        "a": "<:1f1e6:1126860389527863296> ",
        "b": "<:1f1e7:1126860393940275261> ",
        "c": "<:1f1e8:1126860396674953227> ",
        "d": "<:1f1e9:1126860400135258193> ",
        "e": "<:1f1ea:1126860403037712474> ",
        "f": "<:1f1eb:1126860405914996867> ",
        "g": "<:1f1ec:1126860408272191488> ",
        "h": "<:1f1ed:1126860411573129276> ",
        "i": "<:1f1ee:1126860413347299438> ",
        "j": "<:1f1ef:1126860416144900208> ",
        "k": "<:1f1f0:1126860418216890459> ",
        "l": "<:1f1f1:1126860421136130139> ",
        "m": "<:1f1f2:1126860423308775494> ",
        "n": "<:1f1f3:1126860426269958164> ",
        "o": "<:1f1f4:1126860428572622960> ",
        "p": "<:1f1f5:1126860431076642878> ",
        "q": "<:1f1f6:1126860433471574026> ",
        "r": "<:1f1f7:1126860436512456754> ",
        "s": "<:1f1f8:1126860438223728701> ",
        "t": "<:1f1f9:1126860441407197265> ",
        "u": "<:1f1fa:1126860443424665600> ",
        "v": "<:1f1fb:1126860446499094589> ",
        "w": "<:1f1fc:1127677059859238973> ",
        "x": "<:1f1fd:1126860452442411128> ",
        "y": "<:1f1fe:1126860455651061820> ",
        "z": "<:1f1ff:1126860457186181120> ",
    },
    "gray": {
        "a": "<:1f1e6:1126863966153474060>",
        "b": "<:1f1e7:1126863969366323211>",
        "c": "<:1f1e8:1126863970968551505>",
        "d": "<:1f1e9:1126863974068133928>",
        "e": "<:1f1ea:1126863976312078478>",
        "f": "<:1f1eb:1126863979025801276>",
        "g": "<:1f1ec:1126863980477030501>",
        "h": "<:1f1ed:1126863982905524245>",
        "i": "<:1f1ee:1126863984402890892>",
        "j": "<:1f1ef:1126863985644404859>",
        "k": "<:1f1f0:1126863989075345419>",
        "l": "<:1f1f1:1126863991831015484>",
        "m": "<:1f1f2:1126863993735221350>",
        "n": "<:1f1f3:1126863996365045761>",
        "o": "<:1f1f4:1126863998177005620>",
        "p": "<:1f1f5:1127679116376805496>",
        "q": "<:1f1f6:1126864001918312648>",
        "r": "<:1f1f7:1127679119245717555>",
        "s": "<:1f1f8:1126864007224102942>",
        "t": "<:1f1f9:1126864010185297993>",
        "u": "<:1f1fa:1126864012274044938>",
        "v": "<:1f1fb:1126864015558180987>",
        "w": "<:1f1fc:1127679121296719993>",
        "x": "<:1f1fd:1126864021841260675>",
        "y": "<:1f1fe:1126864024592715837>",
        "z": "<:1f1ff:1126864026568228995>",
    },
}


def generate_colored_word(guess: str, answer: str) -> str:
    """
    Builds a string of emoji codes where each letter is
    colored based on the key:

    - Same letter, same place: Green
    - Same letter, different place: Yellow
    - Different letter: Gray

    Args:
        word (str): The word to be colored
        answer (str): The answer to the word

    Returns:
        str: A string of emoji codes
    """
    colored_word = [EMOJI_CODES["gray"][letter] for letter in guess]
    guess_letters: List[Optional[str]] = list(guess)
    answer_letters: List[Optional[str]] = list(answer)
    # change colors to green if same letter and same place
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    # change colors to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return "".join(colored_word)


def generate_blanks() -> str:
    """
    Generate a string of 5 blank white square emoji characters

    Returns:
        str: A string of white square emojis
    """
    return "\N{WHITE MEDIUM SQUARE}" * 5


def generate_puzzle_embed(user: nextcord.User, puzzle_id: int) -> nextcord.Embed:
    """
    Generate an embed for a new puzzle given the puzzle id and user

    Args:
        user (nextcord.User): The user who submitted the puzzle
        puzzle_id (int): The puzzle ID

    Returns:
        nextcord.Embed: The embed to be sent
    """
    embed = nextcord.Embed(title="Wordle Clone")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱ Начините игру с - /play!\n"
        "Что бы угадать, ответьте  на сообщение со словом"
    )
    return embed


def update_embed(embed: nextcord.Embed, guess: str) -> nextcord.Embed:
    """
    Updates the embed with the new guesses

    Args:
        embed (nextcord.Embed): The embed to be updated
        puzzle_id (int): The puzzle ID
        guess (str): The guess made by the user

    Returns:
        nextcord.Embed: The updated embed
    """
    puzzle_id = int(embed.footer.text.split()[1])
    answer = popular_words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    # replace the first blank with the colored word
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # check for game over
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if num_empty_slots == 0:
            embed.description += "\n\nPhew!"
        if num_empty_slots == 1:
            embed.description += "\n\nGreat!"
        if num_empty_slots == 2:
            embed.description += "\n\nSplendid!"
        if num_empty_slots == 3:
            embed.description += "\n\nImpressive!"
        if num_empty_slots == 4:
            embed.description += "\n\nMagnificent!"
        if num_empty_slots == 5:
            embed.description += "\n\nGenius!"
    elif num_empty_slots == 0:
        embed.description += f"\n\nThe answer was/Ответом было {answer}!"
    return embed


def is_valid_word(word: str) -> bool:
    """
    Validates a word

    Args:
        word (str): The word to validate

    Returns:
        bool: Whether the word is valid
    """
    return word in all_words


def random_puzzle_id() -> int:
    """
    Generates a random puzzle ID

    Returns:
        int: A random puzzle ID
    """
    return random.randint(0, len(popular_words) - 1)


def daily_puzzle_id() -> int:
    """
    Calculates the puzzle ID for the daily puzzle

    Returns:
        int: The puzzle ID for the daily puzzle
    """
    # calculate days since 1/1/2022 and mod by the number of puzzles
    num_words = len(popular_words)
    time_diff = datetime.datetime.now().date() - datetime.date(2022, 1, 1)
    return time_diff.days % num_words


def is_game_over(embed: nextcord.Embed) -> bool:
    """
    Checks if the game is over in the embed

    Args:
        embed (nextcord.Embed): The embed to check

    Returns:
        bool: Whether the game is over
    """
    return "\n\n" in embed.description


def generate_info_embed() -> nextcord.Embed:
    """
    Generates an embed with information about the bot

    Returns:
        nextcord.Embed: The embed to be sent
    """
    join_url = "https://discord.com/oauth2/authorize?client_id=1125452899145744544&permissions=8&scope=bot"
    discord_url = "https://vk.com/veracept"
    discord_url1 = "https://docs.google.com/document/d/1M1ZxSnzi0i22BkW1vg17XkDKgW4-6fRT6CS7LJa7Asw/edit?usp=sharing"
    return nextcord.Embed(
        title="О Discord Wordle",
        description=(
            "Discord Wordle — это игра-головоломка, где нужно угадать слово из 5 букв, с 6 попыток.\n\n"
            "На данный момент слова можно угадать только на английском языке.\n\n"
            "**Вы можете начать игру с помощью:**\n\n"
            ":sunny: `/play daily` - ежедневная игра\n"
            ":game_die: `/play random` - случайный пазл\n"
            ":boxing_glove: `/play id <puzzle_id>` - играть с помощью id(всего id 2990)\n\n"
            f":incoming_envelope:  Добавить бота к себе на [сервер]({join_url})\n"
            f":newspaper: Все слова, которые используются в боте находятся в этом [файле(drive.google)]({discord_url1})\n"
            f"<:vk_logo_icon_134603:1127918115423002645> Если нашли баг, обязательно напишите мне в [ВКонтакте]({discord_url})\n"
            
        ),
    )


async def process_message_as_guess(bot: nextcord.Client, message: nextcord.Message) -> bool:
    """
    Check if a new message is a reply to a Wordle game.
    If so, validate the guess and update the bot's message.

    Args:
        bot (nextcord.Client): The bot
        message (nextcord.Message): The new message to process

    Returns:
        bool: True if the message was processed as a guess, False otherwise
    """
    # get the message replied to
    ref = message.reference
    if not ref or not isinstance(ref.resolved, nextcord.Message):
        return False
    parent = ref.resolved

    # if the parent message is not the bot's message, ignore it
    if parent.author.id != bot.user.id:
        return False

    # check that the message has embeds
    if not parent.embeds:
        return False

    embed = parent.embeds[0]

    guess = message.content.lower()

    # check that the user is the one playing
    if (
        embed.author.name != message.author.name
        or embed.author.icon_url != message.author.display_avatar.url
    ):
        reply = "Start a new game with /play / Начните новую игру с /play"
        if embed.author:
            reply = f"This game was started by/Эту игру начал {embed.author.name}. " + reply
        await message.reply(reply, delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the game is not over
    if is_game_over(embed):
        await message.reply("The game is already over. Start a new game with /play /Игра уже окончена. Начните новую игру с /play", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # strip mentions from the guess
    guess = re.sub(r"<@!?\d+>", "", guess).strip()

    bot_name = message.guild.me.nick if message.guild and message.guild.me.nick else bot.user.name

    if len(guess) == 0:
        await message.reply(
            "I am unable to see what you are trying to guess.\n"
            "Please try mentioning me in your reply before the word you want to guess.\n\n"
            f"**For example:**\n{bot.user.mention} crate\n\n"
            f"To bypass this restriction, you can start a game with `@\u200b{bot_name} play` instead of `/play`",
            delete_after=14,
        )
        try:
            await message.delete(delay=14)
        except Exception:
            pass
        return True

    # check that a single word is in the message
    if len(guess.split()) > 1:
        await message.reply("Please respond with a single 5-letter word/Пожалуйста введите слово из 5 букв", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the word is valid
    if not is_valid_word(guess):
        await message.reply("That is not a valid word/Это неизвестное слово", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # update the embed
    embed = update_embed(embed, guess)
    await parent.edit(embed=embed)

    # attempt to delete the message
    try:
        await message.delete()
    except Exception:
        pass

    return True
