import os
import random
import vk_api as vk

from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_session = vk.VkApi(token=os.getenv("VK_GROUP_TOKEN"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
