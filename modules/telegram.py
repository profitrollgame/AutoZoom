import time
import requests

from modules.functions import configGet, configSet

def telegramSendText(message, force=False, token=configGet("token", "telegram")):
    if configGet("enabled", "telegram") or force:
        try:
            requests.post(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={configGet("user_id", "telegram")}&text={message}&parse_mode=markdown')
        except:
            pass

def telegramLink(token):
    try:
        code = 
        while True:
            answer = requests.post(f"https://api.telegram.org/bot{token}/getUpdates").json()
            for entry in answer["result"]:
                if "message" in entry:
                    if str(code) in entry["message"]["text"]:
                        telegramSendText("Бот успешно привязан к AutoZoom!", force=True, token=token)
                        configSet("user_id", entry["message"]["from"]["id"], "telegram")
                        print(f"Бот успешно привязан к аккаунту {entry['message']['from']['first_name']}!")
                        return {"success": True, "user_id": entry["message"]["from"]["id"]}
            time.sleep(1)
    except KeyboardInterrupt:
        return {"success": False, "user_id": None}