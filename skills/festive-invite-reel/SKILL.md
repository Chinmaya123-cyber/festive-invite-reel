---
name: festive-invite-reel
description: "Make personalised, beat-synced festive party invitation reels (9:16) in an Indian-maximalism collage style: bold swatch-poster colour pairs (hot magenta + golden yellow, lime + red, purple + mint, cotton blue + cherry), funky kinetic typography slammed to a voice/meme intro track, a kaleido sunburst drop with an illustrated card deck and playing cards flipping on every beat, then a second song for the details: a decorated auto-rickshaw ride with NEXT STOP?, marigold strings, alta footprints, hanging diyas, split-colour info slides (date, time, dress code), the venue, fireworks and a screenshot-able end card. Indie 2D illustrated stickers with paper grain, stop-motion boil, two songs cut together on a beat. Art via the Atlabs MCP (required, Seedream 5 Pro). HTML/CSS/JS + Playwright. Use for Diwali / Holi / Navratri / Eid / Christmas / New Year / birthday / house-party invites, festival greetings, Gen-Z e-invites, WhatsApp/Instagram invite reels, 'make an invite like this reel', or edits to one."
---

# Festive invite reel

A 25–35 s vertical invite in two musical halves, every cut on a beat:

| Part | Music | What happens |
| --- | --- | --- |
| **A. Hook** (0 → ~12 s) | intro track: a voice/meme/dialogue reel audio | Text slams in sync with each spoken phrase on a flat hot-magenta field ("NAMASTE" → "BEHAN AUR BHAIYO" → sparkle bursts with stickers → "AAPKO DIKHANE JA RAHE HAIN" → "YEH, YEH, YEH!" zooming through the camera). On the drop: kaleido sunburst, an illustrated card deck falls in, lands, wiggles, bursts, and one illustrated playing card flips in per beat; a joker card ("YOU'RE INVITED!") zooms through into Part B. |
| **B. Details** (~12 s → end) | main song, cut in on its first hit; loop-spliced to fit | Decorated auto drives left→right ("BHAIYA, CHALOGE?" / "HAAN JI!") and leaves "NEXT STOP?" behind it, font flipping every beat; marigold strings swing in, alta footprints step up; hanging diyas drop on the title; split-colour swatch slides for date / time / dress code; venue illustration + address card; "SEE YOU THERE! Happy …" with fireworks; end card with every detail. |

Everything is data: `content.js` (words, colours, stickers), `timing.js` (beats), `art/` (stickers + venue), `audio/mix.wav`.
`index.html` draws `seek(t)`; `scripts/render.mjs` renders it frame-exact with Playwright + ffmpeg.

```
SK=<this skill's folder>        e.g. ~/.claude/skills/festive-invite-reel
PY=<python with requirements>   ~/.claude/video-env/bin/python if it exists, else a venv with requirements.txt
```

## 0. Hard rule: connect the Atlabs MCP first

