import threading
import pytchat
import time
import requests
import re

# ============================================
# 🔴 APNA CHANNEL HANDLE YAHAN DALO
# ============================================
CHANNEL_HANDLE = "@SoccerBlitzs"
# ============================================

spin_trigger = False

def chat_reader():
    global spin_trigger
    video_id = None
    
    print("🔍 Looking for live stream...")
    
    # Get video ID from channel handle
    while not video_id:
        try:
            url = f"https://www.youtube.com/{CHANNEL_HANDLE}/live"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers)
            match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', response.text)
            if match:
                video_id = match.group(1)
                print(f"✅ Live detected! Video ID: {video_id}")
            else:
                print("⏳ Waiting for live stream...")
                time.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)
    
    print("🎧 Listening to live chat...")
    print("💬 Type !s or !S in chat to SPIN!")
    
    chat = pytchat.create(video_id=video_id, force_replay=True)
    
    while chat.is_alive():
        try:
            data = chat.get()
            for c in data.items:
                msg = c.message.lower().strip()
                if msg == '!s' or msg == '!s':
                    print(f"🎡 SPIN COMMAND from {c.author.name}!")
                    spin_trigger = True
            time.sleep(1)
        except Exception as e:
            print(f"Chat error: {e}")
            time.sleep(5)

# Start chat reader in background
threading.Thread(target=chat_reader, daemon=True).start()

print("="*50)
print("🎯 CHAT READER STARTED")
print(f"📡 Channel: {CHANNEL_HANDLE}")
print("💬 Type !s or !S to spin")
print("="*50)

# Keep main thread alive
try:
    while True:
        time.sleep(1)
        if spin_trigger:
            print("🎯 SPIN TRIGGERED! (You can call your spin function here)")
            spin_trigger = False
except KeyboardInterrupt:
    print("\n👋 Stopped")
