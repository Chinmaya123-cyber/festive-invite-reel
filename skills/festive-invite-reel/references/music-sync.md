# Music sync: two songs, one clock

## The shape
- **Intro track** (~12 s): a voice / meme / dialogue reel audio. Each spoken phrase gets one text slam. Its biggest
  onset is the **drop** (sunburst + deck). The beats after the drop carry the deck wiggles and one card per beat.
- **Main song**: enters on its **first big hit**, placed exactly where the intro ends (the joker card zooms through on it).
  Its beats drive the whole Part B.

## Steps
1. `analyze_audio.py refs/intro.wav --words --lang hi`
   - `words` → slam times. A slam starts on its first word, ends when the next phrase starts.
   - `biggest_hits[0]` → `TIMING.drop` (lead it by ~1 frame, e.g. 5.96 for a hit at 5.98).
   - `beats` after the drop → `deckBeats` (3) and `cardBeats` (one per card); the last beat before the intro's tail → `joker`.
   - the intro's final beat → `cut_at` in mix.json (the main hit lands there).
2. `analyze_audio.py refs/main.wav --loops` → `beats[0]`/`biggest_hits` gives `main.hit`; `loop_candidates` give splices.
3. Decide the length: count beats Part B needs (ride 11, title 3, each slide 3–4, address 4–5, finale 4, end card ≥ 8 for ~4 s).
   If the main clip is short, add splices: each candidate repeats 4 or 8 beats. Prefer **three different splice points**
   over one bar repeated many times (it starts to sound like a skipping record).
4. `build_mix.py mix.json` → `audio/mix.wav` + `timing.json`. Paste `mainStart`, `beats`, `end` into `timing.js`, set the plan.

## Splices
`segments: [[0, 3.059], [1.126, 10.304], [6.444, 10.304], [8.377, null]]` means: play 0–3.059, jump back to 1.126 (repeats
4 beats), play to 10.304, jump back to 6.444 (repeats 8 beats), play to 10.304, jump back to 8.377 (repeats 4), play to the end.
Each jump must go from a candidate's `at` to its `jump_back_to`. Crossfade is 12 ms.

## Honesty
You can measure beats and spectra but you cannot hear. Say which splices you used and ask the user to listen to them and to the
song cut before they share the video.
