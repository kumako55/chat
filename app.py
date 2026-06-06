import pytchat
import time

VIDEO_ID = "3iMSKPNWP_w"

def read_chat():
    print(f"🎧 Listening to live chat...")
    print(f"📺 Video ID: {VIDEO_ID}")
    print("="*50)
    
    # force_replay=True is the key fix
    chat = pytchat.create(video_id=VIDEO_ID, force_replay=True)
    
    while chat.is_alive():
        try:
            data = chat.get()
            for c in data.items:
                print(f"[{c.datetime}] {c.author.name}: {c.message}")
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    try:
        read_chat()
    except KeyboardInterrupt:
        print("\n👋 Stopped")
