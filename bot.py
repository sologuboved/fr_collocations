"""
cit - blank
stat - blank
all - blank
file - blank
random - 15 or blank
tag - divers
tags - blank
"""

import logging
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from global_vars import FILE_PATH
from helpers import PIDWriter, check_auth, get_chat_id
from command_processors import by_random, by_tag, get_citation, get_stats, get_tags, get_all
from data_processors import list_to_texts, lists_to_texts
from userinfo import TELETOKEN
from write import to_email, to_txt

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


async def send_help(update, context):
    # /help
    await context.bot.send_message(
        chat_id=get_chat_id(update),
        text="""Commands:
/cit
/all
/email
/file
/random 15
/stat
/tag divers
/tags""",
    )


async def send_citation(update, context):
    # /cit
    await context.bot.send_message(
        chat_id=get_chat_id(update),
        text=get_citation(),
    )


async def send_stats(update, context):
    # /stat
    await context.bot.send_message(
        chat_id=get_chat_id(update),
        text=get_stats(),
    )


async def send_all(update, context):
    # /all
    for text in lists_to_texts(get_all()):
        await context.bot.send_message(
            chat_id=get_chat_id(update),
            text=text,
        )
        time.sleep(2)


@check_auth
async def send_email(update, context):
    # /email
    for func in (to_txt, to_email):
        caption = func(FILE_PATH)
        await context.bot.send_message(
            chat_id=get_chat_id(update),
            text=caption,
        )
        time.sleep(1)


async def send_file(update, context):
    # /file
    caption = to_txt(FILE_PATH)
    await context.bot.send_document(
        chat_id=get_chat_id(update),
        document=FILE_PATH,
        caption=caption,
    )


async def send_random(update, context):
    # /rndm 15
    query = update['message']['text'].split()
    try:
        query = int(query[1].strip())
    except IndexError:
        query = None
    except ValueError:
        await context.bot.send_message(
            chat_id=get_chat_id(update),
            text="Il fallait en fait que ce soit un nombre entier, mais bon.",
        )
        time.sleep(2)
        query = None
    for text in list_to_texts(by_random(query), with_tag=True):
        await context.bot.send_message(
            chat_id=get_chat_id(update),
            text=text,
        )
        time.sleep(2)


async def send_tag(update, context):
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


async def send_tags(update, context):
    # /tags
    keyboard = [[InlineKeyboardButton(tag, callback_data=tag)] for tag in get_tags()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Voilà :", reply_markup=reply_markup)


async def tag_button(update, context):
    query = update.callback_query
    await query.answer()
    tag = query.data
    await query.edit_message_text(text=f"Tag sélectionné : {tag}")
    for text in list_to_texts(by_tag(tag), with_tag=False):
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=text,
        )
        time.sleep(2)


def main():
    application = Application.builder().token(TELETOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', send_help))
    application.add_handler(CommandHandler('cit', send_citation))
    application.add_handler(CommandHandler('stat', send_stats))
    application.add_handler(CommandHandler('all', send_all))
    application.add_handler(CommandHandler('email', send_email))
    application.add_handler(CommandHandler('file', send_file))
    application.add_handler(CommandHandler('random', send_random))
    application.add_handler(CommandHandler('tag', send_tag))
    application.add_handler(CommandHandler('tags', send_tags))
    application.add_handler(CallbackQueryHandler(tag_button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    with PIDWriter():
        main()
