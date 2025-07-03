from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from products import categories

main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton(text=c)] for c in categories] + [[KeyboardButton(text="🧾 Оформить заказ")]]
)

def category_keyboard(category_name):
    from products import categories
    items = categories[category_name]
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text=item)] for item in items] + [[KeyboardButton(text="⬅️ Назад")]]
    )