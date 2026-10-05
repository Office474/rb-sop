import subprocess, sys, os

SRC = "src.mp4"
CTA_DUR = 4.0
W, H = 1080, 1920

# Each reel: hook headline, list of source cuts, list of (src_start, src_end, text) cues
REELS = [
    dict(name="reel1_why_this_apartment", hook="למה בחרנו דווקא\\Nאת הדירה הזאת?",
         cuts=[(0.2, 22.8), (24.0, 26.3), (28.4, 42.3)],
         cues=[(0.2, 4.8, "אני רוצה להראות לכם דירה לפני שיפוץ, דירה שמתאימה לרד בריז"),
               (4.8, 7.4, "אסביר לכם למה הדירה הספציפית הזאת"),
               (7.6, 12.8, "נבחרה להיות משופצת עבור רד בריז"),
               (13.8, 19.1, "קודם כל תראו את הכניסה, את המבואה ואת חדר המדרגות"),
               (19.1, 22.8, "יש גם גרם מדרגות"),
               (24.0, 26.3, "וזו המעלית"),
               (28.4, 30.4, "המעלית במצב טוב ומתוחזקת ברמה טובה"),
               (30.4, 33.8, "סך הכל הבניין מתוחזק מאוד יפה, הכניסה מאוד יפה"),
               (34.1, 37.6, "בואו ניכנס לראות את הדירה מבפנים"),
               (37.8, 42.3, "מדובר בדירה של כמעט 80 מטר, 75 מטר")]),
    dict(name="reel2_3m_ceilings", hook="תקרה של 3 מטר\\N(וזה משנה הכל)",
         cuts=[(48.0, 64.8), (76.8, 80.3), (82.9, 90.1)],
         cues=[(48.0, 50.2, "אנחנו בדירה"),
               (50.2, 52.0, "אפשר לראות כמה מאפיינים די מיידית"),
               (52.0, 54.2, "התקרה פה די גבוהה"),
               (54.2, 56.0, "אתם יכולים לראות כמה היא גבוהה"),
               (56.0, 60.8, "זה בעצם 3 מטר"),
               (60.8, 64.8, "יש תחושת מרחב, ומאוד נעים לשהות בדירה"),
               (76.8, 80.3, "הדירה הזאת מאוד מוארת"),
               (82.9, 87.3, "ומחולקת כרגע לשני חדרי שינה ועוד מזווה"),
               (87.3, 90.1, "זו המזווה, מזווה גדולה")]),
    dict(name="reel3_light_and_balconies", hook="סלון מואר\\N+ שתי מרפסות",
         cuts=[(101.9, 105.9), (107.3, 115.3), (140.1, 151.5), (207.9, 217.7)],
         cues=[(101.9, 104.5, "בואו נמשיך לראות את החדרים הנוספים"),
               (104.5, 105.9, "זה הסלון"),
               (109.7, 111.2, "הסלון גם מואר"),
               (111.2, 115.3, "יש יציאה למרפסת"),
               (140.1, 143.4, "עכשיו נראה את החדר השני"),
               (143.4, 147.5, "היתרון שלו: יש לו גם מרפסת קטנה נוספת"),
               (147.5, 151.5, "לא מרפסת גדולה, אבל מרפסת שמכניסה הרבה אור"),
               (207.9, 212.6, "עכשיו אנחנו בחדר שיש לו יציאה למרפסת"),
               (212.6, 217.7, "המרפסת חזיתית, לרחוב חד סטרי ויחסית שקט")]),
    dict(name="reel4_renovation_plan", hook="מה משנים בשיפוץ?\\Nפותחים את החלל",
         cuts=[(76.8, 80.3), (82.9, 87.3), (173.4, 195.6)],
         cues=[(76.8, 80.3, "הדירה הזאת מאוד מוארת"),
               (82.9, 87.3, "ומחולקת כרגע לשני חדרי שינה ועוד מזווה"),
               (173.4, 179.0, "עכשיו נראה את החדר השני ואת חדר הרחצה"),
               (179.0, 181.6, "יש פה מסדרון קטן"),
               (181.6, 183.1, "את הקיר הזה כמובן נוריד"),
               (183.1, 187.6, "ונשפר עוד קירות, ככל שהמהנדס יאפשר לנו"),
               (187.6, 192.9, "לפתוח את הדירה, את החלל, ולהגדיל את התחושה"),
               (192.9, 195.6, "יש פה חדר רחצה קטן")]),
    dict(name="reel5_balcony_long_stay", hook="המרפסת שגורמת\\Nלדיירים להישאר",
         cuts=[(207.9, 217.7), (235.6, 252.8)],
         cues=[(207.9, 212.6, "עכשיו אנחנו בחדר שיש לו יציאה למרפסת"),
               (212.6, 217.7, "המרפסת חזיתית, לרחוב חד סטרי ויחסית שקט"),
               (235.6, 240.9, "חשוב לנו ברד בריז שגם המרפסת תהיה מקום נעים לשבת"),
               (240.9, 245.4, "אפשר לשים פה שולחן עם שני כיסאות, אפילו שני שולחנות"),
               (245.4, 249.8, "וזה מאפשר לדיירים להרגיש בבית ולהישאר תקופה ממושכת"),
               (249.8, 252.8, "גם לתיירים, וגם לשהיות ארוכות יותר")]),
]

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def map_time(cuts, t):
    off = 0.0
    for a, b in cuts:
        if a <= t <= b:
            return off + (t - a)
        if t < a:
            return off
        off += b - a
    return off

