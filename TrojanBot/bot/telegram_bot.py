import os
import logging
import asyncio
import telegram
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ApplicationBuilder
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        logger.info("Initializing Telegram Bot")
        self.app = None

    async def run_setup(self):
        for attempt in range(3):
            try:
                self.app = ApplicationBuilder().token(TOKEN).build()
                
                # Commands
                self.app.add_handler(CommandHandler("start", self.start))
                self.app.add_handler(CommandHandler("menu", self.show_menu))
                self.app.add_handler(CallbackQueryHandler(self.handle_button_click))
                await self.app.initialize()
                logger.info("Telegram bot initialized.")
                break
            except telegram.error.TimedOut as e:
                logger.warning(f"Attempt {attempt+1} failed: {e}")
                if attempt < 2:
                    await asyncio.sleep(3)
                else:
                    raise
        return self.app

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Welcome Boss! Use /menu to interact with trojan.")

    async def show_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [
                InlineKeyboardButton("📈 Show Price", callback_data="show_price"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
            ],
            [InlineKeyboardButton("❌ Close", callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

    async def handle_button_click(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        query = update.callback_query
        await query.answer()
        data = query.data

        if data == "show_price":
            await query.edit_message_text("Current price is $99.99 💰")
        elif data == "settings":
            await query.edit_message_text("Settings coming soon, boss 🛠️")
        elif data == "close":
            await query.delete_message()
