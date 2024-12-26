from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import random
from datetime import datetime, timedelta

# Ваш токен API от BotFather
API_TOKEN = "7719119088:AAFoRl0wLWy-0CESMlIKoyzey8-npWwfGCY"

# Словари для хранения данных пользователей
user_stars = {}
last_bonus_time = {}
last_activity = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_stars[user_id] = user_stars.get(user_id, 0)  # Инициализация звёзд, если пользователь новый

    await update.message.reply_text(
        "Добро пожаловать в Trix Magic!\n\n"
        "Используй команды:\n"
        "/predict - получить предсказание\n"
        "/stars - проверить количество звёзд\n"
        "/bonus - обменять звёзды на бонус"
    )

# Команда /predict
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    predictions = [
        "Сегодня тебя ждёт удача!",
        "Звёзды советуют быть осторожным.",
        "Этот день будет полон сюрпризов.",
    ]
    user_id = update.message.from_user.id
    user_stars[user_id] = user_stars.get(user_id, 0) + 1  # Добавить 1 звезду
    last_activity[user_id] = datetime.now()  # Обновить время активности

    await update.message.reply_text(
        f"✨ Твоё предсказание: {random.choice(predictions)}\n"
        f"⭐ Ты получил 1 звезду! У тебя теперь {user_stars[user_id]} звёзд."
    )

# Команда /stars
async def stars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    stars = user_stars.get(user_id, 0)
    await update.message.reply_text(f"⭐ У тебя {stars} звёзд!")

# Команда /bonus
async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_stars.get(user_id, 0) >= 5:  # Проверяем, достаточно ли звёзд
        user_stars[user_id] -= 5  # Снимаем 5 звёзд
        bonus_prediction = random.choice([
            "Твой бонус: сегодня отличный день для новых начинаний!",
            "Улыбка принесёт удачу.",
            "Избегай споров, и всё будет хорошо!",
        ])
        await update.message.reply_text(
            f"🎁 Бонусное предсказание: {bonus_prediction}\n"
            f"⭐ У тебя осталось {user_stars[user_id]} звёзд."
        )
    else:
        await update.message.reply_text("❌ У тебя недостаточно звёзд для бонуса. Накопи минимум 5 звёзд!")

# Команда /miniapp для открытия Mini App
async def miniapp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    stars = user_stars.get(user_id, 0)

    mini_app_url = f"https://trix-magic.github.io/trix-mini-app/?stars={stars}"
    keyboard = [[InlineKeyboardButton("Открыть Mini App", web_app=WebAppInfo(url=mini_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Нажмите на кнопку ниже, чтобы открыть Mini App:",
        reply_markup=reply_markup
    )

# Основная функция
def main():
    application = Application.builder().token(API_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("predict", predict))
    application.add_handler(CommandHandler("stars", stars))
    application.add_handler(CommandHandler("bonus", bonus))
    application.add_handler(CommandHandler("miniapp", miniapp))

    # Запуск вебхука
    application.run_webhook(
        listen="0.0.0.0",
        port=8080,
        webhook_url="https://08b6-2a00-1858-1022-c70b-58ce-63d4-1caf-9dcc.ngrok-free.app/webhook"
    )

if __name__ == "__main__":
    main()
