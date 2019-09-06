import os

from dialogflow import detect_intent_texts
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from tg_logging import start_logger


def start(bot, update):
    update.message.reply_text('Здравствуйте')


def send_answer(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text
    project_id = os.getenv('PROJECT_ID')
    try:
        dialogflow_response = detect_intent_texts(chat_id, message, project_id)
        update.message.reply_text(dialogflow_response.query_result.fulfillment_text)
    except Exception:
        logger.warning('Невозможно обратиться к dialogflow')


def main():
    bot_token = os.getenv('BOT_TOKEN')
    updater = Updater(bot_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, send_answer))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    load_dotenv()
    logger = start_logger(Bot(os.getenv('BOT_TOKEN')), os.getenv('OWNER_CHAT_ID'))
    main()
