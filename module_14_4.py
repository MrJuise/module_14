from itertools import product

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from DB_SQLite.module_14 import texts
import crud_functions

api = "[x][x][x]"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_inline = InlineKeyboardMarkup()
kb_prod = InlineKeyboardMarkup()
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_inline = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
button_inline_2 = InlineKeyboardButton(text="Формулы рассчета", callback_data="formulas")

button_prod = InlineKeyboardButton(text="Продукт 1", callback_data="product_buying")
button_prod_2 = InlineKeyboardButton(text="Продукт 2", callback_data="product_buying")
button_prod_3 = InlineKeyboardButton(text="Продукт 3", callback_data="product_buying")
button_prod_4 = InlineKeyboardButton(text="Продукт 4", callback_data="product_buying")

button = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button3 = KeyboardButton(text="Купить")
kb.row(button, button2)
kb.add(button3)
kb_inline.row(button_inline, button_inline_2)
kb_prod.row(button_prod, button_prod_2, button_prod_3, button_prod_4)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f"Привет {message.from_user.username}, я бот помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text="Купить")
async def get_Buying_list(message):
    prod = crud_functions.get_all_products()
    images = ['img/1.jpg', 'img/2.jpg', 'img/3.jpg', 'img/4.jpeg']
    for i in range(min(len(prod), len(images))):
        with open(images[i], 'rb') as img:
            await message.answer_photo(
                img,
                f"Продукт: {prod[i][1]} \nОписание: {prod[i][2]} \nЦена: {prod[i][3]}"
            )
    await message.answer("Выберите продукт для покупки:", reply_markup=kb_prod)



@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно купили продукт!")
    await call.answer()


@dp.message_handler(text="Информация")
async def start(message):
    await message.answer("Информация о боте.")


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()
    level_activ = State()


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберете опцию:", reply_markup=kb_inline)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer(
        "для мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x коэффициент активности;\n"
        "для женщин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161) x коэффициент активности."
    )
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_gender(call):
    await call.message.answer("Введите свой пол (М / Ж):")
    await call.answer()
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    try:
        gender = str(message.text.casefold())
        if gender in ["м", "ж"]:
            await state.update_data(gender=gender)
            await message.answer("Введите свой возраст:")
            await UserState.age.set()
        else:
            await message.answer("Введите корректный пол (М / Ж).")
    except ValueError:
        await message.answer("Введите корректный пол (М / Ж).")


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    try:
        age = float(message.text)
        if age in range(13, 81):
            await state.update_data(age=age)
            await message.answer("Введите свой рост:")
            await UserState.growth.set()
        else:
            await message.answer("Данная формула актуальна только для лиц в возрасте от 13 до 80 лет.")
    except ValueError:
        await message.answer("Введите возраст в числовом формате.")


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    try:
        growth = float(message.text)
        if growth > 0:
            await state.update_data(growth=growth)
            await message.answer("Введите свой вес:")
            await UserState.weight.set()
        else:
            await message.answer("Рост не может быть меньше 0. Введите корректное значение!")
    except ValueError:
        await message.answer("Введите возраст в числовом формате.")


@dp.message_handler(state=UserState.weight)
async def set_level_active(message, state):
    try:
        weight = float(message.text)
        if weight > 0:
            await state.update_data(weight=weight)
            await message.answer("Введите свой уровень активности согласно номеру в таблице: \n "
                                 "1 - Минимальная активность \n 2 - Слабая активность\n "
                                 "3 - Средняя активность \n 4 - Высокая активность \n "
                                 "5 - Экстра-активность")
            await UserState.level_activ.set()
        else:
            await message.answer("Вес не может быть меньше 0. Введите корректный вес!")
    except ValueError:
        await message.answer("Введите вес в числовом формате.")


@dp.message_handler(state=UserState.level_activ)
async def send_calories(message, state):
    activ_value = {
        1: 1.2,
        2: 1.375,
        3: 1.55,
        4: 1.725,
        5: 1.9
    }
    try:
        level_active = int(message.text)
        if level_active in range(1, 6):
            await state.update_data(level_active=level_active)
            data = await state.get_data()
            if data["gender"] == "м":
                calories = (10 * float(data["weight"]) + 6.25 * float(data["growth"]) - 5 *
                            float(data["age"]) + 5) * activ_value[level_active]
                await message.answer(f"Норма калорий в день составляет: {round(calories)}")
            elif data["gender"] == "ж":
                calories = (10 * float(data["weight"]) + 6.25 * float(data["growth"]) - 5 *
                            float(data["age"]) + 5) * activ_value[level_active]
                await message.answer(f"Норма калорий в день составляет: {round(calories)}")
            await state.finish()
        else:
            await message.answer("Введите значение от 1 до 5 согласно таблице.")
    except ValueError:
        await message.answer("Введите значение от 1 до 5 согласно таблице.")


@dp.message_handler()
async def all_massages(message):
    await message.answer("Введите команду 'Start' для запуска бота.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
