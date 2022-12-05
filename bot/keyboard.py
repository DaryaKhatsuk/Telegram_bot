from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

start = types.ReplyKeyboardMarkup(resize_keyboard=True)
info = types.KeyboardButton('Inform')
stats = types.KeyboardButton('Statistic')
pols = types.KeyboardButton('Покажи пользователя')

start.add(stats, info, pols)

stats_keyb = InlineKeyboardMarkup()
stats_keyb.add(InlineKeyboardButton(f'yes', callback_data='join'))
stats_keyb.add(InlineKeyboardButton(f'no', callback_data='cancel'))

pols_keyb = InlineKeyboardMarkup()
pols_keyb.add(InlineKeyboardButton(f'хочу увидеть id', callback_data='pols_key'))
pols_keyb.add(InlineKeyboardButton(f'вернутся обратно', callback_data='back_start'))
