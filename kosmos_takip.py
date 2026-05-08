import os
import hashlib
import json
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["8427789852:AAFpor05eEx8dqHxmH25CE9kJCsBj1yyyOg"]
CHAT_ID = os.environ["1683085249"]

URLS = [
    "https://kosmosvize.com.tr/",
    "https://kosmosvize.com.tr/tr-tr/duyurular",
]

HASH_DOSYASI = "hashler.json"

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

def hashleri_yukle():

    try:
        with open(HASH_DOSYASI, "r") as f:
            return json.load(f)

    except:
        return {}

def hashleri_kaydet(hashler):

    with open(HASH_DOSYASI, "w") as f:
        json.dump(hashler, f)

def kontrol_et():

    eski_hashler = hashleri_yukle()

    yeni_hashler = {}

    for url in URLS:

        try:

            text = sayfa_metni_al(url)

            mevcut_hash = hash_al(text)

            yeni_hashler[url] = mevcut_hash

            eski_hash = eski_hashler.get(url)

            if eski_hash and eski_hash != mevcut_hash:

                telegram_gonder(
                    f"Kosmos sitesinde değişiklik algılandı:\n{url}"
                )

        except Exception as e:

            telegram_gonder(
                f"Hata oluştu:\n{url}\n{str(e)}"
            )

    hashleri_kaydet(yeni_hashler)

if __name__ == "__main__":
    kontrol_et()
