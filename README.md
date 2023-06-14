# Телеграмм бот для введения дел 📝
## Данный бот был создан с помощью 2-х библиотек:
1. python-decouple
2. aiogram

## Бот умеет:
* создавать список задач;
* удалять задачу из списка;
* обновлять задачу;
* очищать список задач;
* удалять задачу после истечения у него дедлайна.

## Необходимые шаги для запуска бота:
1. Скопировать репозиторий (SSH ключ):
```py
git clone git@github.com:dinarius1/TodoListBot2.git
```
2. Создать и активировать виртуальное окружение:
```py
python3 -m venv venv
. venv/bin/activate
```
3. Установить необходимые библиотеки:
```py
pip install -r requirements.txt
```
4. Создать .env и прописать:
```py
touch .env
nano .env
TOKEN =5993019843:AAFZuWg9qdc5rlJoY-7RkuvFA5MXL2V2sjw
```
6. Запустить бота:
```py
python main.py
```
