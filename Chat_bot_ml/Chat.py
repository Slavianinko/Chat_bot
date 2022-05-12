import random
import json
from sklearn.linear_model import RidgeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def bot(text):
    """Принимаем текст от бота и отвечаем случайной фразой из интента,
        определённого моделью классификации
    """
    intent = clf.predict(vectorizer.transform([text]))[0]
    return random.choice(BOT_CONFIG['intents'][intent]['responses'])

# Определение обработчиков команд.
def start(update: Update, context: CallbackContext) -> None:
    """Отправление сообщения, когда будет получена команда Старт"""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Отправление сообщения, когда будет получена команда Help"""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Отвечаем на сообщение"""
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


# -------- Запуск телеграм-бота ------------------------------------------------------
if __name__ == '__main__':
    # -------- Чтение данных из файла -------------------------------------------------
    with open('BOT_CONFIG.json', 'r', encoding='utf-8') as f:
        BOT_CONFIG = json.load(f)
    with open('bot_key.json', 'r', encoding='utf-8') as f:
        bot_key = json.load(f)
    print(bot_key['key'])

    corpus = []
    y = []
    for intent in BOT_CONFIG['intents'].keys():
        for example in BOT_CONFIG['intents'][intent]['examples']:
            corpus.append(example)
            y.append(intent)

    # ------- Создание и тренировка модели ---------------------------------------------
    # vectorizer = CountVectorizer(ngram_range=(2,4), analyzer='char_wb')
    vectorizer = TfidfVectorizer(ngram_range=(2, 4), analyzer='char_wb', use_idf=True)
    X = vectorizer.fit_transform(corpus)
    # clf = sklearn.linear_model.RidgeClassifier(copy_X=True, max_iter=200)
    clf = RandomForestClassifier()
    clf.fit(X, y)

    main()