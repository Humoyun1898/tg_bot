import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from products import categories, category_units
from keyboards import main_menu, category_keyboard, remove_menu
from storage import user_data

API_TOKEN = "8199829547:AAEhP9S6kjWFYxiX5U7mdHYjZA9e_RMeKTo"
OWNER_ID = 5914148670

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {"cart": [], "stage": "awaiting_name"}
    await message.answer("\U0001F44B Напишите название вашей фирмы или имя, если нет договора.")

@dp.message(F.text)
async def handle_text(message: Message):
    user_id = message.from_user.id
    state = user_data[user_id]["stage"]
    text = message.text

    if state == "awaiting_name":
        user_data[user_id]["name"] = text
        user_data[user_id]["stage"] = "choosing_category"
        await message.answer("Что вы хотите заказать?", reply_markup=main_menu)

    elif text in categories:
        user_data[user_id]["category"] = text
        user_data[user_id]["stage"] = "choosing_product"
        await message.answer(f"Выберите товар из раздела {text}:", reply_markup=category_keyboard(text))

    elif text == "⬅️ Назад":
        user_data[user_id]["stage"] = "choosing_category"
        await message.answer("Что вы хотите заказать?", reply_markup=main_menu)

    elif state == "choosing_product" and any(text in products for products in categories.values()):
        user_data[user_id]["product"] = text
        user_data[user_id]["stage"] = "awaiting_quantity"
        category = user_data[user_id]["category"]
        await message.answer(f"Введите количество {category_units[category]}:")

    elif state == "awaiting_quantity":
        if not text.isdigit():
            await message.answer("❌ Пожалуйста, введите число.")
            return
        product = user_data[user_id]["product"]
        user_data[user_id]["cart"].append((product, text))
        user_data[user_id]["stage"] = "choosing_category"
        await message.answer("✅ Товар добавлен в корзину.\nЧто вы хотите заказать ещё?", reply_markup=main_menu)

    elif text == "🧾 Оформить заказ":
        cart = user_data[user_id]["cart"]
        if not cart:
            await message.answer("🛒 Ваша корзина пуста.")
        else:
            summary = "\n".join([f"{p} — {q}" for p, q in cart])
            await message.answer(
                f"Ваш заказ:\n{summary}\n\nПодтвердить заказ? (да/нет)\nИли вы можете удалить товар.",
                reply_markup=remove_menu
            )

    elif text == "Удалить товар 🗑️":
        cart = user_data[user_id]["cart"]
        if not cart:
            await message.answer("🛒 Корзина пуста.")
            return
        delete_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        for p, q in cart:
            delete_kb.add(f"{p} — {q}")
        delete_kb.add("⬅️ Назад")
        user_data[user_id]["stage"] = "awaiting_delete"
        await message.answer("Выберите товар для удаления:", reply_markup=delete_kb)

    elif user_data[user_id]["stage"] == "awaiting_delete":
        product_line = text
        cart = user_data[user_id]["cart"]
        new_cart = [item for item in cart if f"{item[0]} — {item[1]}" != product_line]
        if len(cart) != len(new_cart):
            user_data[user_id]["cart"] = new_cart
            await message.answer("✅ Товар удалён.", reply_markup=main_menu)
        else:
            await message.answer("❌ Такой товар не найден.")
        user_data[user_id]["stage"] = "choosing_category"

    elif text.lower() == "да":
        name = user_data[user_id]["name"]
        summary = "\n".join([f"{p} — {q}" for p, q in user_data[user_id]["cart"]])
        await bot.send_message(OWNER_ID, f"📦 Новый заказ от {name}:\n{summary}")
        await message.answer("✅ Заказ оформлен. Спасибо!")
        user_data[user_id]["cart"] = []

    elif text.lower() == "нет":
        await message.answer("❌ Заказ отменён. Вы можете продолжить выбор.", reply_markup=main_menu)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
