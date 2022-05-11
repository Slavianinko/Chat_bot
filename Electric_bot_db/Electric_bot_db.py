import random
import json
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def bot(text):

  return text

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    input_text = update.message.text
    reply = bot(input_text)
    update.message.reply_text(reply)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(bot_key['key'])
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    # Start the Bot
    updater.start_polling()
    updater.idle()

# -------- Чтение данных из файла -------------------------------------------------

with open('bot_key.json', 'r', encoding='utf-8') as f:
    bot_key = json.load(f)
print(bot_key['key'])
# with open('/content/BOT_CONFIG.json', 'w') as f:
#    json.dump(BOT_CONFIG, f)


# ------- Создание и тренировка модели ---------------------------------------------



# -------- Запуск телеграм-бота ------------------------------------------------------
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    main()