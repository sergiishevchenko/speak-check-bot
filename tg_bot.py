import logging
import os

from dotenv import load_dotenv
from google_methods.get_intent import get_intent
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logger = logging.getLogger(__name__)

load_dotenv()


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Здравствуйте {user.mention_markdown_v2()}\!', reply_markup=ForceReply(selective=True))


def send_through_dialog_flow(update: Update, context: CallbackContext) -> None:
    response = get_intent(project_id=context.bot_data['project_id'], session_id=update.effective_user.id, msg=update.message.text, language_code='en-EN')
    update.message.reply_text(response.fulfillment_text)


def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater = Updater(token=os.getenv('TG_BOT_TOKEN'))

    dispatcher = updater.dispatcher

    project_id = os.getenv('PROJECT_ID')
    dispatcher.bot_data = {
        'project_id': project_id,
    }

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_through_dialog_flow))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()