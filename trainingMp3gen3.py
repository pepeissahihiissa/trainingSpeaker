import pysrt
from pydub import AudioSegment
import os

subs = pysrt.open("script.srt", encoding="utf-8")

timeline = AudioSegment.silent(duration=0)


for i, sub in enumerate(subs):

    start = sub.start.ordinal   # ms

    wav = f"cache/voice_{i}.wav"

    if not os.path.exists(wav):
        print("Missing:", wav)
        continue

    audio = AudioSegment.from_wav(wav)

    # 現在の長さ
    current = len(timeline)

    # 足りない分だけ無音を足す
    if start > current:
        gap = start - current
        timeline += AudioSegment.silent(duration=gap)

    # 音声を追加
    timeline += audio


# ===== 終端トリム =====

last_sub = subs[-1]
last_text = last_sub.text.replace("\n", "").strip()

char_count = len(last_text)

estimated = char_count * 200   # 1文字200ms
margin = 3000

end_time = last_sub.start.ordinal + estimated + margin

if len(timeline) > end_time:
    timeline = timeline[:end_time]


# ===== 保存 =====

timeline.export("training.wav", format="wav")
timeline.export("training.mp3", format="mp3", bitrate="128k")

print("Done:", len(timeline)/1000, "sec")