import requests
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def publish_file(chat_id, file_path, delay=0):
    
    if delay > 0:
        time.sleep(delay)
        
    if file_path.startswith("http"):
        file_url = file_url.replace("http://", "https://", 1)
        response = requests.post(f"{TELEGRAM_API}/sendDocument", data={"chat_id": chat_id, "document": file_path})
        print(f"chatid: \n{chat_id}\n")
        print(f"token: \n{TELEGRAM_API}\n")
        print(f"file: \n{file_path}\n")
        print(f"Respose: \n{response}\n")
    else:
        with open(file_path, "rb") as f:
            requests.post(
                f"{TELEGRAM_API}/sendDocument",
                data={"chat_id": chat_id},
                files={"document": f}
            )