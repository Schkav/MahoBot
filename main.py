import os
import pycountry
from dotenv import load_dotenv
from discord.ext import commands
from googletrans import Translator
from charas import Chara
from skills import Skills
from gacha import Gacha
import random
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='^', case_insensitive=True)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='chara', help='Return summary of a character', aliases=['c'])
async def chara(ctx, *names):
    chara = Chara()
    message = []
    character_to_remove = "!. "
    joined_name = "".join(names)
    name = joined_name.lower().strip()
    for character in character_to_remove:
        name = name.replace(character, "")
    summary = chara.get_page(name)
    if not summary:
        message = "Character not found, please try again"
    else:
        message = """```css
{}
    
{}

{}

{}
    ```""".format(*summary)
    await ctx.send(message)


@bot.command(name='skill', help='Return skills of a character', aliases=['s'])
async def chara(ctx, *names):
    skills = Skills()
    message = []
    character_to_remove = "!. "
    joined_name = "".join(names)
    name = joined_name.lower().strip()
    for character in character_to_remove:
        name = name.replace(character, "")
    skills_summary = skills.get_skills(name)
    if not skills_summary:
        message = "Character not found, please try again"
    else:
        message = """```css
UB
{}
    
Skill 1
{}

Skill 2
{}

Passive
{}
        ```""".format(*skills_summary)
    await ctx.send(message)


@bot.command(name='roll', help='Do a 10 roll and hope you get yuni')
async def roll(ctx, *banners):
    message = []
    gacha = Gacha()
    gacha.set_pool(banners)
    results = gacha.get_ten()

    for draw in results:
        if draw in gacha.perm_list:
            message.append("""```yaml
{}```""".format(draw))

        elif draw in gacha.special_list:
            message.append("""```fix
{}```""".format(draw))

        else:
            message.append("""```brainfuck
{}```""".format(draw))

    await ctx.send(''.join(message))


@bot.command(name='rollspark', help='Do a 200 roll and hope you get your spark target')
async def rollspark(ctx, *banners):
    message = []
    gacha = Gacha()
    gacha.set_pool(banners)
    results = gacha.get_spark()

    message.append("""```css\n
You got {} SSR in 200 rolls
Including the following 3★:```""".format(len(results)))

    for draw in results:
        if draw in gacha.special_list:
            message.append("""```fix
{}
```""".format(draw))
        else:
            message.append("""```yaml
{}```""".format(draw))

    await ctx.send(''.join(message))


@bot.command(name='spark', help='Calculate spark')
async def spark(ctx, jewels = 0, tickets = 0):
    jewel_rolls = jewels//150
    total_rolls = jewel_rolls + tickets
    percentage = (total_rolls / 200) * 100
    response = "You have {} rolls available ({:.1f}% complete)".format(total_rolls, percentage)
    await ctx.send(response)


@bot.command(name='roll?', help='Return 50:50 yes or no')
async def roll(ctx):
    yes_or_no = ['Yes, YOLO!', 'No, save up', 'Yes, do a 10', 'No, not worth it']
    response = random.choice(yes_or_no)
    await ctx.send(response)


@bot.command(name='choice', help='Return random choice from input')
async def choice(ctx, *choices):
    choice_list = []
    for item in choices:
        choice_list.append(item)
    response = random.choice(choice_list).title()
    await ctx.send(response)


@bot.command(name='translate', help='Translate [text] > [language]. Default is translate to English if without ">" sign', aliases=['tl'])
async def translate(ctx, *texts):
    translator = Translator()
    joined_text = " ".join(texts).lower()
    lan_choice = False
    for text in texts:
        if text.lower() == ">":
            lan_choice = True
    if lan_choice:
        split_text = joined_text.split('>')
        language_code = pycountry.languages.get(name=split_text[-1].strip())
        language = language_code.alpha_2
        if split_text[-1].strip().lower() == "chinese":
            language = "zh-CN"
        text_to_translate = split_text[0]
    else:
        language = "english"
        text_to_translate = joined_text
    translated_text = translator.translate(str(text_to_translate), dest=str(language))
    await ctx.send(translated_text.text)


@bot.command(name='feedback', help='Send feedback or bug report message to bot owner', aliases=['bugreport'], pass_context=True)
async def feedback(ctx, *messages):
    feedback_message = " ".join(messages)
    response = """
Your feedback has been sent to Schkav#9999.
Thank you for your feedback!"""
    await bot.get_user(209998612594294784).send("{} from {}".format(feedback_message, ctx.message.author))
    await ctx.send(response)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send('Invalid parameters. See %help for correct parameters.')


bot.run(TOKEN)
