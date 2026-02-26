from dotenv import load_dotenv
import logging
import os
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from health import run_health_server
from threading import Thread
from handlers import start, button_handler, radius_handler, location_handler



load_dotenv()
token = os.getenv("BOT_TOKEN")

if not token:
    raise ValueError("BOT_TOKEN not loaded.")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="find_restaurants"))
    app.add_handler(CallbackQueryHandler(radius_handler, pattern="^radius_"))
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))

    Thread(target=run_health_server, daemon=True).start()
    app.run_polling()

if __name__ == "__main__":
    main()