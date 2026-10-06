"""Web variant of the Athens apartment reels for the Paioniou 22 landing page.

Reuses REELS/cuts/cues from build.py (branch claude/dreamy-johnson-3y7tbi) but:
- drops the 4s webinar CTA end card ("link in bio" makes no sense on a web page)
- uses the static Google Fonts Heebo files (family "Heebo Black"/"Heebo ExtraBold")
- writes a 720x1280 web encode + a poster frame next to the 1080x1920 master
"""
import os, subprocess, sys
import build

build.CTA_DUR = 0.0
build.HEADER = (build.HEADER
                .replace("HeeboX 900", "Heebo Black")
                .replace("HeeboX 800", "Heebo ExtraBold"))


def build_ass(r, total):
    lines = [f"Dialogue: 1,{build.ts(0)},{build.ts(total)},Hook,,0,0,0,,{{\\fad(250,0)}}{build.rtl(r['hook'])}"]
    for a, b, text in r["cues"]:
        s, e = build.map_time(r["cuts"], a), build.map_time(r["cuts"], b)
        parts = build.chunks(text)
        L = sum(len(p) for p in parts)
        t = s
        for p in parts:
            d = (e - s) * len(p) / L
            lines.append(f"Dialogue: 0,{build.ts(t)},{build.ts(min(t + d, total))},Sub,,0,0,0,,{build.rtl(p)}")
            t += d
    return build.HEADER + "\n".join(lines) + "\n"


build.build_ass = build_ass


def web(name, out_dir):
    master = f"out/{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", master,
                    "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "27", "-profile:v", "high", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart",
                    f"{out_dir}/{name}.mp4"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1.2", "-i", master, "-frames:v", "1",
                    "-vf", "scale=720:1280", "-q:v", "4", f"{out_dir}/{name}.jpg"], check=True)


if __name__ == "__main__":
    out_dir = sys.argv[1]
    os.makedirs("out", exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    for r in build.REELS:
        build.render(r)
        web(r["name"], out_dir)
