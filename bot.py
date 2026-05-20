from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

TOKEN = "8358059992:AAEeN1OKZbTGX_9YTFtsDJ6I5uNzjloguss"

# ВСТАВЬ СВОЙ TELEGRAM ID
ADMIN_ID = 5774291749

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# ===== СОСТОЯНИЯ =====

class BuyStars(StatesGroup):
    waiting_for_screenshot = State()


# ===== START =====

@dp.message(CommandStart())
async def start(message: types.Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⭐ 50 Stars",
                    callback_data="buy_50"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐ 100 Stars",
                    callback_data="buy_100"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐ 200 Stars",
                    callback_data="buy_200"
                )
            ]
        ]
    )

    await message.answer(
        "⭐ Добро пожаловать в Nova Stars Market!\n\n"
        "Выберите количество Stars:",
        reply_markup=keyboard
    )


# ===== ВЫБОР STARS =====

@dp.callback_query()
async def buy(callback: types.CallbackQuery, state: FSMContext):

    if callback.data == "buy_50":

        await state.update_data(stars="50")

        await callback.message.answer(
            "💳 Для оплаты переведите 75₽\n\n"
            "СБП:\n"
            "+79624481471\n\n"
            "После оплаты отправьте скриншот."
        )

        await state.set_state(BuyStars.waiting_for_screenshot)


    elif callback.data == "buy_100":

        await state.update_data(stars="100")

        await callback.message.answer(
            "💳 Для оплаты переведите 175₽\n\n"
            "СБП:\n"
            "+79624481471\n\n"
            "После оплаты отправьте скриншот."
        )

        await state.set_state(BuyStars.waiting_for_screenshot)


    elif callback.data == "buy_200":

        await state.update_data(stars="200")

        await callback.message.answer(
            "💳 Для оплаты переведите 275₽\n\n"
            "СБП:\n"
            "+79624481471\n\n"
            "После оплаты отправьте скриншот."
        )

        await state.set_state(BuyStars.waiting_for_screenshot)

    await callback.answer()


# ===== СКРИНШОТ =====

@dp.message(BuyStars.waiting_for_screenshot)
async def screenshot(message: types.Message, state: FSMContext):

    if message.photo:

        data = await state.get_data()
        stars = data.get("stars")

        username = message.from_user.username

        # Пользователю
        await message.answer(
            "✅ Оплата отправлена на проверку.\n\n"
            "Ожидайте, в скором времени Stars будут выданы ⭐"
        )

        # Админу
        await bot.send_message(
            ADMIN_ID,
            f"🛒 Новый заказ!\n\n"
            f"👤 Username: @{username}\n"
            f"⭐ Stars: {stars}"
        )

        # Скрин админу
        await bot.send_photo(
            ADMIN_ID,
            photo=message.photo[-1].file_id
        )

        await state.clear()

    else:
        await message.answer(
            "❌ Пожалуйста, отправьте скриншот оплаты."
        )


# ===== ЗАПУСК =====

async def main():
    await dp.start_polling(bot)


asyncio.run(main())