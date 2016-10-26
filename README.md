## `loggerbot`

Simple Telegram bot that logs chat messages.

## Running

```sh
python3 bot.py --token <TOKEN> messages.sqlite3
```

Bot API token can be also specified via `LOGGER_BOT_TELEGRAM_TOKEN` environment variable.

Messages are logged into the `messages` table.

## systemd

```sh
$ cd
$ git clone git@github.com:eigenein/loggerbot.git
$ git clone git@gitlab.com:eigenein/dotfiles.git
$ sudo systemctl link /home/eigenein/loggerbot/loggerbot.service
$ cd /etc/systemd/system
$ sudo ln -s /home/eigenein/dotfiles/loggerbot.service.d loggerbot.service.d
$ sudo systemctl start loggerbot
```
