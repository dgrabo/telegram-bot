# 🍽 Restaurant Finder Telegram Bot

A Telegram bot that helps users discover the best restaurants near their location using the Google Places API.

## Features

- **Location-based search** — Share your GPS location to find nearby restaurants
- **Adjustable search radius** — Choose between 500m, 1km, or 2km
- **Restaurant details** — View name, address, and rating for each result
- **Google Maps links** — Direct links for easy navigation to each restaurant
- **Search again** — Quick button to start a new search without restarting the bot

## Tech Stack

- Python
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [Google Places API (New)](https://developers.google.com/maps/documentation/places/web-service/overview)
- Deployed on [Render](https://render.com)

## Setup

### Prerequisites

- Python 3.10+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Google Cloud API Key with Places API enabled

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dgrabo/telegram-bot.git
   cd telegram-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory:
   ```
   BOT_TOKEN=your_telegram_bot_token
   GOOGLE_API_KEY=your_google_api_key
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

1. Open the bot on Telegram and send `/start`
2. Click **"🍽 Find restaurants"**
3. Choose a search radius (500m, 1km, or 2km)
4. Share your location using the location button
5. Browse the top 5 restaurants with ratings and Google Maps links
6. Click **"🔄 Search again"** to start a new search

## Deployment

The bot is deployed on Render as a Web Service with a lightweight health server for uptime monitoring. UptimeRobot pings the service every 5 minutes to prevent sleeping on the free tier.

## License

This project is for educational purposes.