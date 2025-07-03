from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from products import categories

main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton(text=c)] for c in categories] + [[KeyboardButton(text="🧾 Оформить заказ")]]
)

def category_keyboard(category_name):
    items = categories[category_name]
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text=item)] for item in items] + [[KeyboardButton(text="⬅️ Назад")]]
    )

remove_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Удалить товар 🗑️")],
        [KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="🧾 Оформить заказ")]
    ]
)