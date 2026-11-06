#!/usr/bin/env python3
"""Measure a song or reel soundtrack for beat-synced editing.

    python -I analyze_audio.py intro.wav [--words] [--loops]

Prints JSON: duration, tempo, beat times (tight beat tracker), strong onsets (the big hits / drops),
loudness per 0.5 s, optional word timings (faster-whisper, for voice/dialogue reels) and optional
loop-splice candidates (pairs of beats 4 or 8 apart whose audio matches, so a bar or phrase can be
repeated seamlessly to make the song longer).
"""
import argparse, json, sys
import numpy as np
import librosa


def analyze(path, words=False, loops=False, lang=None):
    y, sr = librosa.load(path, sr=22050, mono=True)
    dur = len(y) / sr
    hop = 128
    oe = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
    tempo, beats = librosa.beat.beat_track(onset_envelope=oe, sr=sr, hop_length=hop, units="time", tightness=300)
    on = librosa.onset.onset_detect(onset_envelope=oe, sr=sr, hop_length=hop, units="frames")
    st = oe[on]
    thr = np.percentile(st, 80) if len(st) else 0
    strong = [round(float(librosa.frames_to_time(f, sr=sr, hop_length=hop)), 3) for f, s in zip(on, st) if s >= thr]
    biggest = sorted(zip(st, on), reverse=True)[:5]
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    tt = librosa.times_like(rms, sr=sr, hop_length=hop)
    loud = [round(float(np.nanmean(rms[(tt >= a) & (tt < a + .5)]) if ((tt >= a) & (tt < a + .5)).any() else 0), 3) for a in np.arange(0, dur, .5)]
    out = {
        "file": path, "duration": round(dur, 3),
        "tempo": round(float(np.atleast_1d(tempo)[0]), 2),
        "beat_period": round(float(np.median(np.diff(beats))), 4) if len(beats) > 1 else None,
        "beats": [round(float(b), 3) for b in beats],
        "strong_onsets": strong,
        "biggest_hits": [round(float(librosa.frames_to_time(f, sr=sr, hop_length=hop)), 3) for _, f in biggest],
        "loudness_per_half_second": loud,
    }
    if loops and len(beats) > 9:
        fps = sr / hop
        S = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop, n_mels=64))
        w = int(.25 * fps)
        cands = []
        for i in range(len(beats)):
            for n in (4, 8):
                if i + n >= len(beats):
                    continue
                a, b = beats[i], beats[i + n]
                fa, fb = int(a * fps), int(b * fps)
                if fa - w < 0 or fb + w >= S.shape[1]:
                    continue
                d = float(np.mean(np.abs(S[:, fa - w:fa + w] - S[:, fb - w:fb + w])))
                cands.append({"diff_db": round(d, 2), "from_beat": i, "beats": n, "jump_back_to": round(float(a), 3), "at": round(float(b), 3),
                              "adds_seconds": round(float(b - a), 3)})
        cands.sort(key=lambda c: c["diff_db"])
        out["loop_candidates"] = cands[:12]
        out["loop_help"] = ("Play the song up to `at`, then continue from `jump_back_to`: that repeats `beats` beats. "
                            "Lower diff_db = more seamless (under ~4 is usually clean). Prefer spreading repeats over "
                            "several candidates instead of repeating one bar many times.")
    if words:
        try:
            from faster_whisper import WhisperModel
            y16 = librosa.resample(y, orig_sr=sr, target_sr=16000)
            m = WhisperModel("small", compute_type="int8")
            segs, _ = m.transcribe(y16, language=lang, word_timestamps=True)  # numpy array: avoids the PyAV path bug
            out["words"] = [{"w": w.word.strip(), "t": round(float(w.start), 2), "end": round(float(w.end), 2)} for s in segs for w in s.words]
        except Exception as e:  # optional dependency
            out["words_error"] = str(e)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--words", action="store_true", help="transcribe dialogue/lyrics with word timings (faster-whisper)")
    ap.add_argument("--loops", action="store_true", help="rank seamless loop splice points")
    ap.add_argument("--lang", default=None, help="whisper language hint, e.g. hi or en")
    a = ap.parse_args()
    res = [analyze(f, a.words, a.loops, a.lang) for f in a.files]
    json.dump(res if len(res) > 1 else res[0], sys.stdout, indent=1, ensure_ascii=False)
    print()
