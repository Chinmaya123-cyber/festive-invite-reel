#!/usr/bin/env python3
"""Build the two-song soundtrack and the main song's beat grid.

    python -I build_mix.py mix.json

mix.json:
{
  "intro": {"file": "refs/intro.wav", "end": 11.905, "fade": 0.07},     # intro track, cut at `end` (just after its last beat)
  "main":  {"file": "refs/main.wav",  "hit": 0.064,                        # the main song's first hit (seconds into the file)
            "segments": [[0, 3.059], [1.126, 10.304], [6.444, 10.304], [8.377, null]]},  # optional loop splices
  "cut_at": 11.90,                                                          # film time where the main song's hit lands
  "out": "audio/mix.wav",
  "timing": "timing.json"
}

`segments` plays each [start, end) of the main song in order (null = to the end) with 12 ms crossfades.
Get splice pairs from `analyze_audio.py --loops`: for a candidate, end one segment at `at` and start the next at `jump_back_to`.
Writes the mix and timing.json with mainStart, beats (the main song's beat grid on the spliced clock) and end —
paste those into template/timing.js.
"""
import json, sys
import numpy as np
import soundfile as sf
import librosa

cfg = json.load(open(sys.argv[1]))
sr = 48000
intro, _ = librosa.load(cfg["intro"]["file"], sr=sr, mono=False)
main, _ = librosa.load(cfg["main"]["file"], sr=sr, mono=False)
if intro.ndim == 1: intro = np.stack([intro, intro])
if main.ndim == 1: main = np.stack([main, main])
md = main.shape[1] / sr

# beat grid of the main song (on its own clock)
y, _ = librosa.load(cfg["main"]["file"], sr=22050, mono=True)
oe = librosa.onset.onset_strength(y=y, sr=22050, hop_length=128)
_, beats = librosa.beat.beat_track(onset_envelope=oe, sr=22050, hop_length=128, units="time", tightness=300)
beats = [float(b) for b in beats]

segs = cfg["main"].get("segments") or [[0, None]]
xf = int(0.012 * sr)
B, JB, off = None, [], 0.0
for a, b in segs:
    b = md if b is None else b
    x = main[:, int(a * sr):int(b * sr)]
    JB += [round(off + (t - a), 3) for t in beats if a - 1e-3 <= t < b - 1e-3]
    if B is None:
        B = x
    else:
        r = np.linspace(0, 1, xf)
        B = np.concatenate([B[:, :-xf], B[:, -xf:] * (1 - r) + x[:, :xf] * r, x[:, xf:]], 1)
        off -= xf / sr
    off += b - a

hit = cfg["main"].get("hit", beats[0] if beats else 0)
T0 = cfg["cut_at"] - hit                      # main song starts here so its hit lands on cut_at
iend = cfg["intro"].get("end", cfg["cut_at"])
total = T0 + B.shape[1] / sr
out = np.zeros((2, int(total * sr) + 1), np.float32)
ia = intro[:, :int(iend * sr)].copy()
n = int(cfg["intro"].get("fade", .07) * sr)
ia[:, -n:] *= np.linspace(1, 0, n)
out[:, :ia.shape[1]] += ia
s = int(T0 * sr)
out[:, s:s + B.shape[1]] += B[:, :out.shape[1] - s]
peak = float(np.abs(out).max())
if peak > .98: out *= .98 / peak
sf.write(cfg.get("out", "audio/mix.wav"), out.T, sr)
res = {"mainStart": round(T0, 3), "beats": JB, "end": round(total - .02, 2), "beat_count": len(JB),
       "note": "paste mainStart, beats and end into timing.js; set spec.json duration = end"}
json.dump(res, open(cfg.get("timing", "timing.json"), "w"), indent=1)
print(json.dumps(res))
