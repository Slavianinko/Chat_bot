import random
import nltk
import json
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def clean(text):
    """Очистка текста от лишних символов"""
    clean_text = ''
    for char in text.lower():
        if char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdifghiklmnoprstvwqzyx':
            clean_text = clean_text + char
    return clean_text

def get_intent(text):
    """Получение наиболее похожего интента"""
    for intent in BOT_CONFIG['intents'].keys():
        for example in BOT_CONFIG['intents'][intent]['examples']:
            s1 = clean(text)
            s2 = clean(example)
            if nltk.edit_distance(s1, s2) / max(len(s1)+1, len(s2)) < 0.4:
                return intent
    return 'intent not found :('

def bot(text):
    """Принимаем текст от бота и отвечаем случайной фразой из похожего интента"""
    intent = get_intent(text)
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
    """Запуск бота"""
    # Создаём Updater и передаём ему токен
    updater = Updater(bot_key['key'])

    # Get the dispatcher to register handlers
    # Регистрация обработчиков
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # Ответы на команды
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    # ответ на не команду
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запуск бота
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    # Чтение интентов из файла
    with open('BOT_CONFIG.json', 'r', encoding='utf-8') as f:
        BOT_CONFIG = json.load(f)
    # Чтение ключа телеграм-бота
    with open('bot_key.json', 'r', encoding='utf-8') as f:
        bot_key = json.load(f)
    corpus = []
    for intent in BOT_CONFIG['intents'].keys():
        for example in BOT_CONFIG['intents'][intent]['examples']:
            corpus.append(example)

    main()
