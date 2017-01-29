#!/usr/bin/env python3
# coding: utf-8

import asyncio
import logging
import socket
import sqlite3
import typing

import aiohttp
import aiotg
import click


@click.command()
@click.option("-t", "--token", help="Telegram Bot API token.", required=True, envvar="LOGGER_BOT_TELEGRAM_TOKEN")
@click.option("-v", "--verbose", help="Increase verbosity.", is_flag=True)
@click.option("-l", "--log-file", help="Log file.", type=click.File("at", encoding="utf-8"))
@click.argument("database", type=click.Path(dir_okay=False, writable=True))
def main(token: str, verbose: bool, log_file: typing.io.TextIO, database: str):
    """
    Simple Telegram bot that logs chat messages.
    """
    logging.basicConfig(
        format="%(asctime)s [%(levelname).1s] %(message)s",
        level=(logging.INFO if not verbose else logging.DEBUG),
        stream=(log_file or click.get_text_stream("stderr")),
        datefmt="%m-%d %H:%M:%S",
    )

    logging.info("Creating database…")
    db = sqlite3.connect(database)
    create_database(db)

    logging.info("Running…")
    try:
        asyncio.get_event_loop().run_until_complete(async_main(token, db))
    except Exception as ex:
        logging.critical("Critical error.", exc_info=ex)


def create_database(db: sqlite3.Connection):
    """
    Initializes the database.
    """
    try:
        with db:
            db.executescript("""
                CREATE TABLE messages (
                    timestamp INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    from_user_id INTEGER NOT NULL,
                    text TEXT NOT NULL
                );
            """)
    except sqlite3.OperationalError:
        logging.info("Table is already created.")
    else:
        logging.info("Created table.")


async def async_main(token: str, db: sqlite3.Connection):
    """
    Runs bot on async I/O loop.
    """
    connector = aiohttp.TCPConnector(family=socket.AF_INET, verify_ssl=False)
    await aiotg.LongPollingRunner(aiotg.Telegram(token, connector=connector), Bot(db)).run()


class Bot(aiotg.Bot):
    """
    Logs every received text message to the database.
    """

    def __init__(self, db: sqlite3.Connection):
        self.db = db

    async def on_update(self, telegram: aiotg.Telegram, update: aiotg.Update):
        message = update.message
        if not message or not message.text:
            return
        with self.db:
            self.db.execute("""
                    INSERT INTO messages (timestamp, chat_id, from_user_id, `text`)
                    VALUES (?, ?, ?, ?)
                """,
                (int(message.date.timestamp()), message.chat.id, message.from_.id, message.text))


if __name__ == "__main__":
    main()
