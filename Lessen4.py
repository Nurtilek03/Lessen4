"""Машина состаение"""
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# import asyncio, logging
# from config import my_token

# logging.basicConfig(level=logging.INFO)

# bot = Bot(token=my_token)
# dp = Dispatcher()

# class UserInfo(StatesGroup):
#     name = State()
#     phone = State()
#     course = State()
#     department = State()
#     city = State()

# student_data = {}

# @dp.message(Command("start"))
# async def start(message:types.Message, state: FSMContext):
#     await message.answer("Добро пожаловать. Давай начнем с твоего имени. Как тебя зовут?")
#     await state.set_state(UserInfo.name)

# @dp.message(UserInfo.name)
# async def name(message:types.Message, state:FSMContext):
#     student_data['name'] = message.text
#     await message.reply("Введите номер телефона")
#     await state.set_state(UserInfo.phone)

# @dp.message(UserInfo.phone)
# async def phone(message:types.Message, state:FSMContext):
#     student_data['phone'] = message.text
#     await message.reply("Введите курса")
#     await state.set_state(UserInfo.course)

# @dp.message(UserInfo.course)
# async def course(message:types.Message, state:FSMContext):
#     student_data['course'] = message.text
#     await message.reply("Введите свой кафедру")
#     await state.set_state(UserInfo.department)

# @dp.message(UserInfo.department)
# async def department(message:types.Message, state:FSMContext):
#     student_data['department'] = message.text
#     await message.reply("Введите свой город")
#     await state.set_state(UserInfo.city)

# @dp.message(UserInfo.city)
# async def city(message:types.Message, state:FSMContext):
#     student_data['city'] = message.text
#     await message.answer(f'Спосибо за информацию ! Вот твои данные: \n'
#                          f'Имя: {student_data['name']}\n'
#                          f'Телефон: {student_data['phone']}\n'
#                          f'Курсы: {student_data['course']}\n'
#                          f'Кафедра: {student_data['department']}\n'
#                          f'город: {student_data["city"]}\n')
#     await state.clear()


# async def main():
#     await dp.start_polling(bot)

# asyncio.run(main())