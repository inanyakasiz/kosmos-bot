
import time
import hashlib
import requests
from bs4 import BeautifulSoup

BOT_TOKEN =  "8427789852:AAFpor05eEx8dqHxmH25CE9kJCsBj1yyyOg"
CHAT_ID = "1683085249"

URLS = [
    "https://kosmosvize.com.tr/",
    "https://kosmosvize.com.tr/tr-tr/duyurular",
]

KONTROL_ARALIGI = 300  # 5 dakika

def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": mesaj
        },
        timeout=20
    )

def sayfa_metni_al(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=30)

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return soup.get_text(" ", strip=True).lower()

def hash_al(text):
    return hashlib.sha256(text.encode()).hexdigest()

def kontrol_et():

    onceki_hashler = {}

       telegram_gonder("Kosmos kontrolü başladı.")

    for url in URLS:

        try:
            text = sayfa_metni_al(url)
            mevcut_hash = hash_al(text)

            telegram_gonder(
                f"Kosmos kontrol edildi:\n{url}"
            )

        except Exception as e:
            telegram_gonder(
                f"Hata oluştu:\n{url}\n{str(e)}"
            )

if __name__ == "__main__":
    kontrol_et()
