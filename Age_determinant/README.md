# [Определение возраста по фотографии](https://t.me/Age_determinant_bot)

Статус проекта: | В плане :black_square_button: | Выполняется :black_square_button: | Завершён :white_check_mark: | 
:------------ | :-------------| :-------------| :-------------

## Задача:

Учебный проект по [определению возраста по фотографии](https://github.com/Slavianinko/Yandex_practicum/tree/main/Age_determination) вдохновил меня пойти немного дальше. Очень хотелось проверить работу модели на своей фотографии и фотографиях друзей и знакомых. Тренажёр Яндекс Практикума таких вольностей не позволял, поэтому решил перенести код проекта на платформу [Kaggle](kaggle.com). Используемый в проекте набор данных и GPU на данной платформе есть, и с обучением нейросети проблем не возникло. Кроме того, перед решением непосредственно задачи регрессии, была добавлена модель детекции лиц. Получив рабочую модель, мне захотелось пойти ещё дальше, и я решил завернуть её в интерфейс телеграм-бота.

План действий получился такой:
1. Переносим код из учебного проекта на платформу [Kaggle](kaggle.com);
2. Обучаем модель;
3. Сохраняем модель в файл;
4. Создаём телеграм-бота;
5. В программе управляющей ботом загружаем модель и формируем обработчики так, чтобы при поступлении фотографии, с помощью загруженной модели определяем возраст и отвечаем.
6. Упаковываем программу в docker container и деплоим на VPS сервере.

## Данные:

Использован датасет [Apparent and real age estimation in still images with deep residual regressors on APPA-REAL database.](https://chalearnlap.cvc.uab.cat/dataset/26/description/#)


## Используемые библиотеки
- PIL
- tensorflow.keras
- python-telegram-bot;
- face_recognition

## Отработанные методы и навыки
- Построение нейросетевой модели машинного обучения для решения задачи регрессии;
- Создание сервисов с помощью телеграм-бота;
- Работа с Docker;
- Деплой на сервере VPS.
  

## Итоги проекта

1. Получены навыки работы с нейросетевыми моделями в решении задачь детекции и регрессии.
2. Было очень интересно протестировать модель на реальных фотографиях. Убедился, что модель работает и показывает точность, схожую с полученной на валидационной выборке.
3. Создан телеграм-бот с помощью которого можно очень просто определять видимый возраст кого угодно.
4. Бот упакован в Docker контейнер и задеплоен на сервер.

## Приглашаю всех протестировать бота! [Age_determinant_bot](https://t.me/Age_determinant_bot)
