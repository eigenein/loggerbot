#!/usr/bin/env python3
# coding: utf-8

import asyncio
import logging
import sqlite3
import typing

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
    offset = 0
    async with aiotg.Telegram(token) as telegram:  # type: aiotg.Telegram
        while True:
            updates = await telegram.get_updates(offset, 100, 5)
            if not updates:
                continue
            for update in updates:
                logging.info("Received update #%s.", update.id)
                logging.debug("Received update: %s", update)
                try:
                    await handle_update(update, db)
                except Exception as ex:
                    logging.error("Error while handling update.", exc_info=ex)
            offset = updates[-1].id + 1


async def handle_update(update: aiotg.Update, db: sqlite3.Connection):
    """
    Handles single update.
    """
    message = update.message
    if not message or not message.text:
        return
    with db:
        db.execute("""
            INSERT INTO messages (timestamp, chat_id, from_user_id, `text`)
            VALUES (?, ?, ?, ?)
        """, (int(message.date.timestamp()), message.chat.id, message.from_.id, message.text))


if __name__ == "__main__":
    main()
