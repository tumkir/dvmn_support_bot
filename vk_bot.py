import logging
import os
from random import randint

from vk_api import VkApi
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow import detect_intent_texts
from tg_logging import MyLogsHandler


def send_answer(event, vk_api):
    project_id = os.getenv("PROJECT_ID")
    try:
        dialogflow_response = detect_intent_texts(event.user_id, event.text, project_id)
    except Exception:
        logger.warning("Невозможно обратиться к dialogflow по запросу из ВК")
    if dialogflow_response.query_result.intent.is_fallback is not True:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_response.query_result.fulfillment_text,
            random_id=randint(1, 1000)
        )

def main():
    vk_token = os.getenv("VK_TOKEN")
    try:
        vk_session = VkApi(token=vk_token)
        vk_session_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        logger.info("ВК бот запущен")
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                send_answer(event, vk_session_api)
    except Exception:
        logger.warning("Невозможно подключиться к ВК")


if __name__ == "__main__":
    load_dotenv()
    
    logger = logging.getLogger("VK_Logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())

    main()
