import discord
from discord.ext import commands
import random
import asyncio
import os
import json

# Intentsを設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得するために必要

# ボットの接頭辞を設定
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # あなたのボットのトークン
TARGET_CHANNEL_ID = YOUR_TARGET_CHANNEL_ID  # メッセージを送信したい出力先のチャネルのID
DATA_FILE = os.path.join(os.path.dirname(__file__), 'saved_messages.json')  # 保存するファイルの名前
EXCLUDED_CHANNEL_IDS = [EXCLUDED_CHANNEL_ID_1, EXCLUDED_CHANNEL_ID_2]  # 除外するチャンネルのIDリスト
ALLOWED_CHANNEL_IDS = [ALLOWED_CHANNEL_ID_1, ALLOWED_CHANNEL_ID_2]  # コマンド実行を許可するチャンネルのIDリスト

def message_to_dict(message):
    return {
        'id': message.id,
        'channel': {
            'id': message.channel.id
        },
        'guild': {
            'id': message.guild.id
        },
        'content': message.content,
        'author': {
            'id': message.author.id,
            'name': message.author.name
        },
        'attachments': [{'url': attachment.url} for attachment in message.attachments]
    }

async def save_messages(messages):
    try:
        if messages:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=4)
            print(f'メッセージの保存が完了しました。ファイルパス: {DATA_FILE}')
        else:
            print('保存するメッセージがありません')
    except Exception as e:
        print(f'メッセージの保存中にエラーが発生しました: {e}')

def load_messages():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = f.read().strip()
                if not data:
                    print('JSONファイルが空です')
                    return []
                return json.loads(data)
        except json.JSONDecodeError as e:
            print(f'JSONの読み込み中にエラーが発生しました: {e}')
            return []
        except Exception as e:
            print(f'ファイルの読み込み中にエラーが発生しました: {e}')
            return []
    else:
        print('データファイルが存在しません')
        return []

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='11')
async def random_message(ctx):
    # コマンド実行を許可されたチャンネルでのみ実行
    if ctx.channel.id not in ALLOWED_CHANNEL_IDS:
        await ctx.send('このチャンネルではコマンドを実行できません。')
        return

    try:
        all_messages = load_messages()

        if not all_messages:
            # JSONファイルが存在しない場合は全メッセージを取得して保存する
            await ctx.send('初回起動です。メッセージを取得しています...')
            all_messages = await retrieve_and_save_messages(ctx)
        else:
            await ctx.send('保存されたメッセージを表示します...')
        
        if all_messages:
            random_messages = random.sample(all_messages, min(11, len(all_messages)))  # 11件のメッセージをランダムに選択
            target_channel = bot.get_channel(TARGET_CHANNEL_ID)
            if target_channel is None:
                await ctx.send(f'出力先のチャンネルID {TARGET_CHANNEL_ID} が見つかりません。')
                return
            
            for random_message in random_messages:
                message_link = f"https://discord.com/channels/{random_message['guild']['id']}/{random_message['channel']['id']}/{random_message['id']}"
                
                # 画像のURLを抽出
                if random_message.get('attachments'):
                    image_urls = [attachment['url'] for attachment in random_message['attachments']]
                    response = f'> {random_message.get("content")}\n{message_link}\n' + '\n'.join(image_urls)
                else:
                    response = f'> {random_message.get("content")}\n{message_link}'
                
                await target_channel.send(response)
            await ctx.send('メッセージの書き込みが完了しました。')  # 完了メッセージを送信
            print('メッセージの書き込みが完了しました')
        else:
            await ctx.send('メッセージが見つかりませんでした。')

    except Exception as e:
        print(f'コマンド実行中にエラーが発生しました: {e}')
        await ctx.send('コマンド実行中にエラーが発生しました。')

@bot.command(name='11-json')
async def update_json(ctx):
    # コマンド実行を許可されたチャンネルでのみ実行
    if ctx.channel.id not in ALLOWED_CHANNEL_IDS:
        await ctx.send('このチャンネルではコマンドを実行できません。')
        return

    try:
        await ctx.send('全メッセージを再取得してJSONファイルを更新します...')
        all_messages = await retrieve_and_save_messages(ctx)
        if all_messages:
            await ctx.send('JSONファイルの更新が完了しました。')
        else:
            await ctx.send('メッセージが見つかりませんでした。')
    except Exception as e:
        print(f'コマンド実行中にエラーが発生しました: {e}')
        await ctx.send('コマンド実行中にエラーが発生しました。')

async def retrieve_and_save_messages(ctx):
    all_messages = []

    # サーバー内の全チャンネルIDを取得し、除外チャンネルをフィルタリング
    source_channel_ids = [channel.id for channel in ctx.guild.channels if isinstance(channel, discord.TextChannel) and channel.id not in EXCLUDED_CHANNEL_IDS]
    print(f'チャンネルIDの取得が完了しました: {source_channel_ids}')

    for channel_id in source_channel_ids:
        channel = bot.get_channel(channel_id)
        if channel is None:
            await ctx.send(f'メッセージ取得元のチャンネルID {channel_id} が見つかりません。')
            continue

        messages = []
        try:
            async for message in channel.history(limit=None):  # 全メッセージを取得
                messages.append(message_to_dict(message))
            print(f'チャンネル {channel_id} から {len(messages)} 件のメッセージを取得しました')
        except Exception as e:
            print(f'チャンネル {channel_id} のメッセージ取得中にエラーが発生しました: {e}')
        
        all_messages.extend(messages)

    print(f'全メッセージの取得が完了しました。合計メッセージ数: {len(all_messages)}')
    await save_messages(all_messages)
    return all_messages

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
