import discord
from discord.ext import commands
import random

# Intentsを設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得するために必要

# ボットの接頭辞を設定
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # あなたのボットのトークン
SOURCE_CHANNEL_IDS = [YOUR_CHANNEL_ID_1, YOUR_CHANNEL_ID_2]  # メッセージを取得したい複数のチャネルのID
TARGET_CHANNEL_ID = YOUR_TARGET_CHANNEL_ID  # メッセージを送信したい出力先のチャネルのID

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='run')
async def random_message(ctx):
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if target_channel is None:
        await ctx.send(f'出力先のチャンネルID {TARGET_CHANNEL_ID} が見つかりません。')
        return
    
    all_messages = []
    
    for channel_id in SOURCE_CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel is None:
            await ctx.send(f'メッセージ取得元のチャンネルID {channel_id} が見つかりません。')
            continue
        
        messages = []
        async for message in channel.history(limit=100):  # 最新の100件のメッセージを取得
            messages.append(message)
        
        all_messages.extend(messages)
    
    if all_messages:
        random_message = random.choice(all_messages)
        message_link = f"https://discord.com/channels/{random_message.guild.id}/{random_message.channel.id}/{random_message.id}"
        response = f'ランダムなメッセージ: {random_message.content}\nメッセージのリンク: {message_link}'
        await target_channel.send(response)
    else:
        await ctx.send('メッセージが見つかりませんでした。')

bot.run(TOKEN)
