import pytchat
import time
import requests
import re
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# ============================================
# 🔴 APNI DETAILS YAHAN DALO
# ============================================
CHANNEL_HANDLE = "@SoccerBlitzs"
HF_SPACE_URL = "https://asad235-youtube.hf.space"  # 🔴 APNA HF SPACE URL
# ============================================

spin_trigger = False

def get_video_id_from_handle():
    try:
        url = f"https://www.youtube.com/{CHANNEL_HANDLE}/live"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', response.text)
        if match:
            return match.group(1)
        return None
    except:
        return None

def send_spin_to_hf():
    try:
        requests.post(f"{HF_SPACE_URL}/spin", json={"command": "spin"}, timeout=2)
        print("✅ Spin sent to HF!")
    except:
        pass

def chat_reader():
    global spin_trigger
    video_id = None
    
    print("🔍 Looking for live stream...")
    
    while not video_id:
        video_id = get_video_id_from_handle()
        if video_id:
            print(f"✅ Live detected! Video ID: {video_id}")
        else:
            print("⏳ Waiting...")
            time.sleep(10)
    
    print("🎧 Listening (pytchat)...")
    print("💬 Type !s or !S to spin!")
    
    chat = pytchat.create(video_id=video_id, force_replay=True)
    
    while chat.is_alive():
        try:
            data = chat.get()
            for c in data.items:
                msg = c.message.lower().strip()
                if msg == '!s' or msg == '!s':
                    print(f"🎡 SPIN! from {c.author.name}")
                    send_spin_to_hf()
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    print("="*50)
    print("🎯 PYCHAT CHAT READER")
    print(f"📡 Channel: {CHANNEL_HANDLE}")
    print("="*50)
    
    threading.Thread(target=chat_reader, daemon=True).start()
    
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
