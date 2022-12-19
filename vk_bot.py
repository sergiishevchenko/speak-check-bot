import logging
import os
import random
import telebot
import vk_api as vk

from dotenv import load_dotenv
from google_methods.get_intent import get_intent
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


def send_to_vk(event, project_id, vk_api: VkApiMethod):
    fulfillment_text, is_fallback = get_intent(project_id, event.user_id, event.text, language_code='en-EN')
    if is_fallback:
        vk_api.messages.send(user_id=event.user_id, message=fulfillment_text, random_id=random.randint(1, 1000))
        logger.info('Сообщение отправлено!')


if __name__ == '__main__':
    load_dotenv()

    bot = telebot.TeleBot(os.getenv('TG_BOT_TOKEN'))
    project_id = os.getenv('PROJECT_ID')

    logger.addHandler(TelegramLogsHandler(bot, chat_id=os.getenv('TG_CHAT_ID')))
    logger.setLevel('INFO')

    vk_session = vk.VkApi(token=os.getenv('VK_GROUP_TOKEN'))
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                send_to_vk(event, project_id, vk_api)
            except Exception as error:
                logger.exception('{}'.format(error))

