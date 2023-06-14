import logging
import asyncio
import os
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Parsing import get_links_by_class
from Schedule import read_schedule

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create bot instance
bot = Bot(token='5790202829:AAGlXbk17iGU0bYsB5vPVgEiBQ5nyMiUDsc')

# Create dispatcher
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define the state for waiting for group input
class ScheduleMenuState(StatesGroup):
    waiting_for_group = State()

# Define the handler for the /start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(text='Новости'), types.KeyboardButton(text='Расписание'), types.KeyboardButton(text='Изменения в расписании')]
    keyboard.add(*buttons)

    await message.answer("Доброго дня, студент! Я КБК БОТ, создан для улучшения твоей жизни. Выбери панель команды находящиеся на панели кнопок", reply_markup=keyboard)

# Define the handler for the News button
@dp.message_handler(text='Новости')
async def news(message: types.Message):
    url = 'https://student39.ru/news/'
    class_name = 'newsItem'
    links = get_links_by_class(url, class_name)

    # Send each link as a separate message with a delay
    for index, link in enumerate(links, start=1):
        await asyncio.sleep(0.5)  # Delay for 0.5 seconds before sending each message
        await message.answer(f"Link {index}: https://student39.ru{link}")

# Define the handler for the Schedule button
@dp.message_handler(text='Расписание')
async def schedule_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(text='Введите свою группу'), types.KeyboardButton(text='Главное меню')]
    keyboard.add(*buttons)

    await message.answer("Выберите кнопку 'Ввести группу' для открытия расписания или вернитесь в главное меню на кнопку 'Главное меню':", reply_markup=keyboard)

# Define the handler for the "Enter your group" button
@dp.message_handler(text='Введите свою группу', state='*')
async def enter_group_menu(message: types.Message):
    await message.answer("Пожалуйста введите имя своей группы! Важный момент, вводите имя своей группы без знака '-' Например: 20ИСП4 или 21ИСА3")
    await ScheduleMenuState.waiting_for_group.set()

# Define the handler for the "Back" button
@dp.message_handler(text='Главное меню', state='*')
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await start(message)

# Define the handler for receiving the group name in the schedule menu
@dp.message_handler(state=ScheduleMenuState.waiting_for_group)
async def receive_group_name_schedule_menu(message: types.Message, state: FSMContext):
    group_name = message.text

    # Get the newest Excel file in the directory
    directory = 'C:/Users/Sugimoto/PycharmProjects/KBKBot/Excel'
    newest_file = max([os.path.join(directory, f) for f in os.listdir(directory)], key=os.path.getctime)

    groups, lessons, schedule_data = read_schedule(newest_file, group_name)
    schedule_text = f"Schedule for group {group_name}:\n\n"
    for day, schedule in schedule_data.items():
        schedule_text += f"{day}\t\t{schedule.get(group_name, '')}\n"
    await message.answer(schedule_text)

    await state.finish()

# Define the handler for the Check button
@dp.message_handler(text='Изменения в расписании')
async def check_schedule(message: types.Message):
    # Insert your schedule checking code and get the output

    def compare_excel_files(file1, file2):
        # Load data from Excel files
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)

        # Compare the data
        changes = []
        for column in df2.columns[1:]:
            if not df1[column].equals(df2[column]):
                changes.append(column)

        if not changes:
            result = "No changes"
        else:
            result = f"Изменения в расписании для групп: {', '.join(changes)}. Студенты, пожалуйста проверьте расписание указанных групп !"

        return result

    # Get the two most recent Excel files in the directory
    directory = 'C:/Users/Sugimoto/PycharmProjects/KBKBot/Excel'
    files = os.listdir(directory)
    excel_files = [file for file in files if file.endswith('.xlsx') or file.endswith('.xls')]
    excel_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    recent_files = excel_files[:2]

    def proof():
        # Check for changes in the last two files
        if len(recent_files) == 2:
            file1 = os.path.join(directory, recent_files[0])
            file2 = os.path.join(directory, recent_files[1])
            result = compare_excel_files(file1, file2)
            return result
        else:
            return "Insufficient files for comparison"

    output = proof()

    # Send the message via the Telegram bot
    await message.answer(output)

# Define the handler for unknown commands or messages
@dp.message_handler()
async def unknown_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(text='Новости'), types.KeyboardButton(text='Расписание'), types.KeyboardButton(text='Изменения в расписании')]
    keyboard.add(*buttons)
    await message.answer("Такой команды не существует, пожалуйста воспользуйтесь панелью кнопок:", reply_markup=keyboard)

# Start the bot
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
