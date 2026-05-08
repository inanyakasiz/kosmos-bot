import os
import hashlib
import json
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URLS = [
    "https://kosmosvize.com.tr/",
    "https://kosmosvize.com.tr/tr-tr/duyurular",
    "https://x.com/Kosmos_Vize",
]

HASH_DOSYASI = "hashler.json"

def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mesaj}, timeout=20)

def sayfa_metni_al(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return soup.get_text(" ", strip=True).lower()

def hash_al(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def hashleri_yukle():
    try:
        with open(HASH_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def hashleri_kaydet(hashler):
    with open(HASH_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(hashler, f, ensure_ascii=False, indent=2)

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
                    f"Kosmos tarafında değişiklik algılandı:\n{url}"
                )

        except Exception as e:
            telegram_gonder(
                f"Kontrol hatası:\n{url}\n{str(e)}"
            )

    hashleri_kaydet(yeni_hashler)

if __name__ == "__main__":
    kontrol_et()
