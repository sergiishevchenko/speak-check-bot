import logging
import random
import telebot
import vk_api as vk

from google_methods.set_intent import set_intent
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.vk_api import VkApiMethod

logger = logging.getLogger('telegram_logging')


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.tg_bot = tg_bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_to_vk(event, vk_api: VkApiMethod, env: Env):
    message, is_correct = set_intent(env('PROJECT_ID'), event.user_id, event.text, language_code='ru-RU')
    if is_correct:
        vk_api.messages.send(user_id=event.user_id, message=message, random_id=random.randint(1, 1000))


if __name__ == "__main__":
    env = Env()
    env.read_env()

    bot = telebot.TeleBot(env('TG_BOT_TOKEN'))

    logger.addHandler(TelegramLogsHandler(bot, chat_id=env('TG_CHAT_ID')))
    logger.setLevel('INFO')

    vk_session = vk.VkApi(token=env('VK_GROUP_TOKEN'))
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_to_vk(event, vk_api, env)
