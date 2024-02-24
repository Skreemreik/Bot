import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from langchain.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage

llm = GigaChat(
  verify_ssl_certs=False,
  scope="GIGACHAT_API_PERS",
  credentials="...")

API_TOKEN = '6646127537:AAEa-erni0KflNBwLICNJByogiuUc0T3pqo'

# Устанавливаем уровень логов на INFO
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Определяем состояния текста, в которых находится пользователь
class TextStates(StatesGroup):
    INPUT_DIALOG1 = State()
    INPUT_DIALOG2 = State()
    INPUT_DIALOG3 = State()
    START = State()  # Стартовое состояние
    FINISH = State()

# Обработчик команды /start


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Я бот gigachat. Люблю болтать, с какой частью меня вы хотите поговорить?"
                        "\n 1. Компьютерный мастер. \n 2. Человек-паук \n 3. Знаток Лиги Легенд.")

    # Переход в стартовое состояние
    await TextStates.START.set()


@dp.message_handler(commands=['1'], state=TextStates.START)
async def finish(message: types.Message, state: FSMContext):
    await message.reply("Напиши свой вопрос, или напиши 404, чтобы выйти из диалога")
    await TextStates.INPUT_DIALOG1.set()


@dp.message_handler(state=TextStates.INPUT_DIALOG1)
async def finish(message: types.Message, state: FSMContext):
        messages = [
            SystemMessage(
                content="Ты компьютерный мастер!"
            )
        ]
        dialog = message.text
        if dialog == "404":
            await message.reply("Привет! Я бот gigachat. Люблю болтать, с какой частью меня вы хотите поговорить?"
                                "\n 1. Компьютерный мастер. \n 2. Человек-паук \n 3. Знаток Лиги Легенд.")
            await TextStates.START.set()
        else:
            messages.append(HumanMessage(content=dialog))
            res = llm(messages)
            messages.append(res)
            await message.reply(res.content)
            await message.reply("Напиши свой вопрос, или напиши 404, чтобы выйти из диалога")
            await TextStates.INPUT_DIALOG1.set()


@dp.message_handler(commands=['2'], state=TextStates.START)
async def finish(message: types.Message, state: FSMContext):
    await message.reply("Напиши свой вопрос, или напиши 404, чтобы выйти из диалога")
    await TextStates.INPUT_DIALOG2.set()


@dp.message_handler(state=TextStates.INPUT_DIALOG2)
async def finish(message: types.Message, state: FSMContext):
        messages = [
            SystemMessage(
                content="Ты человек-паук!"
            )
        ]
        dialog = message.text
        if dialog == "404":
            await message.reply("Привет! Я бот gigachat. Люблю болтать, с какой частью меня вы хотите поговорить?"
                                "\n 1. Компьютерный мастер. \n 2. Человек-паук \n 3. Знаток Лиги Легенд.")
            await TextStates.START.set()
        else:
            messages.append(HumanMessage(content=dialog))
            res = llm(messages)
            messages.append(res)
            await message.reply(res.content)
            await message.reply("Напиши свой вопрос, или напиши 404, чтобы выйти из диалога")
            await TextStates.INPUT_DIALOG2.set()



@dp.message_handler(commands=['3'], state=TextStates.START)
async def finish(message: types.Message, state: FSMContext):
    await message.reply("Напиши свой вопрос, или напиши 404, чтобы выйти из диалога")
    await TextStates.INPUT_DIALOG3.set()


@dp.message_handler(state=TextStates.INPUT_DIALOG3)
async def finish(message: types.Message, state: FSMContext):
        messages = [
            SystemMessage(
                content="Ты знаток Лиги Легенд!"
            )
        ]
        dialog = message.text
        if dialog == "404":
            await message.reply("Привет! Я бот gigachat. Люблю болтать, с какой частью меня вы хотите поговорить?"
                                "\n 1. Компьютерный мастер. \n 2. Человек-паук \n 3. Знаток Лиги Легенд.")
            await TextStates.START.set()
        else:
            messages.append(HumanMessage(content=dialog))
            res = llm(messages)
            messages.append(res)
            await message.reply(res.content)
            await message.reply("Напиши свой вопрос, или напиши 404, чтобы выйти из диалога")
            await TextStates.INPUT_DIALOG3.set()


# Обработчик неизвестных команд
@dp.message_handler()
async def process_unknown_command(message: types.Message):
    await message.reply("Извините, я не понимаю такую команду.")


if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
