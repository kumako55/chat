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

# ============================================
# FLASK ENDPOINTS (For Render health checks)
# ============================================

@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "service": "Chat Reader",
        "channel": CHANNEL_HANDLE,
        "message": "Listening for !s commands"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/spin', methods=['POST'])
def spin_receiver():
    """Receive spin from HF (if needed)"""
    data = request.json
    print(f"📨 Spin received from HF: {data}")
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("="*50)
    print("🎯 PYCHAT CHAT READER")
    print(f"📡 Channel: {CHANNEL_HANDLE}")
    print(f"🎯 Target: {HF_SPACE_URL}")
    print("="*50)
    
    # Start chat reader in background
    threading.Thread(target=chat_reader, daemon=True).start()
    
    # Start Flask server
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
