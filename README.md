# discord-random-message-bot
discordのログをランダムで表示するbot（ChatGPT作）

### 書き換える箇所
> TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # あなたのボットのトークン

> SOURCE_CHANNEL_IDS = [YOUR_CHANNEL_ID_1, YOUR_CHANNEL_ID_2]  # メッセージを取得したい<ins>**複数の**</ins>チャンネルのID

> TARGET_CHANNEL_ID = YOUR_TARGET_CHANNEL_ID  # メッセージを送信したい出力先のチャンネルのID

### 実行方法
コマンドラインでpythonを実行
> $ python3 discord-random-message-bot.py

メッセージを送信したい出力先のチャネンルでコマンドを入力
> !ran
