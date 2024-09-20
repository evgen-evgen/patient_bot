# patient_bot
бот для учета пациентов(тестовое) 


## Установка и запуск бота

### Получите токен для вашего бота:

1. Перейдите в Telegram и найдите канал [BotFather](https://t.me/BotFather).
2. Следуйте инструкциям BotFather для создания нового бота и получения токена.

### Скачайте репозиторий:

#### Если у вас установлен Git, клонируйте репозиторий и перейдите в директорию проекта:
```
git clone https://github.com/evgen-evgen/patient_bot
cd patient_bot
```

### Если у вас нет Git, скачайте ZIP-архив с репозиторием:
1. Перейдите на страницу вашего репозитория на GitHub.
2. Нажмите кнопку "Code" и выберите "Download ZIP".
3. Распакуйте скачанный архив и перейдите в распакованную директорию.

### Настройка токена
Рекомендуется создать файл .env в корневой директории проекта и добавить в него строку:
```
    BOT_TOKEN='ваш токен полученный в BotFather'
```

Либо, если вы не хотите использовать файл .env, откройте файл main.py и найдите строки, связанные с токеном:
    
```
        # BOT_TOKEN = os.environ['BOT_TOKEN']  # Строка 36
        BOT_TOKEN = 'YOUR_BOT_TOKEN'  # Строка 37
```

Замените 'YOUR_BOT_TOKEN' на ваш токен, полученный в BotFather.
Раскомментируйте строку 37 и закомментируйте строку 36:
```
        # BOT_TOKEN = os.environ['BOT_TOKEN']  # Строка 36
        BOT_TOKEN = 'ваш токен'  # Строка 37
```
### Установка зависимостей
Установите зависимости, выполнив команду:
```
    pip install -r requirements.txt
```
### Запуск бота
Запустите бота, выполнив команду:
```
    python main.py
```

После запуска бота вы можете найти его в Telegram и начать использовать.