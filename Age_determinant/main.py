import json
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os


# Определение обработчиков команд.
def start(update: Update, context: CallbackContext) -> None:
    """Отправление сообщения, когда будет получена команда Старт"""
    user = update.effective_user
    keyboard = ReplyKeyboardMarkup([['/start','/help']], resize_keyboard=True)
    
    update.message.reply_markdown_v2(fr'Привет {user.mention_markdown_v2()}\!',
                                     # reply_markup=ForceReply(selective=True),
                                    )
    update.message.reply_text('Прикрепи своё фото к ответному сообщению, и я скажу на какой возраст ты выглядишь!',
                               # reply_markup = ForceReply(selective=True),
                              reply_markup=keyboard
                             )


def help_command(update: Update, context: CallbackContext) -> None:
    """Отправление сообщения, когда будет получена команда Help"""
    keyboard = ReplyKeyboardMarkup([['/start', '/help']], resize_keyboard=True)
    update.message.reply_text('Привет! Прикрепи своё фото к ответному сообщению, и я скажу на какой возраст ты выглядишь!',
                              reply_markup=keyboard
                             )


def ansver_photo(update: Update, context: CallbackContext) -> None:
    """Отвечаем на сообщение если в сообщении фото"""
    try:
        # Сохраняем файл с фотографией на диск
        update.message.photo[1].get_file().download()
        # Отвечаем предсказанием
        update.message.reply_text('Думаю, тебе ' + get_predict(PATH))
    except:
        # Если что-то пошло не так
        print('Eror')
        print(update.message.photo)
        update.message.reply_text('Что-то пошло не так.')


def ansver_file(update:Update, context: CallbackContext) -> None:
    """Отвечаем на сообщение если в сообщении файл"""
    try:
        # Сохраняем файл с фотографией на диск
        update.message.document.get_file().download()
        # Отвечаем предсказанием
        update.message.reply_text('Думаю, тебе ' + get_predict(PATH))
    except:
        # Если что-то пошло не так
        print('Eror')
        print(update.message.document)
        update.message.reply_text('Что-то пошло не так.')

def get_predict(path):
    """ Принимаем путь к папке.
        Возвращаем предсказание.
    """
    # Создаём генератор данных
    datagen = ImageDataGenerator(rescale=(1 / 255))
    my_datagen = datagen.flow_from_directory(
        directory=path,
        shuffle=False,
        target_size=(224, 224)
    )
    # Предсказываем возраст
    predictions = model.predict(my_datagen)
    print(predictions)
    # Удаляем файл с фотографией
    os.remove(os.path.join(path+'/My_foto/', os.listdir(path+'/My_foto/')[0]))
    return str(round(predictions[0][0]))


def main() -> None:
    """Запуск бота"""
    # Создаём Updater и передаём ему токен
    updater = Updater(TOKEN)

    # Регистрация обработчиков
    dispatcher = updater.dispatcher

    # Ответы на команды
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # ответ на сообщение
    dispatcher.add_handler(MessageHandler(Filters.photo, ansver_photo))
    dispatcher.add_handler(MessageHandler(Filters.document, ansver_file))

    # Запуск бота
    updater.start_polling()


# Точка входа
if __name__ == '__main__':
    # Определяем путь
    PATH = os.path.abspath(os.path.join(os.getcwd(),".."))
    # Читаем токен телеграм-бота из файла
    with open('../../bot_key.json', 'r', encoding='utf-8') as f:
        bot_key = json.load(f)
        TOKEN = bot_key['key']
    # Читаем модель из файла
    model = load_model('../../my_cnn.h5')
    print(model.summary())
    # Запускаем бота
    main()