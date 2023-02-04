<<<<<<< HEAD
=======
import os
from keras.layers import Rescaling
>>>>>>> main
from keras.models import load_model
from keras.utils import image_dataset_from_directory
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
<<<<<<< HEAD
import os
import face_recognition
from PIL import Image


=======


# Определение обработчиков команд
>>>>>>> main
def start(update: Update, context: CallbackContext) -> None:
    """Отправление сообщения, когда будет получена команда Старт"""

    user = update.effective_user
    keyboard = ReplyKeyboardMarkup([['/start','/help']], resize_keyboard=True)
    
<<<<<<< HEAD
    update.message.reply_markdown_v2(fr'Привет {user.mention_markdown_v2()}\!')
    update.message.reply_text('\n'.join([
        'Прикрепи своё фото к ответному сообщению, и я скажу на какой возраст ты выглядишь!',
        'Для лучшего качества распознавания, отправляйте фотографию как файл без сжатия.',
        '',
        'И, не судите строго - я ведь всего лишь нейросеть!'
        ]),reply_markup=keyboard
        )
=======
    update.message.reply_markdown_v2(fr'Привет {user.mention_markdown_v2()}\!',
                                     # reply_markup=ForceReply(selective=True),
                                    )
    update.message.reply_text('Прикрепи своё фото к ответному сообщению, и я скажу на какой возраст ты выглядишь!',
                               # reply_markup = ForceReply(selective=True),
                              reply_markup=keyboard
                             )
    print('Start comand')
>>>>>>> main


def help_command(update: Update, context: CallbackContext) -> None:
    """Отправление сообщения, когда будет получена команда Help"""
    keyboard = ReplyKeyboardMarkup([['/start', '/help']], resize_keyboard=True)
<<<<<<< HEAD
    update.message.reply_text('\n'.join([
        'Прикрепи своё фото к ответному сообщению, и я скажу на какой возраст ты выглядишь!',
        'Для лучшего качества распознавания, отправляйте фотографию как файл без сжатия.'
        ]),reply_markup=keyboard
        )


def ansver_photo(update: Update, context: CallbackContext) -> None:
    """Отвечаем на сообщение если в сообщении фото"""

    # Сохраняем файл с фотографией на диск
    update.message.photo[-1].get_file().download()
    # Отвечаем предсказанием
    answer(update)
=======
    update.message.reply_text('Привет! Прикрепи своё фото к ответному сообщению, и я скажу на какой возраст ты выглядишь!',
                              reply_markup=keyboard
                             )
    print('Help comand')

def ansver_photo(update: Update, context: CallbackContext) -> None:
    """Отвечаем на сообщение если в сообщении фото"""
    print('ansver_photo')
    try:
        # Сохраняем файл с фотографией на диск
        print('Download', os.listdir())
        update.message.photo[1].get_file().download()
        print(os.listdir())
        # Отвечаем предсказанием
        update.message.reply_text('Думаю, тебе ' + get_predict())
    except:
        # Если что-то пошло не так
        print('Eror')
        update.message.reply_text('Что-то пошло не так.')
>>>>>>> main


def ansver_file(update:Update, context: CallbackContext) -> None:
    """Отвечаем на сообщение если в сообщении файл"""
<<<<<<< HEAD
    # Сохраняем файл с фотографией на диск
    update.message.document.get_file().download()
    # Отвечаем предсказанием
    answer(update)


def answer(update:Update):
    """ Формируем ответ """
    try:
        # Отвечаем предсказанием
        ages, images = get_predict(PATH)
        print(ages)
        print(images)
        if ages == 999:
            # Если не нашли лиц на фото
            update.message.reply_photo(open(PATH + '/foto/' + images[0], 'rb'),
                                       caption='\n'.join([
                'Что-то я ненашёл лиц на фотографии.((',
                'Отправьте фото как файл без сжатия, либо выберите другое фото.'
            ]))
        else:
            # Если нашли лица - отвечаем
            for age, item in zip(ages, images):
                print(item)
                update.message.reply_photo(open(PATH + '/' + item, 'rb'),
                                           caption='Думаю, тебе ' + str(round(age))
                                           )
    except Exception as ex:
        # печатаем ошибку
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

=======
    print('ansver_file')
    try:
        # Сохраняем файл с фотографией на диск
        print('Download', os.listdir())
        update.message.document.get_file().download()
        print(os.listdir())
        # Отвечаем предсказанием
        update.message.reply_text('Думаю, тебе ' + get_predict())
    except:
>>>>>>> main
        # Если что-то пошло не так
        print('Eror')
        print(update.message.photo)
        update.message.reply_text('Что-то пошло не так.')
    finally:
        # Удаляем файлы
        for file in os.listdir(PATH + '/foto/'):
            os.remove(os.path.join(PATH + '/foto/', file))


def get_predict():
    """ Принимаем путь к папке.
        Возвращаем предсказание.
    """
<<<<<<< HEAD
    # загружаем файл в модель распознавания лиц
    filename = os.listdir(path + '/foto/')[0]
    image = face_recognition.load_image_file(filename)
    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        return 999, [filename]
    print(face_locations)
    # Удаляем файл с фотографией
    os.remove(os.path.join(path + '/foto/', filename))

    # Сохраняем каждое найденное лицо в файл
    for idx, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location
        print(top, right, bottom, left)
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.save(f'face_{idx}.jpg')

    # Создаём генератор данных
    datagen = ImageDataGenerator(rescale=(1 / 255))
    my_datagen = datagen.flow_from_directory(
        directory=path,
        shuffle=False,
        target_size=(224, 224)
    )
    print(my_datagen.filenames)
=======
    # Создаём набор данных
    print('get_predict')
    dataset = image_dataset_from_directory(directory="..",
                                           shuffle=False,
                                           batch_size=1,
                                           image_size=(224, 224))
    print('Normalize')
    normalization_layer = Rescaling(1. / 255)
    normalized_ds = dataset.map(lambda x, y: (normalization_layer(x), y))
    print('predict')
>>>>>>> main
    # Предсказываем возраст
    predictions = model.predict(normalized_ds)
    print(predictions)
<<<<<<< HEAD
    preds = [p[0] for p in predictions]

    return preds, my_datagen.filenames
=======
    # Удаляем файл с фотографией
    for item in os.listdir():
        os.remove(item)
    return str(round(predictions[0][0]))
>>>>>>> main


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
<<<<<<< HEAD
    dispatcher.add_handler(MessageHandler(Filters.document.category("image"), ansver_file))

=======
    dispatcher.add_handler(MessageHandler(Filters.document, ansver_file))
>>>>>>> main
    # Запуск бота
    updater.start_polling()


# Точка входа
if __name__ == '__main__':
<<<<<<< HEAD

    # Определяем путь
    PATH = os.path.abspath(os.path.join(os.getcwd(), ".."))
    print(PATH)

    # Читаем токен телеграм-бота из файла
    with open('../../bot_key.txt', 'r', encoding='utf-8') as f:
        TOKEN = f.read()

    # Читаем модель из файла
    model = load_model('../../my_cnn_fr_1.h5')
    print(model.summary())

=======
    # Читаем токен телеграм-бота из файла
    with open('bot_key.txt', 'r', encoding='utf-8') as f:
        TOKEN = f.read()
    # Читаем модель из файла
    model = load_model('my_cnn.h5')
    print(model.summary())
    print(os.listdir())
    # Определяем рабочий каталог
    os.chdir('My_foto/foto')
>>>>>>> main
    # Запускаем бота
    main()