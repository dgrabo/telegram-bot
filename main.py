from dotenv import load_dotenv
import logging
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters
)


load_dotenv()
token = os.getenv("BOT_TOKEN")
google_api_key = os.getenv("GOOGLE_API_KEY")
# MENU, OPTION1, OPTION2 = range(3)

if not token:
    raise ValueError("BOT_TOKEN not loaded.")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Find restaurants", callback_data="find_restaurants")]]
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Option:", reply_markup=markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "find_restaurants":

        keyboard = [[KeyboardButton("Send Location\n(make sure that your GPS/location is on)", request_location=True)]]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await query.message.reply_text("Press the button for sharing the location\n(make sure that your GPS/location is on)", reply_markup=markup)

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    location_latitude = update.message.location.latitude
    location_longitude = update.message.location.longitude

    await update.message.reply_text(f'Your location: {location_latitude}, {location_longitude}')

def search_restaurants(lat, lng):
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": google_api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating"
    }
    body = {
        "includedTypes": ["restaurant"],
        "maxResultCount": 5,
        "locationRestriction":
        {
            "circle": {
                "center":{
                    "latitude": lat, "longitude": lng
                },
                "radius": 1000.0
            }
        }
    }
    response = requests.post(url, headers=headers, json=body)
    
    return response.json()

def main():
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))

    app.run_polling()

if __name__ == "__main__":
    main()