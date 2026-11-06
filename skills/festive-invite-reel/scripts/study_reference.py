#!/usr/bin/env python3
"""Study a reference reel: contact sheet + the moments the picture changes (cuts, text swaps, card flips).

    python -I study_reference.py refs/reel.mp4 [--fps 3] [--out refs/sheets]

Writes <out>/<name>_sheet.jpg (frames every 1/fps s, tiled) and prints JSON with duration, resolution,
fps and `changes`: times where the frame changes a lot (strength > 4). Line these up with the audio's
beats/words from analyze_audio.py to copy the reference's motion grammar beat for beat.
Download reels with:  uvx yt-dlp -o "refs/%(id)s.%(ext)s" <url>   (only reels the user asked you to use)
"""
import argparse, json, os, subprocess
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--fps", type=float, default=3)
ap.add_argument("--out", default=None)
a = ap.parse_args()
out = a.out or os.path.join(os.path.dirname(a.video) or ".", "sheets")
os.makedirs(out, exist_ok=True)
name = os.path.splitext(os.path.basename(a.video))[0]

probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height,r_frame_rate,codec_type",
                                   "-of", "json", a.video], capture_output=True, text=True).stdout)
v = next(s for s in probe["streams"] if s["codec_type"] == "video")
num, den = map(int, v["r_frame_rate"].split("/"))
fps = num / den
dur = float(probe["format"]["duration"])
n = int(dur * a.fps) + 1
cols = 10
rows = (n + cols - 1) // cols
sheet = os.path.join(out, f"{name}_sheet.jpg")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-vf", f"fps={a.fps},scale=150:-1,tile={cols}x{rows}", "-frames:v", "1", sheet], check=True)

W, H = 90, 160
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(float)
d = np.abs(np.diff(fr, axis=0)).mean((1, 2))
changes, last = [], -1
for i, x in enumerate(d):
    t = (i + 1) / fps
    if x > 4 and t - last > .1:
        changes.append({"t": round(t, 2), "strength": round(float(x), 1)}); last = t
print(json.dumps({"video": a.video, "duration": round(dur, 2), "size": [v["width"], v["height"]], "fps": round(fps, 2),
                  "sheet": sheet, "sheet_every_s": round(1 / a.fps, 3), "changes": changes}, indent=1))
