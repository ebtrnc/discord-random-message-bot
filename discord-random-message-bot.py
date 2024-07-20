import discord
from discord.ext import commands
import random
import asyncio

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
    await send_random_message(ctx)

async def send_random_message(ctx):
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
        
        # 画像のURLを抽出
        if random_message.attachments:
            image_urls = [attachment.url for attachment in random_message.attachments]
            response = f'> {random_message.content}\n{message_link}\n' + '\n'.join(image_urls)
        else:
            response = f'> {random_message.content}\n{message_link}'
        
        await target_channel.send(response)
    else:
        await ctx.send('メッセージが見つかりませんでした。')

async def keep_bot_running():
    while True:
        try:
            await bot.start(TOKEN)
        except discord.errors.ConnectionClosed:
            print("Connection closed, reconnecting...")
            await asyncio.sleep(5)

# エントリーポイント
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(keep_bot_running())
