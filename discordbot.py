import discord
import os
from gpt import *
from discord.ext import commands
from gpt import BOTNAME, CHARACTER, RELATIONSHIP
from datetime import datetime
from pytz import timezone

BOT_KEY = os.environ['BOT_KEY']
bot = commands.Bot(command_prefix='', intents=discord.Intents.all())

boot_time = datetime.now()

async def send_text(text, ctx):
    segments = text_to_segments(text)
    for segment in segments:
        if segment.strip():
            await ctx.message.channel.send(segment)


@bot.event
async def on_ready():
    global boot_time
    boot_time = datetime.now(timezone('Asia/Seoul'))
    print(f'Login bot: {bot.user}')
 

@bot.command(name=f'{BOTNAME}야,')
async def response(ctx):
    message = ctx.message
    async with ctx.typing():
        text = message.content[len(BOTNAME)+2:].strip()
        if len(text) > 500:
            answer = str(f'{message.author.mention}님, 질문이 너무 길어요!')
        else:
            answer = str(f'{message.author.mention}님, {ask(text, message.author.nick)}')
        await send_text(answer, ctx)


@bot.command(name='$$memory')
async def get_memory(ctx):
    await ctx.message.channel.send(f'{get_log().size}개의 대화를 기억하고 있습니다.')
    await ctx.message.channel.send(f'마지막 초기화 시간은 {boot_time}입니다.')
    

@bot.command(name='$$clear')
async def clear_memory(ctx):
    global boot_time
    clear_log()
    boot_time = datetime.now(timezone('Asia/Seoul'))
    await ctx.message.channel.send(f'기억을 초기화 했습니다.')


@bot.command(name='$$character')
async def change_character(ctx, *args):
    global CHARACTER, RELATIONSHIP
    args = ' '.join(args)
    if args.strip() == '':
        await ctx.message.channel.send(f"저는 '{CHARACTER}'이고, 당신은 '{RELATIONSHIP}'입니다.")
    else:
        character, relationship = args.split(',')
        character, relationship = character.strip(), relationship.strip()
        set_character(character, relationship)
        CHARACTER, RELATIONSHIP = character, relationship
        clear_log()
        await ctx.message.channel.send(f"저는 '{character}'이고, 당신은 '{relationship}'입니다.")

bot.run(BOT_KEY)
