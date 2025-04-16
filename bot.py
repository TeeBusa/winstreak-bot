import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = '7490158178:AAHHy7CPu7GEr1OfONO546484K0F0Q9hBnw'  # replace this later

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Mock league list
leagues = {
    "Premier League": "EPL",
    "La Liga": "LL",
    "Serie A": "SA",
    "Bundesliga": "BL",
    "Ligue 1": "L1"
}

# Mock prediction data
mock_predictions = {
    "EPL": ["Liverpool vs Spurs – Home Win (72%)", "Arsenal vs Chelsea – Draw (54%)", "Man City vs Brentford – Home Win (81%)"],
    "LL": ["Real Madrid vs Valencia – Home Win (77%)", "Barcelona vs Betis – Home Win (68%)", "Sevilla vs Girona – Away Win (51%)"],
    "SA": ["Juve vs Napoli – Draw (48%)", "Inter vs Roma – Home Win (63%)", "Milan vs Lazio – Home Win (58%)"],
    "BL": ["Bayern vs Dortmund – Home Win (66%)", "Leipzig vs Leverkusen – Away Win (60%)", "Wolfsburg vs Mainz – Draw (45%)"],
    "L1": ["PSG vs Lyon – Home Win (80%)", "Marseille vs Rennes – Draw (52%)", "Lille vs Nice – Home Win (55%)"]
}

# /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("👋 Welcome to WinStreak AI!\n\nGet accurate football predictions based on stats.\n\nUse /leagues to see supported leagues or /predict to get today’s picks.")

# /leagues
@dp.message_handler(commands=['leagues'])
async def show_leagues(message: types.Message):
    reply = "🏆 Supported Leagues:\n"
    for league in leagues:
        reply += f"– {league}\n"
    await message.reply(reply)

# /predict
@dp.message_handler(commands=['predict'])
async def choose_league(message: types.Message):
    markup = InlineKeyboardMarkup()
    for name, code in leagues.items():
        markup.add(InlineKeyboardButton(text=name, callback_data=f"league_{code}"))
    await message.reply("Select a league for today’s predictions:", reply_markup=markup)

# Handle league selection
@dp.callback_query_handler(lambda c: c.data.startswith('league_'))
async def send_predictions(callback_query: types.CallbackQuery):
    code = callback_query.data.split("_")[1]
    predictions = mock_predictions.get(code, [])
    reply = "\n".join([f"🔹 {p}" for p in predictions])
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"📊 Predictions:\n{reply}")

# /plan
@dp.message_handler(commands=['plan'])
async def show_plan(message: types.Message):
    await message.reply("💼 Pricing plans coming soon!\nWe’ll offer free daily tips & paid advanced access.")

# /subscribe
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    await message.reply("🔐 Subscription system is coming soon.\nStay tuned!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
