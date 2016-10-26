#!/usr/bin/env python3
# coding: utf-8

import asyncio
import logging
import typing

import aiotg
import click


@click.command()
@click.option("-t", "--token", help="Telegram Bot API token.", required=True, envvar="LOGGER_BOT_TELEGRAM_TOKEN")
@click.option("-v", "--verbose", help="Increase verbosity.", is_flag=True)
@click.option("-l", "--log-file", help="Log file.", type=click.File("at", encoding="utf-8"))
def main(token: str, verbose: bool, log_file: typing.io.TextIO):
    """
    Simple Telegram bot that logs chat messages.
    """
    logging.basicConfig(
        format="%(asctime)s [%(levelname).1s] %(message)s",
        level=(logging.INFO if not verbose else logging.DEBUG),
        stream=(log_file or click.get_text_stream("stderr")),
        datefmt="%m-%d %H:%M:%S",
    )
    asyncio.get_event_loop().run_until_complete(async_main(token))


async def async_main(token: str):
    offset = 0
    async with aiotg.Telegram(token) as telegram:  # type: aiotg.Telegram
        while True:
            updates = await telegram.get_updates(offset, 100, 5)
            if not updates:
                continue
            for update in updates:
                logging.debug("Got update: %s", update)
            offset = updates[-1].id + 1


if __name__ == "__main__":
    main()
