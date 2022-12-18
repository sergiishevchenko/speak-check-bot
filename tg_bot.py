import logging
import os

from environs import Env
from google_methods.set_intent import set_intent
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Здравствуйте {user.mention_markdown_v2()}\!', reply_markup=ForceReply(selective=True))


def send_through_dialog_flow(update: Update, context: CallbackContext) -> None:
    response = set_intent(project_id=os.getenv('PROJECT_ID'), session_id=update.effective_user.id, msg=update.message.text, language_code='en-EN')[0]
    update.message.reply_text(response)


def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    env = Env()
    env.read_env()

    updater = Updater(token=os.getenv('TG_BOT_TOKEN'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_through_dialog_flow))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()