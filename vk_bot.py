import logging
import os
from random import randint

import vk_api
from dialogflow import detect_intent_texts
from dotenv import load_dotenv
from google.auth import exceptions as google_exceptions
from vk_api.longpoll import VkEventType, VkLongPoll

from tg_logging import MyLogsHandler


def send_answer(event, vk_api):
    project_id = os.getenv("PROJECT_ID")
    dialogflow_response = detect_intent_texts(event.user_id, event.text, project_id)
    if not dialogflow_response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_response.query_result.fulfillment_text,
            random_id=randint(1, 1000)
        )

def main():
    vk_token = os.getenv("VK_TOKEN")
    try:
        vk_session = vk_api.VkApi(token=vk_token)
    except vk_api.exceptions.ApiError:
        logger.exception('В файле .env неверный токен VK')
    vk_session_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger.info("ВК бот запущен")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                send_answer(event, vk_session_api)
            except google_exceptions.DefaultCredentialsError:
                logger.exception('Не удалось подключиться в dialogflow по запросу из ВК (скорее всего, неверно указан пусть к json-файлу в .env)')
            except vk_api.exceptions.ApiError:
                logger.exception("Не удалось отправить сообщение пользователю в ВК")
            


if __name__ == "__main__":
    load_dotenv()
    
    logger = logging.getLogger("VK_Logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())

    main()
