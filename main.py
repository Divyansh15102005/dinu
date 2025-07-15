from keep_alive import keep_alive
keep_alive()

from flask import Flask
import threading
import asyncio
import nest_asyncio
import datetime
from pymongo import MongoClient
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
)
import os

nest_asyncio.apply()

# Flask app initialization
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running"

def run_flask():
    app.run(host='0.0.0.0', port=8081)

# MongoDB and Bot setup using env vars
MONGO_URI = os.environ.get("MONGO_URI")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

client = MongoClient(MONGO_URI)
db = client["mlm_bot"]
users = db["users"]
transactions = db["transactions"]

ADMIN_ID = 5856521394
UPI_ID = "9889036619@pthdfc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ref = int(context.args[0]) if context.args else None

    if not users.find_one({"user_id": user.id}):
        users.insert_one({
            "user_id": user.id,
            "username": user.username,
            "ref_by": ref,
            "points": 0,
            "paid": False,
            "joined": datetime.datetime.now()
        })
        await update.message.reply_text(
            "🎉 बधाई हो! आपने बॉट को जॉइन कर लिया है।\n\n"
            "💼 Network Marketing Plan:\n"
            "✅ ₹500 में इस बॉट का Premium Member बनें\n"
            "✅ और referral से ₹20,000 से ₹30,000+ महीना तक कमाएँ\n\n"
            "💸 Referral Commission Structure:\n"
            "👥 Level 1 (Direct): ₹200 प्रति सदस्य\n"
            "👥 Level 2: ₹120 प्रति सदस्य\n"
            "👥 Level 3: ₹80 प्रति सदस्य\n\n"
            "🔐 Important:\n"
            "बिना ₹500 पेमेंट किए आप रेफरल लिंक नहीं बना सकते और कमाई शुरू नहीं होगी।\n\n"
            "🪙 पेमेंट के लिए /pay कमांड भेजें।\n"
            "🙋‍♂ और मदद के लिए /help टाइप करें।"
        )
    else:
        await update.message.reply_text(
            "✅ आप पहले से रजिस्टर हैं।\n"
            "💡 कमाई शुरू करने के लिए ₹500 पे करें – /pay टाइप करें।"
        )

# (All other handlers remain unchanged — paste your logic from earlier code here)

# ... referral_link, approve_payment, myteam, profile, etc.

async def main():
    print("✅ MongoDB Connected")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("referral_link", referral_link))
    app.add_handler(MessageHandler(filters.Regex(r"^/approve_\d+$"), approve_payment))
    app.add_handler(CommandHandler("myteam", myteam))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("top_referrers", top_referrers))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("teamtree", teamtree))
    app.add_handler(CommandHandler("rewards", rewards))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("level", level))
    app.add_handler(CommandHandler("pay", pay))
    app.add_handler(CommandHandler("confirm_payment", confirm_payment))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("transactions", transactions_cmd))

    print("🤖 Bot is running...")
    await app.run_polling()

# Start Flask server in background
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Run Bot
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
