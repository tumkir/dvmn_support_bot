import os
from random import randint

import vk_api
from dialogflow import detect_intent_texts
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll


def send_answer(event, vk_api):
    dialogflow_response = detect_intent_texts(event.user_id, event.text, project_id)
    if dialogflow_response == 'Не совсем понимаю, о чём ты.':
        pass
    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_response,
            random_id=randint(1, 1000)
        )


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv('vk_token')
    project_id = os.getenv('project_id')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_answer(event, vk_api)
