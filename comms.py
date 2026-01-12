import requests
import threading
import cv2
import os
from datetime import datetime

# --- CREDENTIALS (VERIFIED) ---
BOT_TOKEN = "8510508200:AAGQmgYGJt5pyyjMZT0RkzBD3bTHnON47t4" 
CHAT_ID = "5137505210"

def send_telegram_photo(image_path, caption="🚨 INTRUDER DETECTED"):
    """
    Sends the photo to Telegram API.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    print(f"   [Step 2] Uploading {image_path} to Telegram...") 
    
    try:
        with open(image_path, 'rb') as f:
            files = {'photo': f}
            data = {'chat_id': CHAT_ID, 'caption': caption}
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                print("   [Step 3] ✅ SUCCESS: Alert Sent!")
            else:
                print(f"   [Step 3] ❌ FAILED: {response.text}")

    except Exception as e:
        print(f"   [Step 3] ❌ ERROR: {e}")

def trigger_alert(frame):
    """
    Saves frame and starts a background thread to upload it.
    """
    # 1. Check Folder
    if not os.path.exists("alerts"):
        os.makedirs("alerts")
        print("   [Info] Created 'alerts' folder.")

    # 2. Save Image locally
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"alerts/intruder_{timestamp}.jpg"
    
    success = cv2.imwrite(filename, frame)
    
    if success:
        print(f"   [Step 1] Photo saved: {filename}")
        # 3. Start Upload Thread
        t = threading.Thread(target=send_telegram_photo, args=(filename,))
        t.start()
    else:
        print("   [Error] Could not save photo! Check permissions.")