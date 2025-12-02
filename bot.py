"""
file - blank
random - 15 or blank
tag - divers
tags - blank
"""

import logging
import time

from telegram.ext import Application, CommandHandler

from db_ops import to_txt
from global_vars import DEFAULT_NUM
from helpers import PIDWriter, get_chat_id
from command_processors import by_tag, by_num
from data_processors import list_to_texts
from userinfo import TELETOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
)


async def start(update, context):
    # /start
    await context.bot.send_message(
        chat_id=get_chat_id(update),
        text="=-*=-*-=*-=",
    )


async def info(update, context):
    # /help
    await context.bot.send_message(
        chat_id=get_chat_id(update),
        text="""Commands:
/email
/file
/random 15
/tag divers
/tags""",
    )


async def email(update, context):
    # /email
    ...


async def file(update, context):
    # /file
    filename = 'collocations.txt'
    caption = to_txt(filename)
    await context.bot.send_document(
        chat_id=get_chat_id(update),
        document=filename,
        caption=caption,
    )


async def rndm(update, context):
    # /rndm 15
    query = update['message']['text'].split()
    try:
        query = int(query[1].strip())
    except IndexError:
        query = DEFAULT_NUM
    except ValueError:
        await context.bot.send_message(
            chat_id=get_chat_id(update),
            text="Il fallait en fait que ce soit un nombre entier, mais bon.",
        )
        time.sleep(2)
        query = DEFAULT_NUM
    for text in list_to_texts(by_num(query), with_tag=True):
        await context.bot.send_message(
            chat_id=get_chat_id(update),
            text=text,
        )
        time.sleep(2)


async def tag(update, context):
    # /tag divers
    query = update['message']['text'].split()
    try:
        query = query[1].strip()
    except IndexError:
        await context.bot.send_message(
                chat_id=get_chat_id(update),
                text="Il est nécessaire de fournir une tag.",
            )
    else:
        for text in list_to_texts(by_tag(query), with_tag=False):
            await context.bot.send_message(
                chat_id=get_chat_id(update),
                text=text,
            )
            time.sleep(2)


async def tags(update, context):
    # /tags
    query = update['message']['text']
    print('query:', query)
    query = query.split()
    try:
        query = query[1]
    except IndexError:
        query = ''
    # text = date_to_string(get_nth_day(query))
    # await context.bot.send_message(
    #     chat_id=get_chat_id(update),
    #     text=text,
    # )


def main():
    application = Application.builder().token(TELETOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', info))
    application.add_handler(CommandHandler('email', email))
    application.add_handler(CommandHandler('file', file))
    application.add_handler(CommandHandler('random', rndm))
    application.add_handler(CommandHandler('tag', tag))
    application.add_handler(CommandHandler('tags', tags))

    application.run_polling()


if __name__ == '__main__':
    with PIDWriter():
        main()
