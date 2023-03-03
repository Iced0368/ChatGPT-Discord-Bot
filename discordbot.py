import discord
import os
from gpt import *
from discord.ext import commands
from bot_manager import BotManager

BOT_KEY = os.environ['BOT_KEY']
BOTNAME = 'gptBot'

intents = intents=discord.Intents.all()
bot = commands.Bot(command_prefix='', intents=intents)
manager = BotManager()

async def send_text(text, ctx):
    segments = text_to_segments(text)
    for segment in segments:
        if segment.strip():
            await ctx.message.channel.send(segment)

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')


@bot.event
async def on_member_remove(member):
    if member.bot and member.name == BOTNAME:
        server_id = member.guild.id
        manager.removeBot(server_id)
        print(f"The bot was kicked out of server {server_id}")
 

@bot.command(name=f'{BOTNICK}야,')
async def response(ctx):
    message = ctx.message
    Bot = manager.get(ctx.guild.id)
    async with ctx.typing():
        text = message.content[len(BOTNICK)+2:].strip()
        if len(text) > 500:
            answer = str(f'{message.author.mention}님, 질문이 너무 길어요!')
        else:
            username = message.author.nick
            if username is None:
                username = message.author.name
            answer = str(f'{message.author.mention}님, {Bot.ask(text, username)}')
        await send_text(answer, ctx)


@bot.command(name='$$memory')
async def get_memory(ctx):
    Bot = manager.get(ctx.guild.id)
    await ctx.message.channel.send(f'{Bot.get_log().size}개의 대화를 기억하고 있습니다.')
    await ctx.message.channel.send(f'마지막 초기화 시간은 {Bot.boot_time}입니다.')
    

@bot.command(name='$$clear')
async def clear_memory(ctx):
    Bot = manager.get(ctx.guild.id)
    Bot.clear_log()
    boot_time = datetime.now(timezone('Asia/Seoul'))
    await ctx.message.channel.send(f'기억을 초기화 했습니다.')


@bot.command(name='$$character')
async def change_character(ctx, *args):
    Bot = manager.get(ctx.guild.id)
    args = ' '.join(args)
    if args.strip() == '':
        await ctx.message.channel.send(f"저는 '{Bot.CHARACTER}'이고, 당신은 '{Bot.RELATIONSHIP}'입니다.")
    else:
        character, relationship = args.split(',')
        character, relationship = character.strip(), relationship.strip()
        Bot.set_character(character, relationship)
        Bot.clear_log()
        await ctx.message.channel.send(f"저는 '{character}'이고, 당신은 '{relationship}'입니다.")

bot.run(BOT_KEY)
