import random
import nltk
import json
#import sklearn
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# BOT_CONFIG = {
#     'intents': {
#         'hello': {
#             'examples': ['Привет!', 'хэллоу', 'добрый день!!'],
#             'responses': ['хай', 'Здравствуйте', 'Доброе утро!']
#         },
#         'bye': {
#             'examples': ['Пока!', 'увидимся', 'счастливо'],
#             'responses': ['до свиданья', 'до скорых встреч', 'Спокойной ночи)']
#         },
#         'howdoyoudo': {
#             'examples': ['Как дела?', 'Как жизнь????', 'Как ты?!'],
#             'responses': ['Неплохо!', 'Отлично!!', 'Ужасно(((']
#         }
#         }
# }

with open('BOT_CONFIG.json', 'r', encoding='utf-8') as f:
  BOT_CONFIG = json.load(f)

# with open('/content/BOT_CONFIG.json', 'w') as f:
#    json.dump(BOT_CONFIG, f)

def clean(text):
  clean_text = ''
  for char in text.lower():
    if char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
      clean_text = clean_text + char
  return clean_text

def get_intent(text):
  for intent in BOT_CONFIG['intents'].keys():
    for example in BOT_CONFIG['intents'][intent]['examples']:
      s1 = clean(text)
      s2 = clean(example)
      if nltk.edit_distance(s1, s2) / max(len(s1), len(s2)) < 0.4:
        return intent
  return 'intent not found :('

#def get_intent_by_model(text):
#  return clf.predict(vectorizer.transform([text]))[0]

corpus = []
y = []
for intent in BOT_CONFIG['intents'].keys():
  for example in BOT_CONFIG['intents'][intent]['examples']:
    corpus.append(example)
    y.append(intent)

#corpus_train, corpus_test, y_train, y_test = sklearn.model_selection.train_test_split(corpus, y, test_size=0.2)

# vectorizer = sklearn.feature_extraction.text.CountVectorizer(ngram_range=(2,4), analyzer='char_wb')
#vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(ngram_range=(2, 4), analyzer='char_wb', use_idf=True)
#X_train = vectorizer.fit_transform(corpus_train)
#X_test = vectorizer.transform(corpus_test)

#clf = sklearn.linear_model.RidgeClassifier(copy_X=True, max_iter=200)
# clf = sklearn.ensemble.RandomForestClassifier()
#clf.fit(X_train, y_train)

#clf.score(X_test, y_test)

def bot(text):
  # intent = get_intent_by_model(text)
  intent = get_intent(text)
  return random.choice(BOT_CONFIG['intents'][intent]['responses'])

# input_text = ''
# while input_text != 'STOP':
#   input_text = input()
#   bot(input_text)



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


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
    updater = Updater("2136512388:AAFnKljrnlTUMoxEpGw1aRK0fGnhu-9lfS4")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
