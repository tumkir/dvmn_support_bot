# Telegram и VK бот с использованием [dialogflow.com](Dialogflow) для службы поддержки

## Как подготовить бота к запуску

#### Dialogflow
* Создайте новый агент на сайте Dialogflow по [инструкции](https://cloud.google.com/dialogflow/docs/quick/build-agent])
* Перейдите в настройки, включите **V2 API**, получите и скачайте ключ (json файл) для полного доступа к API Dialogflow ([инструкция](https://dialogflow.com/docs/reference/v2-auth-setup))

#### Telegram бот
* Создайте и получите токен бота через [@botfather](https://t-do.ru/botfather)

#### VK бот
* [Создайте](https://vk.com/groups?tab=admin) группу в VK
* В настройках группы в разделе *Работа с API* создайте токен с доступом к сообщениям группы
* В разделе *Сообщения* включите возможность отправить сообщение в группу


## Как запустить на Heroku

* Зарегистрируйтесь на [heroku.com](https://www.heroku.com/) и создайте [новое приложение](https://dashboard.heroku.com/new-app)
* Форкните данный репозиторий

В разделе **Config Vars** на вкладке **Settings** вашего приложения пропишите:
- `bot_token` — токен телеграм бота, который вы получили у [@botfather](https://t-do.ru/botfather)
- `GOOGLE_APPLICATION_CREDENTIALS`=google-credentials.json
- `GOOGLE_CREDENTIALS` — содержимое файла google-credentials.json
- `owner_chat_id` — ваш id в телеграме для отправки ботом сервисных сообщений вам. Можно узнать у бота [@userinfobot](https://t-do.ru/userinfobot)
- `project_id` — название проекта в Dialogflow (написан в настройках агента)
- `vk_token` — токен от VK

Подтяните ключи из переменной `GOOGLE_CREDENTIALS` вот по этой [инструкции](https://stackoverflow.com/a/56818296/640260)

![config vars](https://raw.githubusercontent.com/tumkir/dvmn_support_bot/master/image/heroku_config_vars.png)


- Напишите личное сообщение вашему боту (если ещё не), иначе он не сможет отправить сообщение вам.
- Привяжите аккаунт GitHub на вкладке **Deploy** вашего приложения на Heroku и выберите нужный репозиторий
- Нажмите на кнопку **Deploy Branch** (позже можете включите автоматический деплой кнопкой выше)
- На вкладке **Resources** включите оба Dynos

Бот должен успешно запуститься и написать об этом вам в телеграм.

Если сообщение от бота не пришло, то нужно поставить [консольный клиент Heroku](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) и прочитать логи

```bash
heroku logs --app APP_NAME
```

## Как запустить на локальной машине
  1. В папке с ботом создайте `.env` файл и пропишите туда:
  - `bot_token` — токен телеграм бота, который вы получили у [@botfather](https://t-do.ru/botfather)
  - `GOOGLE_APPLICATION_CREDENTIALS` — путь до файла google-credentials.json (который вы скачали)
  - `owner_chat_id` — ваш id в телеграме для отправки ботом сервисных сообщений вам. Можно узнать у бота [@userinfobot](https://t-do.ru/userinfobot)
  - `project_id` — название проекта в Dialogflow (написан в настройках агента)
  - `vk_token` — токен от VK
  2. Установите зависимости:
  ```bash
  pip3 install -r requirements.txt
  ```
  3. Запустите бота:
  ```python3
  python3 tg_bot.py
  ```