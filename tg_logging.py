import logging


def start_logger(bot, chat_id):
    class MyLogsHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            bot.send_message(chat_id=chat_id, text=log_entry)

    logger = logging.getLogger('Bot_loger')
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    logger.info('Бот запущен')
    return logger
