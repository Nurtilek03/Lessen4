import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio, logging
from config import my_token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=my_token)

dp = Dispatcher()

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT,
                        username TEXT,
                        address TEXT,
                        description TEXT,
                        status TEXT DEFAULT 'Заказ принят.'
                    )''')
    conn.commit()
    conn.close()

init_db()

def get_category_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍔 Еда", callback_data="category:Еда")],
        [InlineKeyboardButton(text="🔧 Запчасти", callback_data="category:Запчасти")],
        [InlineKeyboardButton(text="🪑 Мебель", callback_data="category:Мебель")],
    ])
    return keyboard

temp_data = {}

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Готовы оформить заказ? Просто выберите одну из категорий ниже:",
        reply_markup=get_category_keyboard()
    )

@dp.callback_query(lambda c: c.data.startswith("category:"))
async def select_category(callback_query: types.CallbackQuery):
    category = callback_query.data.split(":")[1]
    temp_data[callback_query.from_user.id] = {"category": category}
    await bot.send_message(callback_query.from_user.id, "Отлично! Как вас зовут?")

@dp.message(lambda message: message.from_user.id in temp_data and "username" not in temp_data[message.from_user.id])
async def get_username(message: types.Message):
    temp_data[message.from_user.id]["username"] = message.text
    await message.answer("Теперь укажите адрес доставки:")

@dp.message(lambda message: message.from_user.id in temp_data and "address" not in temp_data[message.from_user.id])
async def get_address(message: types.Message):
    temp_data[message.from_user.id]["address"] = message.text
    await message.answer("Опишите, что вам нужно заказать:")

@dp.message(lambda message: message.from_user.id in temp_data and "description" not in temp_data[message.from_user.id])
async def get_description(message: types.Message):
    user_data = temp_data[message.from_user.id]
    user_data["description"] = message.text

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO orders (category, username, address, description) 
                      VALUES (?, ?, ?, ?)''',
                   (user_data["category"], user_data["username"], user_data["address"], user_data["description"]))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()

    del temp_data[message.from_user.id]
    await message.answer(f"Поздравляю! Ваш заказ успешно оформлен. Номер заказа: {order_id}. Ожидайте подтверждения!")

@dp.message(Command("status"))
async def check_status_command(message: types.Message):
    await message.answer("Пожалуйста, введите номер вашего заказа, чтобы узнать его статус:")

@dp.message(lambda message: message.text.isdigit())
async def check_status(message: types.Message):
    order_id = int(message.text)
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        await message.answer(f"Статус вашего заказа: {result[0]}")
    else:
        await message.answer("Увы, заказ с таким номером не найден. Попробуйте еще раз.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())