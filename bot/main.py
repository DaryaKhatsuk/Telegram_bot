from aiogram import Bot, executor, types
import logging
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot import config, keyboard
import re
import json
import parser

storage = MemoryStorage()  # FSM
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(
    # указываем название с логами
    filename='log.txt',
    # указываем уровень логирования
    level=logging.INFO,
    # указываем формат сохранения логов
    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s')


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


@dp.message_handler(commands='info')
async def cmd_test1(message: types.Message):
    await message.reply("I'm evil")


@dp.message_handler(content_types='text')
async def get_message(message):
    if message.text == 'Inform':
        await bot.send_message(message.chat.id, text='Information!\n The bot is designed for learning!',
                               parse_mode='Markdown')
    if message.text == 'Statistic':
        await bot.send_message(message.chat.id, text=f'{message.chat.first_name}, do you want see static?',
                               reply_markup=keyboard.stats_keyb, parse_mode='Markdown')
    if message.text == 'Motorcycles':
        await bot.send_message(message.chat.id, text=f'What brand of motorcycles do you want to see?',
                               reply_markup=keyboard.motorcycles_keyb, parse_mode='Markdown')


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


@dp.callback_query_handler(text_contains='honda')
async def honda(call: types.CallbackQuery):
    honda = {}
    with open('cars.json', newline='', encoding='UTF-8') as file:
        data = json.load(file)
        for i in data:
            if re.findall(r'https+.+/honda/+.+\d{9}', str(i)):
                honda.update(i)
    output_honda = []
    # for it in honda:
    #     for i, j in it.items():
    #         output_honda += str(i) * (j.index(it) + 1)
    #         print(output_honda)
    for i, j in honda.items():
        # print(i, j)
        # for j in honda.items():
        output_honda.append(i)
        output_honda.append(j)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"{str(output_honda)}\n",
                                        parse_mode='Markdown')
    print(honda.keys())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
