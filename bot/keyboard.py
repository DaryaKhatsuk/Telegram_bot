from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

start = types.ReplyKeyboardMarkup(resize_keyboard=True)
info = types.KeyboardButton('Inform')
stats = types.KeyboardButton('Statistic')
motorcycles = types.KeyboardButton('Motorcycles')

start.add(stats, info, motorcycles)

stats_keyb = InlineKeyboardMarkup()
stats_keyb.add(InlineKeyboardButton(f'yes', callback_data='join'))
stats_keyb.add(InlineKeyboardButton(f'no', callback_data='cancel'))

motorcycles_keyb = InlineKeyboardMarkup()
motorcycles_keyb.add(InlineKeyboardButton(f'Honda', callback_data='honda'))
