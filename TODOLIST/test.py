import asyncio
import datetime
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Класс задачи
class Todo:
    def __init__(self, task, deadline):
        self.task = task
        self.deadline = deadline

    def __str__(self):
        return self.task

# Класс списка задач
class TodoList:
    def __init__(self):
        self.todos = []

    def add_task(self, task, deadline):
        todo = Todo(task, deadline)
        self.todos.append(todo)

    def get_tasks(self):
        return self.todos

    def delete_task(self, index):
        if 0 <= index < len(self.todos):
            del self.todos[index]

    def clear_tasks(self):
        self.todos = []

    def update_task(self, index, updated_task):
        if 0 <= index < len(self.todos):
            self.todos[index].task = updated_task

    async def check_deadlines(self):
        while True:
            now = datetime.datetime.now()
            for i, task in enumerate(self.todos):
                if task.deadline < now:
                    self.delete_task(i)
            await asyncio.sleep(60)  # Check deadlines every 60 seconds


# Инициализация бота
bot_token = '5993019843:AAFZuWg9qdc5rlJoY-7RkuvFA5MXL2V2sjw'
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создание объекта todo list
todo_list = TodoList()

# Запуск проверки дедлайнов в фоновом режиме
async def check_deadlines():
    await bot.wait_until_ready()
    await todo_list.check_deadlines()

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply(
        "Привет! Это твой todo list. Выбери любую команду из нижеперечисленных:", reply_markup=main_keyboard())

# Обработка команды /add
@dp.message_handler(commands=['add'])
async def add_handler(message: types.Message):
    task, deadline = message.text[5:].split(maxsplit=1)  # Получаем текст задачи и дедлайн после команды /add
    if task and deadline:
        try:
            deadline_datetime = datetime.datetime.strptime(deadline, "%m-%d")
            deadline_datetime = deadline_datetime.replace(year=datetime.datetime.now().year)  # Set the current year
            todo_list.add_task(task, deadline_datetime)
            formatted_deadline = deadline_datetime.strftime("%d-%m")
            await message.reply(f"Задача '{task}' добавлена в список. Дедлайн: {formatted_deadline}",
                                reply_markup=main_keyboard())
        except ValueError:
            await message.reply("Неправильный формат дедлайна. Используйте MM-DD.")
    else:
        await message.reply("Пожалуйста, введите задачу и дедлайн после команды /add.")



# Обработка команды /list
@dp.message_handler(commands=['list'])
async def list_handler(message: types.Message):
    tasks = todo_list.get_tasks()
    if tasks:
        response = "Список задач:\n"
        for i, task in enumerate(tasks):
            response += f"{i + 1}. {task.task} (Дедлайн: {task.deadline})\n"
    else:
        response = "Список задач пуст."
    await message.reply(response, reply_markup=main_keyboard())


# Обработка команды /delete
@dp.message_handler(commands=['delete'])
async def delete_handler(message: types.Message):
    index = int(message.text[8:]) - 1  # Получаем индекс задачи после команды /delete
    tasks = todo_list.get_tasks()
    if 0 <= index < len(tasks):
        todo_list.delete_task(index)
        await message.reply("Задача удалена из списка.", reply_markup=main_keyboard())
    else:
        await message.reply("Неправильный индекс задачи.", reply_markup=main_keyboard())


# Обработка команды /clear
@dp.message_handler(commands=['clear'])
async def clear_handler(message: types.Message):
    todo_list.clear_tasks()
    await message.reply("Список задач очищен.", reply_markup=main_keyboard())


# Обработка команды /update
@dp.message_handler(commands=['update'])
async def update_handler(message: types.Message):
    try:
        index, updated_task = message.text[8:].split(maxsplit=1)  # Получаем индекс и обновленную задачу
        index = int(index) - 1  # Преобразуем индекс в число
        tasks = todo_list.get_tasks()
        if 0 <= index < len(tasks):
            todo_list.update_task(index, updated_task)
            await message.reply(f"Задача с индексом {index + 1} обновлена.", reply_markup=main_keyboard())
        else:
            await message.reply("Неправильный индекс задачи.", reply_markup=main_keyboard())
    except ValueError:
        await message.reply("Пожалуйста, введите индекс и обновленную задачу после команды /update.")


# Обработка нажатий на Inline-кнопки
@dp.callback_query_handler(lambda c: True)
async def inline_button_handler(callback_query: types.CallbackQuery):
    command = callback_query.data
    if command == 'add':
        await bot.send_message(callback_query.from_user.id, "Введите задачу и дедлайн после команды /add.")
    elif command == 'list':
        tasks = todo_list.get_tasks()
        if tasks:
            response = "Список задач:\n"
            for i, task in enumerate(tasks):
                response += f"{i + 1}. {task.task} (Дедлайн: {task.deadline})\n"
        else:
            response = "Список задач пуст."
        await bot.send_message(callback_query.from_user.id, response, reply_markup=main_keyboard())
    elif command == 'delete':
        await bot.send_message(callback_query.from_user.id, "Введите номер задачи после команды /delete.")
    elif command == 'clear':
        todo_list.clear_tasks()
        await bot.send_message(callback_query.from_user.id, "Список задач очищен.", reply_markup=main_keyboard())
    elif command == 'update':
        await bot.send_message(callback_query.from_user.id,
                               "Введите индекс и обновленную задачу после команды /update.")


# Функция для создания клавиатуры
def main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Добавить задачу", callback_data="add"),
        InlineKeyboardButton("Показать список", callback_data="list"),
        InlineKeyboardButton("Удалить задачу", callback_data="delete"),
        InlineKeyboardButton("Очистить список", callback_data="clear"),
        InlineKeyboardButton("Обновить задачу", callback_data="update")
    )
    return keyboard


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    dp.loop.create_task(check_deadlines())
