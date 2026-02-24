from dotenv import load_dotenv
import logging
import json
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

if not token:
    raise ValueError("BOT_TOKEN not loaded.")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("🍽 Find restaurants", callback_data="find_restaurants")]]
    
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Hello there!", reply_markup=markup)

async def radius_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "radius_500":
        context.user_data["radius"] = 500
    elif query.data == "radius_1000":
        context.user_data["radius"] = 1000
    else:
        context.user_data["radius"] = 2000
    
    keyboard = [[KeyboardButton("Send Location\n(make sure that your GPS/location is on)", request_location=True)]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await query.message.reply_text("Press the button for sharing the location\n(make sure that your GPS/location is on)", reply_markup=markup)
        

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "find_restaurants":
        keyboard = [[InlineKeyboardButton("500m", callback_data="radius_500")],[InlineKeyboardButton("1km", callback_data="radius_1000")],[InlineKeyboardButton("2km", callback_data="radius_2000")]]
        markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text("Chose search radius: ", reply_markup=markup)

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    try:
        location_latitude = update.message.location.latitude
        location_longitude = update.message.location.longitude
        radius = context.user_data.get("radius", 1000)

        results = search_restaurants(location_latitude, location_longitude, radius)
        if "places" not in results or len(results["places"]) == 0:
            await update.message.reply_text("No restaurants found nearby")
            return
        message = ""
        for place in results["places"]:
            displayName = place.get("displayName",{})
            name = displayName.get("text","N/A")
            location = place.get("location",{})
            loc_lati = location.get("latitude")
            loc_long = location.get("longitude")
            adress = place.get("formattedAddress", "N/A")
            rating = place.get("rating", "N/A")
            message += f"Restaurant: {name}\nAddress: {adress}\nRating: {rating}\n"
            if loc_lati and loc_long:
                message += f"Link: https://www.google.com/maps/search/?api=1&query={loc_lati},{loc_long}\n"
            else:
                message += "\n"
            
        keyboard = [[InlineKeyboardButton("🔄 Search again", callback_data="find_restaurants")]]
        markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(message, reply_markup=markup)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Something went wrong")




def search_restaurants(lat, lng, radius):
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": google_api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.location"
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
                "radius": radius
            }
        }
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    logger.info(json.dumps(data, indent=2, ensure_ascii=False))
    return data

def main():
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="find_restaurants"))
    app.add_handler(CallbackQueryHandler(radius_handler, pattern="^radius_"))
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))


    app.run_polling()

if __name__ == "__main__":
    main()