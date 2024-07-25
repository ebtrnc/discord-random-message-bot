# discord-random-message-bot
discord内全てのチャンネルからランダムで11件メッセージを表示するbot（ChatGPT作）

### 書き換える箇所
> TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # あなたのボットのトークン

> TARGET_CHANNEL_ID = YOUR_TARGET_CHANNEL_ID  # メッセージを送信したい出力先のチャネルのID

> EXCLUDED_CHANNEL_IDS = [EXCLUDED_CHANNEL_ID_1, EXCLUDED_CHANNEL_ID_2]  # 除外するチャンネルのIDリスト

> ALLOWED_CHANNEL_IDS = [ALLOWED_CHANNEL_ID_1, ALLOWED_CHANNEL_ID_2]  # コマンド実行を許可するチャンネルのIDリスト

### 実行方法
コマンドラインでpythonを実行
> $ python3 discord-random-message-bot.py

ランダムで11件表示するコマンド（メッセージを送信したい出力先のチャンネルで実行すること）
> !11

取得したメッセージ.jsonを更新するコマンド
> !11-json