The stickers, the auto, the deck, the cards' art and the venue painting are generated with the **Atlabs MCP**
(Seedream 5 Pro). The template ships a finished Diwali sticker set, so a Diwali invite that only changes words
needs no generation, but anything new (another festival, another vehicle, a venue, guests' faces) goes through Atlabs.

1. Call `get_account`. If it answers, note the credit balance and go on.
2. If the Atlabs tools are not available, stop and give the user these steps, then wait:
   > This skill draws its illustrations with the **Atlabs MCP**. Please connect it first:
   > 1. Account: https://app.atlabs.ai (a sticker sheet costs about 2 credits; a whole new festival set about 12).
   > 2. Claude Code: `claude mcp add --transport http atlabs https://mcp.atlabs.ai/mcp`, then `/mcp` → **atlabs** → sign in.
   >    (Installed as this plugin, it is already added; just `/mcp` → atlabs → sign in.)
   >    Claude Desktop / claude.ai: Settings → Connectors → Add custom connector → `Atlabs`, `https://mcp.atlabs.ai/mcp` → Connect.
   > 3. Tell me when it's connected.
3. Before generating, say how many sheets you'll make and the credit cost (`generate_image` returns `credits_required`).

Prompts and the sheet → cutout process: `references/atlabs-art.md`. Default model **`seedream_5_pro`, 2K**.

Local tools: Node 18+, ffmpeg, Playwright (`cd $SK && npm install && npx playwright install chromium`),
Python 3.10–3.12 with `pip install -r $SK/requirements.txt` (librosa, soundfile, rembg, faster-whisper…), `uvx` for yt-dlp.

## 1. Brief (one AskUserQuestion round, then fill gaps yourself)

Ask only what you can't infer:
- **Occasion + tone**: Diwali by default; Holi, Navratri, Eid, Christmas, New Year, birthday, house party… Gen-Z adult by default
  (Hinglish one-liners under facts, e.g. "jaldi aao, late jao"). Family-friendly when asked.
- **Facts**: date (+ weekday: compute it, don't guess), time, dress code, address (exact lines), host name if wanted, RSVP.
  Never invent facts; leave a placeholder and say so.
- **Music**: two tracks: an **intro** (voice/meme/dialogue reel audio the text can sync to) and a **main song** for the details.
  The user may give files or reel links. One song also works: skip Part A's voice slams or time them to lyrics.
- **References**: reel links for motion/colour, and palette swatches. Copy their motion grammar beat for beat, not a loose vibe.

## 2. Scaffold

```bash
bash $SK/scripts/new_invite.sh ~/Downloads/<name>-invite     # copies template/, writes mix.json
node $SK/scripts/render.mjs ~/Downloads/<name>-invite --stills   # renders immediately (silent) with the Diwali set
```

## 3. References and music

1. **Download** reels the user linked (they asked, so it's allowed): `uvx yt-dlp -o "refs/%(id)s.%(ext)s" <url>`.
   Homebrew's yt-dlp may have a broken Python; `uvx` gets a fresh one. Extract audio: `ffmpeg -i refs/x.mp4 -vn -ac 2 -ar 48000 refs/intro.wav`.
2. **Study** each reel: `$PY -I $SK/scripts/study_reference.py refs/x.mp4` → contact sheet + change times. Look at the sheet.
3. **Analyse** audio: `$PY -I $SK/scripts/analyze_audio.py refs/intro.wav --words --lang hi` (voice words + the drop = biggest hit)
   and `… refs/main.wav --loops` (beats + seamless loop splice candidates).
4. **Mix**: edit `mix.json` (`intro.end` just after the intro's last beat; `main.hit` = the main song's first big hit; `cut_at` = where
   that hit lands in the film; `segments` = loop splices to lengthen the main song) → `$PY -I $SK/scripts/build_mix.py mix.json`.
   Paste `mainStart`, `beats`, `end` from `timing.json` into `timing.js`; set `spec.json` duration = end.
   Details: `references/music-sync.md`.

## 4. Words, timing, art

- `content.js` → `intro.slams`: one slam per spoken phrase, `at`/`to` = the phrase's word times (from `--words`).
  **No image over a spoken line**: the text is what syncs; stickers go in the gaps (sparkle slam).
- `timing.js` → `drop`, `deckBeats`, `cardBeats` (one per card), `joker`; `plan` = section starts as beat indices.
  **Reading time rule**: each info slide ≥ 3 beats, slides with 3+ elements (label + big word + people + note) 4 beats, end card
  ≥ 4 s. Two beats (~1 s) was too fast to read in testing. Lengthen the main song with loop splices rather than squeezing.
- `slides[]`: swatch-poster pairs from `references/style.md`; each slide = optional label, big word, sub, note, stickers.
- Art: re-use `art/stickers/*` when it fits; for a new festival or venue generate sheets (`references/atlabs-art.md`),
  cut out with `$PY -I $SK/scripts/cutout.py sheet.png art/stickers 3000 14`, rename by position, contact-sheet them on a dark
  background and look before using them.
- Other festivals: `references/customise.md` (what to swap: deck art, cards, vehicle, title, greeting, palettes).

## 5. Review → render → deliver

1. `node $SK/scripts/render.mjs <proj> --stills` → look at `out/stills/sheet.jpg`. Check: text clipped at edges, garlands or
   stickers covering words, kerning ("DIW ALI" means a missing kern pair: add it to `KERN` in index.html), end-card rows inside the panel.
2. Full render (~10 min for 30 s at 6 workers; run it in the background): `node $SK/scripts/render.mjs <proj> --workers 6`.
   Patch one section: `--from a --to b --out out/seg.mp4`, then splice frames with ffmpeg `trim=start_frame/end_frame` + concat.
3. Sample the finished mp4 (`ffmpeg -vf fps=2,scale=180:-1,tile=10x6`) and look at it.
4. Export: HQ copy + WhatsApp (`-b:v 3200k -maxrate 4000k -bufsize 8000k`, AAC 160k) into `~/Downloads` with clear names.
5. Tell the user plainly: you checked frames, not sound. Ask them to listen to the song cut and every loop splice.
   Mention once: Instagram may mute copyrighted audio; upload silent and add the track from Instagram's library if so.

## Gotchas

- Fonts load from `fonts/all.css` with paths relative to the CSS file; a `NetworkError` on `ready` means a font 404.
- Per-letter spans lose kerning; `KERN` pairs fix the worst (WA, AV, TA, LT, PA…).
- Devanagari must not be split per letter (combining marks break); `txt()` keeps it whole automatically.
- A yellow firework behind yellow type kills legibility; keep bursts away from words.
- Garlands are ~1600 px tall at 150 px wide; keep text ≤ 620 px wide between them (two lines).
- The renderer goes silent if `audio/mix.wav` is missing; that's fine for stills and drafts.
- Never commit or publish the user's music or their real address in a template.
