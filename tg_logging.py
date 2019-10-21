import logging
import os

from telegram import Bot


class MyLogsHandler(logging.Handler):
    def emit(self, record):
        bot_token = os.getenv("BOT_TOKEN")
        chat_id = os.getenv("OWNER_CHAT_ID")
        log_entry = self.format(record)
        bot = Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=log_entry)
