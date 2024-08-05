import logging


from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from crud_functions import *


logging.basicConfig(level=logging.INFO)
api = '6710583309:AAGVSq2_Tdn-SwCG98f2DDigLRa_UHOUvpg'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Регистрация')],
        [
            KeyboardButton(text='Расчитать'),
            KeyboardButton(text='Информация')
        ],
        [KeyboardButton(text='Купить')]
    ], resize_keyboard=True
)
kb1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
        ]
    ]
)
kb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Product1', callback_data='product_buying'),
            InlineKeyboardButton(text='Product2', callback_data='product_buying'),
            InlineKeyboardButton(text='Product3', callback_data='product_buying'),
            InlineKeyboardButton(text='Product4', callback_data='product_buying')
        ]
    ]
)

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text='Привет')
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Регистрация')
async def sign_up(message):
    await message.answer('Введите имя пользователя (только латинские буквы)')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    is_inc = is_included(message.text)
    if is_inc is True:
        await message.answer('Данное имя уже занято, введите другое')
    else:
        await state.update_data(username=message.text)
        data = await state.get_data()
        await message.answer('Введите свой email')
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_age(message, state):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await message.answer('Введите свой возраст')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def end_of_reg(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await state.finish()
    await message.answer('Поздравляем, вы прошли регистрацию', reply_markup=kb)
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer('Выбери опцию:', reply_markup=kb1)

@dp.message_handler(text='Купить')
async def get_buying_list(message):

    items = get_all_products()
    for i in range(0, 4):
        await message.answer(f'Название:{items[0][i][-1]} | Описание:{items[1][i][-1]}| Цена:{items[2][i][-1]}')
        with open(f'fieles/{i}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer("Выберите товар для покупки:", reply_markup=kb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=float(message.text))
    await message.answer('Введите рост в см.')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(first1=float(message.text))
    await message.answer('Введите вес в кг.')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(first2=float(message.text))
    data = await state.get_data()
    bmi = (10 * data['first2']) + (6.25 * data['first1']) - (5 * data['first']) + 5
    await message.answer(f'Ваша норма калорий равена: {bmi} .')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)