import sqlite3
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters import Command

from utils import validate_name, validate_birth_date, get_day_of_week, get_patient_word

import logging
import locale

import os

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)


conn = sqlite3.connect('patients.db')


BOT_TOKEN = os.environ['BOT_TOKEN']
#BOT_TOKEN = 'YOUR_BOT_TOKEN'



bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)



class Form(StatesGroup):
    name = State()
    birth_date = State()
    





def get_main_keyboard():

    """ get main keyboard """

    builder = ReplyKeyboardBuilder()
    builder.button(text="Пациенты сегодня")
    builder.button(text="Статистика за неделю")
    builder.button(text="Добавить пациента") 
    builder.adjust(2)  
    return builder.as_markup(resize_keyboard=True)  


def get_confiramtion_keyboard():

    """ get keyboard for confirmation """
    
    builder = InlineKeyboardBuilder()
    builder.button(text="Потвердить", callback_data='confirm_yes')
    builder.button(text="Отмена", callback_data='confirm_no')
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)







@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    ''' start command handler '''

    keyboard = get_main_keyboard()
    await message.reply("Добро пожаловать в бот учета пациентов!", reply_markup=keyboard)


@dp.message(lambda message: message.text == 'Добавить пациента')
async def cmd_add_patient(message: types.Message, state: FSMContext):
    ''' add patient command handler '''

    await state.set_state(Form.name)
    await message.reply("Введите полное имя пациента:")


@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    ''' get name of the patient '''

    if validate_name(message.text):
        await state.update_data(name=message.text)
        await state.set_state(Form.birth_date)
        await message.reply("Введите дату рождения пациента. (ДД MM ГГГГ):")
    else:
        await message.reply("Неверный формат. Пожалуйста, введите полное имя пациента:")


@dp.message(Form.birth_date)
async def process_birth_date(message: types.Message, state: FSMContext):
    ''' get birth date of the patient '''

    if validate_birth_date(message.text):
        await state.update_data(birth_date=message.text)
        user_data = await state.get_data()
        keyboard = get_confiramtion_keyboard()
        await message.reply(f"Има: {user_data['name']}\nДата рождения: {message.text}\n", reply_markup=keyboard)
    else:
        await message.reply("Неверный формат. Пожалуйста введите дату рождения (ДД ММ ГГГГ):")



@dp.callback_query(lambda c: c.data.startswith('confirm_'))
async def process_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    ''' process confirmation '''

    if callback_query.data == 'confirm_yes':
        user_data = await state.get_data()
        name = f'{user_data["name"]}'
        birth_date = user_data['birth_date']
        visit_date = datetime.now().strftime('%Y-%m-%d')
        try:
            with conn:
                conn.execute("INSERT INTO patients (name, birth_date, visit_date) VALUES (?, ?, ?)", (name, birth_date, visit_date))
            await bot.send_message(callback_query.from_user.id, "Пациент успешно добавлен!")
        except sqlite3.Error as e:
            logging.error(f"Ошибка при записи в базу данных: {e}")
            await bot.send_message(callback_query.from_user.id, "Произошла ошибка при добавлении пациента. Пожалуйста, попробуйте еще раз.")
        await state.clear()
    else:
        await callback_query.message.edit_text("Операция отменена.")    
        await state.clear()
    
    await callback_query.answer() 




@dp.message(lambda message: message.text == 'Пациенты сегодня')
async def cmd_today_patients(message: types.Message):
    ''' get patients for today '''

    today = datetime.now().strftime('%Y-%m-%d')
    try:
        with conn:
            result = conn.execute("SELECT name, birth_date FROM patients WHERE visit_date = ?", (today,))
            patients = result.fetchall()
        if patients:
            response = "Пациенты сегодня:\n\n" + "\n".join([f"{name},  {birth_date}" for name, birth_date in patients])
        else:
            response = "Сегодня новых пациентов не было."
        await message.reply(response)
    except sqlite3.Error as e:
        logging.error(f"Ошибка при чтении из базы данных: {e}")
        await message.reply("Произошла ошибка при получении данных. Пожалуйста, попробуйте еще раз.")




@dp.message(lambda message: message.text == 'Статистика за неделю')
async def cmd_weekly_stats(message: types.Message):
    ''' get weekly statistics '''
    
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    try:
        with conn:
            result =conn.execute("SELECT visit_date, COUNT(*) FROM patients WHERE visit_date BETWEEN ? AND ? GROUP BY visit_date", (week_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')))
            stats = result.fetchall()
        if stats:
            response = "Статистика за неделю:\n" + "\n".join([f"{get_day_of_week(visit_date)}: {count} {get_patient_word(count)}" for visit_date, count in stats])
        else:
            response = "За последнюю неделю новых пациентов не было."
        await message.reply(response)
    except sqlite3.Error as e:
        logging.error(f"Ошибка при чтении из базы данных: {e}")
        await message.reply("Произошла ошибка при получении данных. Пожалуйста, попробуйте еще раз.")





    
async def main():
    try:
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS patients
                         (id INTEGER PRIMARY KEY, name TEXT, birth_date TEXT, visit_date TEXT)''')
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при создании таблицы: {e}")
        return

    await dp.start_polling(bot, skip_updates=True)





if __name__ == '__main__':
    import asyncio
    loop = asyncio.run(main())