def chunks(text, maxw=4):
    w = text.split()
    n = max(1, -(-len(w) // maxw))
    size = -(-len(w) // n)
    return [" ".join(w[i:i + size]) for i in range(0, len(w), size)]

HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,HeeboX 900,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,6,2,2,80,80,560,177
Style: Hook,HeeboX 900,76,&H00000000,&H00000000,&H0000D7FF,&H0000D7FF,0,0,0,0,100,100,0,0,3,18,0,8,70,70,170,177
Style: CTA1,HeeboX 800,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,4,0,5,80,80,0,177
Style: CTA2,HeeboX 900,92,&H00000000,&H00000000,&H0000D7FF,&H0000D7FF,0,0,0,0,100,100,0,0,3,24,0,5,80,80,0,177

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

RLM = "\u200f"
def rtl(t):
    return RLM + t.replace("\\N", RLM + "\\N" + RLM) + RLM

def build_ass(r, total):
    lines = []
    content = total - CTA_DUR
    lines.append(f"Dialogue: 1,{ts(0)},{ts(content)},Hook,,0,0,0,,{{\\fad(250,0)}}{rtl(r['hook'])}")
    for a, b, text in r["cues"]:
        s, e = map_time(r["cuts"], a), map_time(r["cuts"], b)
        parts = chunks(text)
        L = sum(len(p) for p in parts)
        t = s
        for p in parts:
            d = (e - s) * len(p) / L
            lines.append(f"Dialogue: 0,{ts(t)},{ts(min(t + d, content))},Sub,,0,0,0,,{rtl(p)}")
            t += d
    c0 = content
    cta_a, cta_b, cta_c = rtl('רוצים לראות איך דירה כזו\\Nהופכת להשקעה מניבה?'), rtl('הירשמו לוובינר'), rtl('הקישור בביו')
    lines.append(f"Dialogue: 2,{ts(c0 + 0.2)},{ts(total)},CTA1,,0,0,0,,{{\\fad(300,0)\\pos(540,700)}}{cta_a}")
    lines.append(f"Dialogue: 2,{ts(c0 + 0.7)},{ts(total)},CTA2,,0,0,0,,{{\\fad(300,0)\\pos(540,1000)}}{cta_b}")
    lines.append(f"Dialogue: 2,{ts(c0 + 1.1)},{ts(total)},CTA1,,0,0,0,,{{\\fad(300,0)\\pos(540,1230)}}{cta_c}")
    return HEADER + "\n".join(lines) + "\n"

def render(r):
    content = sum(b - a for a, b in r["cuts"])
    total = content + CTA_DUR
    ass = f"out/{r['name']}.ass"
    open(ass, "w", encoding="utf-8").write(build_ass(r, total))
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for a, b in r["cuts"]:
        cmd += ["-ss", f"{a}", "-t", f"{b - a}", "-i", SRC]
    fc = []
    n = len(r["cuts"])
    for i in range(n):
        fc.append(f"[{i}:v]scale={W}:{H}:flags=lanczos,fps=30,setsar=1,format=yuv420p[v{i}];"
                  f"[{i}:a]aresample=48000,afade=t=in:d=0.04,afade=t=out:st={r['cuts'][i][1]-r['cuts'][i][0]-0.04}:d=0.04[a{i}]")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca]")
    fc.append(f"[cv]tpad=stop_mode=clone:stop_duration={CTA_DUR},"
              f"boxblur=20:2:enable='gte(t,{content})',"
              f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.45:t=fill:enable='gte(t,{content})',"
              f"subtitles={ass}:fontsdir=fonts[ov]")
    fc.append(f"[ca]loudnorm=I=-14:TP=-1.5:LRA=11,apad=whole_dur={total}[oa]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[ov]", "-map", "[oa]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-profile:v", "high",
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-t", f"{total}",
            "-movflags", "+faststart", f"out/{r['name']}.mp4"]
    subprocess.run(cmd, check=True)
    print(r["name"], f"{total:.1f}s", flush=True)

os.makedirs("out", exist_ok=True)
sel = sys.argv[1:] or [r["name"] for r in REELS]
for r in REELS:
    if r["name"] in sel:
        render(r)
