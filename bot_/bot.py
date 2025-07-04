import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart

from tg_bot.src.products import categories, category_units
from tg_bot.src.keyboards import main_menu, category_keyboard, remove_menu
from tg_bot.src.storage import user_data



API_TOKEN = os.getenv("API_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {"cart": [], "stage": "awaiting_name"}
    await message.answer("👋 Добро пожаловать!\nНапишите название вашей фирмы или имя, если нет договора.")

@dp.message(F.text)
async def process(message: Message):
    user_id = message.from_user.id
    text = message.text
    state = user_data[user_id]["stage"]

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

    elif state == "choosing_product" and any(text in items for items in categories.values()):
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
        await message.answer("✅ Товар добавлен в корзину.\nВыберите категорию или оформите заказ.", reply_markup=main_menu)

    elif text == "🧾 Оформить заказ":
        cart = user_data[user_id]["cart"]
        if not cart:
            await message.answer("🛒 Ваша корзина пуста.")
        else:
            summary = "\n".join([f"{p} — {q}" for p, q in cart])
            await message.answer(
                f"Ваш заказ:\n{summary}\n\nПодтвердить заказ? (да/нет)",
                reply_markup=remove_menu
            )

    elif text == "Удалить товар 🗑️":
        cart = user_data[user_id]["cart"]
        if not cart:
            await message.answer("🛒 Корзина пуста.")
            return
        kb = [[f"{p} — {q}"] for p, q in cart] + [["⬅️ Назад"]]
        reply_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text=item[0])] for item in kb])
        user_data[user_id]["stage"] = "awaiting_delete"
        await message.answer("Выберите товар для удаления:", reply_markup=reply_kb)

    elif state == "awaiting_delete":
        cart = user_data[user_id]["cart"]
        product_line = text
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