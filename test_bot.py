import requests

# PASTE YOUR KEYS HERE AGAIN TO BE SURE
BOT_TOKEN = "8510508200:AAGQmgYGJt5pyyjMZT0RkzBD3bTHnON47t4"
CHAT_ID = "5137505210"

def test_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": "⚠️ TEST ALERT: Connection Successful!"}
    
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

test_message()