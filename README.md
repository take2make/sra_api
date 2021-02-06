# SPEECH RECOGNITION APLICATION API

В процессе учавствования в хакатоне: https://hackatom.ru/ реализовано api для перевода аудио речи в текст.

## Описание задачи:
Интеллектуальный сервис по распознаванию текста из аудио
источника для конспектирования учебных занятий и видеолекций.

## Описания решения:
Для конвертирования аудио речи в текст используется открытое api vosk_api (https://alphacephei.com/vosk/).
Используются уже предобученные модели: (https://alphacephei.com/vosk/models).

Пользователь отправляет на api сервер json структуру вида {кодированное аудио/видео, расширение исходного аудио/видео, модель для распознавания, профессиональные термины}. На сервере формируется запрос, после того как произойдет конвертация, результирующий текст будет доступен на сервере.

## Процесс запуска и установки (unix системы)

## Создание виртуального окружения ##
python3 -m venv venv
## Активация виртуального окружения ##
source venv/bin/activate
## Установка необходимых зависимостей ##
## pip3 install -r requirements.txt ##

## Запуск

python3 manage.py runserver

Прежде, может понадобится запустить необходимые миграции:
python3 manage.py makemigrations
python3 manage.py migrate
