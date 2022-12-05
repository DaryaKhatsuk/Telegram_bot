from typing import Optional

from aiogram import Bot, executor, types
import asyncio
import logging
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from bot import config, keyboard
import os
from io import BytesIO

storage = MemoryStorage()  # FSM
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(
    # указываем название с логами
    filename='log.txt',
    # указываем уровень логирования
    level=logging.INFO,
    # указываем формат сохранения логов
    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s '
           u'[%(asctime)s] %(message)s')


class Me_info(StatesGroup):
    Q1 = State()  # задаем состояние 1
    Q2 = State()  # задаем состояние 2


@dp.message_handler(Command('me'), storage=None)
async def enter_me_info(message: types.Message):
    if message.chat.id == config.admin:
        await message.answer("Начинаем настройку \n"
                             "1. Укажите ссылку на Ваш профиль")
        await Me_info.Q1.set()


@dp.message_handler(state=Me_info.Q1)
# нашей функции мы указываем, что хотим получить сообщение и состояние
async def answer_for_state_Q1(message: types.Message, state: FSMContext):
    # сохраняем текст полученного сообщения
    answer = message.text
    # в данном месте прописываем для нашего состояния обновление данных
    # в пространство имен для текущего состояния
    # мы добавляем ключ answer1 со значением answer, далее мы в этом убедимся
    await state.update_data(answer1=answer)
    # после чего выводим сообщение
    await message.answer("Ваша ссылка сохранена \n"
                         "2. Введите текст")
    # и задаем состояние Q2
    await Me_info.Q2.set()


@dp.message_handler(state=Me_info.Q2)
async def answer_for_state_Q2(message: types.Message, state: FSMContext):
    # записываем ответ
    answer = message.text
    # Снова в пространство имен добавляем answer2 со значением answer, т.е. с текстом пользователя
    await state.update_data(answer2=answer)
    # говорим боту отправить сообщение
    await message.answer("Текст сохранен")
    # в переменную data получаем словарь, хранящийся в нашем хранилище состояний для текущего состояния
    data = await state.get_data()
    # print(data)
    # достаем значение по ключу answer1
    answer1 = data.get("answer1")
    # достаем значение по ключу answer2
    answer2 = data.get("answer2")
    # открываем файл link.txt на режим записи в кодировке UTF-8
    with open("link.txt", 'w', encoding="UTF-8") as link_txt:
        # записываем строкой ссылку в наш файл
        link_txt.write(str(answer1))
    # открываем файл text.txt в режиме записи в той же кодировке
    with open("text.txt", "w", encoding="UTF-8") as text_txt:
        # записываем в файл текст, который передал пользователь
        text_txt.write(str(answer2))
    # говорим боту отправить сообщение
    await message.answer(f"Ваша ссылка на профиль: {answer1} \n"
                         f"Ваш текст: {answer2}")
    # закрываем текущее состояние
    await state.finish()


@dp.message_handler(Command('start'), state=None)
async def welcome(message):
    joinedFile = open('user.txt', 'r')
    joinedUsers = set()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open('user.txt', 'a')
        joinedFile.write(str(message.chat.id) + '\n')
        joinedUsers.add(message.chat.id)

    await bot.send_message(message.chat.id, f'Hello, *{message.from_user.first_name},* bot worked',
                           reply_markup=keyboard.start, parse_mode='Markdown')


@dp.callback_query_handler(text_contains='pols_key')
async def pols_key(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Ваш id: {call.message.chat.id}', parse_mode='Markdown')


@dp.callback_query_handler(text_contains='back_start')
async def back_start(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Вы вернулись в главное меню")


@dp.callback_query_handler(text_contains='join')
async def join(call: types.CallbackQuery):
    if call.message.chat.id == config.admin:
        d = sum(1 for line in open('user.txt'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Statistic: {d}', parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'You are not an administrator.')


@dp.callback_query_handler(text_contains='cancel')
async def cancel(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Вы вернулись в главное меню")


@dp.message_handler(commands='info')
async def cmd_test1(message: types.Message):
    await message.reply("I'm evil")


@dp.message_handler(commands='rassilka')
async def rassilka(message):
    if message.chat.id == config.admin:
        await bot.send_message(message.chat.id, f'*Рассылка началась*'
                                                f'\n*Бот оповестит когда закончит*', parse_mode='Markdown')
        receive_users, block_users = 0, 0
        joinedFile = open('user.txt', 'r')
        joinedUsers = set()
        print('open')
        for line in joinedFile:
            joinedUsers.add(line.strip())
        joinedFile.close()
        for user in joinedUsers:
            try:
                print('wait')
                await bot.send_photo(user, open('photo.png', 'rb'))
                receive_users += 1
            except:
                block_users += 1
            await asyncio.sleep(0.4)
        await bot.send_message(message.chat.id,  f'*Рассылка закончилась*\n'
                                                 f'получили сообщение: *{receive_users}*\n'
                                                 f'заблокировали бота: *{block_users}*', parse_mode='Markdown')


@dp.message_handler(content_types='text')
async def get_message(message):
    if message.text == 'Inform':
        await bot.send_message(message.chat.id, text='Information!\n The bot is designed for learning!',
                               parse_mode='Markdown')
    if message.text == 'Statistic':
        await bot.send_message(message.chat.id, text=f'{message.chat.first_name}, do you want see static?',
                               reply_markup=keyboard.stats_keyb, parse_mode='Markdown')
    if message.text == 'Покажи пользователя':
        await bot.send_message(message.chat.id, text='Выберите вариант', reply_markup=keyboard.pols_keyb,
                               parse_mode='Markdown')
    if message.text == 'Добавить фото':
        await bot.send_message(message.chat.id, text='Вставьте фото для сохранения')
        find_type = await bot.send_photo(message.chat.id, message)
        # print(find_type)
        # file_photo = bot.send_photo(find_type)
        direct = os.open('photo_user',)

        full = os.write('photo_user', str(find_type))
        # full.close()
        print(1)
        # with open('photo_user', 'rb') as file_safe:
        #     print(2)
        #     file_safe.write(file_photo)
        #     print(3)
        # await bot.send_message(message.chat.id, text='Фото сохранено')

    if message.text == 'Показать фото из галереи':
        list_photo = os.listdir('photo_user')
        await bot.send_message(message.chat.id, text='Ваши фото')
        for i in list_photo:
            await bot.send_photo(message.chat.id, open('photo_user/' + i, 'rb'))
        await bot.send_message(message.chat.id, text='Все фото показаны')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
