"""Reel 1 – enhanced visual version: animated hook, location tag, build-up checklist,
sqm counter, punch-in zooms, cut flashes, pop-in highlighted subtitles, progress bar,
SFX and animated CTA."""
import subprocess, os
from build import SRC, W, H, ts, map_time, chunks, rtl

CTA_DUR = 4.0
NAME = "reel1_why_this_apartment_VISUAL"

# (src_start, src_end, zoom) — zoom "push" = slow push-in, number = static punch-in
SUBCUTS = [(0.2, 4.8, "push"), (4.8, 7.6, 1.12), (7.6, 13.8, 1.0), (13.8, 19.1, 1.12),
           (19.1, 22.8, 1.0), (24.0, 26.3, 1.15), (28.4, 30.4, 1.0), (30.4, 34.0, 1.12),
           (34.0, 37.8, 1.0), (37.8, 42.3, 1.1)]
CUTS = [(a, b) for a, b, _ in SUBCUTS]

CUES = [(0.2, 4.8, "אני רוצה להראות לכם דירה לפני שיפוץ, דירה שמתאימה לרד בריז"),
        (4.8, 7.4, "אסביר לכם למה הדירה הספציפית הזאת"),
        (7.6, 12.8, "נבחרה להיות משופצת עבור רד בריז"),
        (13.8, 19.1, "קודם כל תראו את הכניסה, את המבואה ואת חדר המדרגות"),
        (19.1, 22.8, "יש גם גרם מדרגות"),
        (24.0, 26.3, "וזו המעלית"),
        (28.4, 30.4, "המעלית במצב טוב ומתוחזקת ברמה טובה"),
        (30.4, 33.8, "סך הכל הבניין מתוחזק מאוד יפה, הכניסה מאוד יפה"),
        (34.1, 37.6, "בואו ניכנס לראות את הדירה מבפנים"),
        (37.8, 42.3, "מדובר בדירה של כמעט 80 מטר, 75 מטר")]

KEYWORDS = {"שיפוץ", "רד", "בריז", "משופצת", "הכניסה", "המבואה", "המעלית", "מתוחזקת",
            "מתוחזק", "80", "75", "יפה"}
CHECKLIST = [(13.8, "כניסה ומבואה מרשימות"), (24.0, "מעלית תקינה"), (30.4, "בניין מתוחזק")]
COUNTER_AT, COUNTER_TO = 37.8, 75

YEL = "&H0000D7FF&"
HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,HeeboX 900,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,3,2,80,80,560,177
Style: Hook,HeeboX 900,92,&H00000000,&H00000000,&H0000D7FF,&H0000D7FF,0,0,0,0,100,100,0,0,3,22,0,5,60,60,0,177
Style: Mini,HeeboX 900,50,&H00000000,&H00000000,&H0000D7FF,&H0000D7FF,0,0,0,0,100,100,0,0,3,12,0,5,60,60,0,177
Style: Tag,HeeboX 800,46,&H00FFFFFF,&H00FFFFFF,&H50000000,&H50000000,0,0,0,0,100,100,0,0,3,14,0,5,60,60,0,177
Style: Chk,HeeboX 800,52,&H00FFFFFF,&H00FFFFFF,&H40000000,&H40000000,0,0,0,0,100,100,0,0,3,14,0,6,60,60,0,177
Style: Shape,HeeboX 900,10,&H0000D7FF,&H0000D7FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,177
Style: Big,HeeboX 900,230,&H0000D7FF,&H0000D7FF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,10,6,5,0,0,0,177
Style: BigLbl,HeeboX 900,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,6,3,5,0,0,0,177
Style: CTA1,HeeboX 800,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,4,0,5,80,80,0,177
Style: CTA2,HeeboX 900,96,&H00000000,&H00000000,&H0000D7FF,&H0000D7FF,0,0,0,0,100,100,0,0,3,26,0,5,80,80,0,177

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

CIRCLE = "m 26 0 b 40 0 52 12 52 26 b 52 40 40 52 26 52 b 12 52 0 40 0 26 b 0 12 12 0 26 0"
CHECK = "m 13 27 l 22 36 l 39 17 l 44 22 l 22 44 l 8 31"
ARROW = "m 0 0 l 64 0 l 32 38"


def ev(lines, layer, a, b, style, text):
    lines.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{text}")


def highlight(chunk):
    # libass breaks bidi across color-tag runs, so emit words in visual (left-to-right)
    # order, each forced LTR with LRO/PDF, colouring keywords.
    from bidi.algorithm import get_display
    LRO, PDF = "\u202d", "\u202c"
    words = chunk.split()[::-1]
    out = []
    for w in words:
        col = YEL if w.strip(",.?!") in KEYWORDS else "&HFFFFFF&"
        out.append(f"{{\\c{col}}}{LRO}{get_display(w, base_dir='R')}{PDF}")
    return f"{{\\c&HFFFFFF&}}{LRO} {PDF}".join(out)


