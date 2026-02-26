import time
import requests
import pygame
import pysrt
import os

VOICEVOX_URL = "http://127.0.0.1:50021"
SPEAKER_ID = 2   # 好きな話者に変更

pygame.mixer.init()

# SRT読み込み
subs = pysrt.open("script.srt", encoding="utf-8")


def synthesize(text, outfile):

    query = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={"text": text, "speaker": SPEAKER_ID}
    ).json()

    audio = requests.post(
        f"{VOICEVOX_URL}/synthesis",
        params={"speaker": SPEAKER_ID},
        json=query
    )

    with open(outfile, "wb") as f:
        f.write(audio.content)


def play_wav(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.05)


start_time = time.time()

print("Start training...")

os.makedirs("cache", exist_ok=True)

for i, sub in enumerate(subs):

    target = sub.start.ordinal / 1000
    text = sub.text.replace("\n", " ")

    # 時刻待ち
    while time.time() - start_time < target:
        time.sleep(0.05)

    wav = f"cache/voice_{i}.wav"

    if not os.path.exists(wav):
        print("Generate:", text)
        synthesize(text, wav)

    play_wav(wav)


print("Finished.")