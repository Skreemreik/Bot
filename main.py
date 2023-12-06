import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '6646127537:AAEa-erni0KflNBwLICNJByogiuUc0T3pqo'

# Устанавливаем уровень логов на INFO
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Определяем состояния текста, в которых находится пользователь
class TextStates(StatesGroup):
    INPUT_REG = State()  # Запрос регистрации
    INPUT_NAME = State()  # Запрос имени пользователя
    INPUT_AGE = State()  # Запрос возраста пользователя
    START = State()  # Стартовое состояние
    FINISH = State()

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Я бот. Могу вас зарегистрировать:\n 1. Я зарегистрирован. \n 2. Зарегистрироваться")

    # Переход в стартовое состояние
    await TextStates.START.set()

@dp.message_handler(commands=['1'], state=TextStates.START)
async def finish(message: types.Message, state: FSMContext):
    await message.reply("В таком случае вы зарегистрированы! Удачи!")

    # Завершаем состояние
    await state.finish()


@dp.message_handler(commands=['2'], state=TextStates.START)
async def process_reg_command(message: types.Message):
    await message.reply("Сейчас зарегистрируем! Напишите своё имя!")

    #Устанавливаем состояние ввода имени
    await TextStates.INPUT_NAME.set()



# Обработчик состояния ввода имени
@dp.message_handler(state=TextStates.INPUT_NAME)
async def process_input_name_state(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)  # Сохраняем имя пользователя


    await message.reply("Отлично! Теперь напиши свой возраст.")

    await TextStates.INPUT_AGE.set()


# Обработчик состояния ввода возраста
@dp.message_handler(state=TextStates.INPUT_AGE)
async def process_input_age_state(message: types.Message, state: FSMContext):
    age = message.text

    # Получаем имя из сохраненных данных состояния
    data = await state.get_data()
    name = data['name']
    try:
        isinstance(int(age), int)
        await message.reply(f"Спасибо, {name}! Твой возраст - {age}.")

        await message.reply("Вы зарегистрированы! Удачи!")
        # Завершаем состояние
        await state.finish()
    except ValueError as a:
        await message.reply("Ошибка! Введите возраст ещё раз, пожалуйста.")
        await TextStates.INPUT_AGE.set()


# Обработчик неизвестных команд
@dp.message_handler()
async def process_unknown_command(message: types.Message):
    await message.reply("Извините, я не понимаю такую команду.")


if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
