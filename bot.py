import requests
import time
import os

# Load environment variables (Render does this automatically)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Flight API URL
FLIGHT_API = "https://akb9.com/flights/currentflights.json"

# Keep track of flights we’ve already sent
sent_flights = set()

def get_flight_data():
    """Fetch flight data from the API."""
    try:
        response = requests.get(FLIGHT_API)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error fetching flight data:", e)
        return None

def send_telegram_message(message):
    """Send a message to Telegram."""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, data=payload)
    except Exception as e:
        print("Error sending Telegram message:", e)

def check_flights():
    """Check for new flights and send updates."""
    global sent_flights
    data = get_flight_data()
    if not data:
        return

    # You might need to adjust this depending on the structure of the API
    for flight in data.get("flights", []):
        flight_id = flight.get("id")
        if flight_id not in sent_flights:
            sent_flights.add(flight_id)
            message = f"✈️ New flight detected:\n{flight}"
            send_telegram_message(message)
            print("Sent update for flight:", flight_id)

def main():
    """Run bot every 15 minutes."""
    print("Bot is running and checking every 15 minutes...")
    while True:
        check_flights()
        time.sleep(900)  # Wait 900 seconds = 15 minutes

if __name__ == "__main__":
    main()
