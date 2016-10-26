## `loggerbot`

Simple Telegram bot that logs chat messages.

## Running

```sh
python3 bot.py --token <TOKEN> messages.sqlite3
```

Bot API token can be also specified via `LOGGER_BOT_TELEGRAM_TOKEN` environment variable.

Messages are logged into the `messages` table.