def build_ass(content, total):
    L = []
    m = lambda t: map_time(CUTS, t)
    # progress bar (fills right-to-left)
    ev(L, 9, 0, content, "Shape", "{\\an7\\pos(0,0)\\1c&HFFFFFF&\\1a&HA0&\\p1}m 0 0 l 1080 0 l 1080 12 l 0 12{\\p0}")
    ev(L, 10, 0, content, "Shape", f"{{\\an7\\pos(0,0)\\clip(1080,0,1080,12)\\t(0,{int(content*1000)},\\clip(0,0,1080,12))\\p1}}m 0 0 l 1080 0 l 1080 12 l 0 12{{\\p0}}")
    # hook: big pop, then shrinks to a mini header for the rest of the reel
    hook_end = m(4.8)
    ev(L, 6, 0, hook_end, "Hook", "{\\pos(540,330)\\fscx20\\fscy20\\t(0,220,\\fscx112\\fscy112)\\t(220,340,\\fscx100\\fscy100)\\fad(0,150)}" + rtl("למה בחרנו דווקא\\Nאת הדירה הזאת?"))
    ev(L, 6, hook_end, content, "Mini", "{\\pos(540,120)\\fad(200,0)}" + rtl("למה דווקא הדירה הזאת?"))
    ev(L, 6, 0.5, hook_end, "Tag", "{\\pos(540,495)\\fad(250,150)}" + rtl("אתונה, יוון  |  לפני שיפוץ"))
    # checklist build-up
    for i, (src_t, text) in enumerate(CHECKLIST):
        a, y = m(src_t), 260 + i * 100
        ev(L, 7, a, content, "Shape", f"{{\\an5\\pos(1000,{y})\\fscx0\\fscy0\\t(0,180,\\fscx120\\fscy120)\\t(180,280,\\fscx100\\fscy100)\\p1}}{CIRCLE}{{\\p0}}")
        ev(L, 8, a, content, "Shape", f"{{\\an5\\pos(1000,{y})\\1c&H000000&\\fscx0\\fscy0\\t(100,280,\\fscx100\\fscy100)\\p1}}{CHECK}{{\\p0}}")
        ev(L, 7, a + 0.05, content, "Chk", f"{{\\an6\\move(1180,{y},950,{y},0,260)\\fad(120,0)}}" + rtl(text))
    # sqm counter
    c0 = m(COUNTER_AT)
    frames = 36
    for k in range(frames):
        v = round(COUNTER_TO * (1 - (1 - (k + 1) / frames) ** 3))
        a = c0 + k / 30
        b = c0 + (k + 1) / 30 if k < frames - 1 else content
        pop = "\\fscx115\\fscy115\\t(0,200,\\fscx100\\fscy100)" if k == frames - 1 else ""
        ev(L, 7, a, b, "Big", f"{{\\pos(540,930){pop}}}{v}")
    ev(L, 7, c0, content, "BigLbl", "{\\pos(540,780)\\fad(200,0)}" + rtl("דירה של כמעט"))
    ev(L, 7, c0 + 0.6, content, "BigLbl", "{\\pos(540,1080)\\fad(200,0)}" + rtl('מ"ר'))
    # white flash on hard cuts
    flashes = [m(24.0), m(28.4)]
    for t in flashes:
        ev(L, 11, t, t + 0.2, "Shape", "{\\an7\\pos(0,0)\\1c&HFFFFFF&\\1a&H30&\\fad(0,170)\\p1}m 0 0 l 1080 0 l 1080 1920 l 0 1920{\\p0}")
    # subtitles: pop-in chunks with highlighted keywords
    for a, b, text in CUES:
        s, e = m(a), m(b)
        parts = chunks(text)
        tot = sum(len(p) for p in parts)
        t = s
        for p in parts:
            d = (e - s) * len(p) / tot
            ev(L, 5, t, min(t + d, content), "Sub", "{\\q2\\fscx80\\fscy80\\t(0,110,\\fscx104\\fscy104)\\t(110,170,\\fscx100\\fscy100)}" + highlight(p))
            t += d
    # CTA end card
    ev(L, 12, content + 0.15, total, "CTA1", "{\\move(540,780,540,700,0,300)\\fad(250,0)}" + rtl("רוצים לראות איך דירה כזו\\Nהופכת להשקעה מניבה?"))
    pulse = "".join(f"\\t({s},{s+350},\\fscx108\\fscy108)\\t({s+350},{s+700},\\fscx100\\fscy100)" for s in range(800, 3800, 700))
    ev(L, 12, content + 0.6, total, "CTA2", f"{{\\pos(540,1000)\\fscx30\\fscy30\\t(0,200,\\fscx110\\fscy110)\\t(200,320,\\fscx100\\fscy100){pulse}}}" + rtl("הירשמו לוובינר"))
    ev(L, 12, content + 1.0, total, "CTA1", "{\\pos(540,1210)\\fad(250,0)}" + rtl("הקישור בביו"))
    t = content + 1.2
    while t < total - 0.01:
        ev(L, 12, t, min(t + 0.5, total), "Shape", f"{{\\an5\\move(540,1300,540,1340,0,250)\\t(250,500,\\fscy100)\\p1}}{ARROW}{{\\p0}}")
        t += 0.5
    return HEADER + "\n".join(L) + "\n", flashes, [m(x) for x, _ in CHECKLIST], c0


