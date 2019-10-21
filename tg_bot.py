import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dialogflow import detect_intent_texts
from tg_logging import MyLogsHandler


def start(bot, update):
    update.message.reply_text("Здравствуйте")


def send_answer(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text
    project_id = os.getenv("PROJECT_ID")
    try:
        dialogflow_response = detect_intent_texts(chat_id, message, project_id)
        update.message.reply_text(dialogflow_response.query_result.fulfillment_text)
    except Exception:
        logger.warning("Невозможно обратиться к dialogflow по запросу из Телеграма")


def main():
    bot_token = os.getenv("BOT_TOKEN")
    updater = Updater(bot_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, send_answer))

    logger.info("Телеграм бот запущен")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    load_dotenv()

    logger = logging.getLogger("TG_Logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())

    main()
