import requests, time, json, os
from pathlib import Path

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FLIGHTS_API = os.getenv("FLIGHTS_API")

SEEN_FILE = Path("seen_flights.json")
if SEEN_FILE.exists():
    seen = set(json.loads(SEEN_FILE.read_text()))
else:
    seen = set()

def save_seen():
    SEEN_FILE.write_text(json.dumps(list(seen)))

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)

def fetch_flights():
    headers = {
        "Accept": "*/*",
        "Referer": "https://akb9.com/flights/",
        "User-Agent": "akb9-bot/1.0"
    }
    r = requests.get(FLIGHTS_API, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()

def format_flight(f):
    dep = f.get("dep") or f.get("departure") or "?"
    arr = f.get("arr") or f.get("arrival") or "?"
    fid = f.get("id") or f.get("flight_id") or str(f)
    return fid, f"✈️ {dep} → {arr}"

def main():
    global seen
    while True:
        try:
            data = fetch_flights()
            flights = data.get("flights") if isinstance(data, dict) else data
            for f in flights:
                fid, text = format_flight(f)
                if fid not in seen:
                    send_telegram(text)
                    seen.add(fid)
                    save_seen()
                    print("Sent:", text)
        except Exception as e:
            print("Error:", e)
        time.sleep(15 * 60)

if __name__ == "__main__":
    main()