def render():
    content = sum(b - a for a, b in CUTS)
    total = content + CTA_DUR
    ass_text, flashes, pops, c0 = build_ass(content, total)
    ass = f"out/{NAME}.ass"
    open(ass, "w", encoding="utf-8").write(ass_text)

    cmd = ["ffmpeg", "-v", "error", "-y"]
    for a, b, _ in SUBCUTS:
        cmd += ["-ss", f"{a}", "-t", f"{b - a}", "-i", SRC]
    fc, n = [], len(SUBCUTS)
    for i, (a, b, z) in enumerate(SUBCUTS):
        d = b - a
        if z == "push":
            v = (f"[{i}:v]fps=30,scale=2160:3840,zoompan=z='1+0.09*on/{int(d*30)}':d=1:s={W}x{H}:fps=30:"
                 f"x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.3'")
        elif z == 1.0:
            v = f"[{i}:v]scale={W}:{H}:flags=lanczos,fps=30"
        else:
            zw, zh = int(W * z) // 2 * 2, int(H * z) // 2 * 2
            v = f"[{i}:v]scale={zw}:{zh}:flags=lanczos,fps=30,crop={W}:{H}:(iw-{W})/2:(ih-{H})*0.3"
        fc.append(v + f",setsar=1,format=yuv420p[v{i}]")
        fc.append(f"[{i}:a]aresample=48000,afade=t=in:d=0.04,afade=t=out:st={d-0.04}:d=0.04[a{i}]")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca]")
    fc.append(f"[cv]tpad=stop_mode=clone:stop_duration={CTA_DUR},"
              f"boxblur=20:2:enable='gte(t,{content})',"
              f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.45:t=fill:enable='gte(t,{content})',"
              f"subtitles={ass}:fontsdir=fonts[ov]")
    # voice + SFX
    fc.append(f"[ca]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad=whole_dur={total}[voice]")
    sfx = []
    for k, t in enumerate(pops):
        fc.append(f"aevalsrc='0.35*sin(2*PI*(700+900*exp(-30*t))*t)*exp(-28*t)':d=0.2:s=48000,adelay={int(t*1000)}|{int(t*1000)},aformat=channel_layouts=stereo[p{k}]")
        sfx.append(f"[p{k}]")
    for k, t in enumerate(flashes + [c0, content]):
        st = max(0, t - 0.18)
        fc.append(f"anoisesrc=d=0.4:c=pink:a=0.5:r=48000,highpass=f=600,lowpass=f=6000,afade=t=in:d=0.18,afade=t=out:st=0.18:d=0.22,volume=0.35,adelay={int(st*1000)}|{int(st*1000)},aformat=channel_layouts=stereo[w{k}]")
        sfx.append(f"[w{k}]")
    tb = content + 0.6
    fc.append(f"aevalsrc='0.25*(sin(2*PI*880*t)+sin(2*PI*1320*t)*gte(t,0.12))*exp(-6*t)':d=0.6:s=48000,adelay={int(tb*1000)}|{int(tb*1000)},aformat=channel_layouts=stereo[ding]")
    sfx.append("[ding]")
    fc.append(f"[voice]aformat=channel_layouts=stereo[vs];[vs]{''.join(sfx)}amix=inputs={len(sfx)+1}:normalize=0:duration=first,alimiter=limit=0.95[oa]")

    cmd += ["-filter_complex", ";".join(fc), "-map", "[ov]", "-map", "[oa]",
            "-c:v", "libx264", "-preset", "slow", "-b:v", "4800k", "-maxrate", "5500k", "-bufsize", "10M",
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-t", f"{total}",
            "-movflags", "+faststart", f"out/{NAME}.mp4"]
    subprocess.run(cmd, check=True)
    print(NAME, f"{total:.1f}s")


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    render()
