from faster_whisper import WhisperModel
import json
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
segs, info = m.transcribe("audio.wav", language="he", word_timestamps=True, vad_filter=True, beam_size=5, initial_prompt="סיור בדירה באתונה לקראת שיפוץ עבור רד בריז. כניסה, לובי, מעלית, תקרה גבוהה, סלון, מרפסת, חדר שינה, מטבח, מחסן, מסדרון, משקיעים, שכירות לטווח קצר.", condition_on_previous_text=False)
out=[]
for s in segs:
    out.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"s":w.start,"e":w.end,"w":w.word} for w in s.words]})
    print(f"[{s.start:6.1f}-{s.end:6.1f}] {s.text}", flush=True)
json.dump(out, open("transcript.json","w"), ensure_ascii=False, indent=1)
