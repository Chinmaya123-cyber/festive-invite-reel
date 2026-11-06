# festive-invite-reel

**A Claude skill that makes personalised, beat-synced festive party invite reels in an Indian-maximalism collage style.**
Bold swatch-poster colours, funky kinetic type, indie 2D illustrated stickers with paper grain and stop-motion boil, and two
songs cut together on a beat. Built for Diwali, and easy to switch to Holi, Navratri, Eid, Christmas, New Year, birthdays or any house party.

<p>
  <img src="examples/01-diwali-house-party/preview-hook.gif" width="270" alt="Hook: kinetic type, sunburst drop, cards flipping on the beat">
  &nbsp;
  <img src="examples/01-diwali-house-party/preview-details.gif" width="270" alt="Details: title, split-colour date, time and dress code slides">
</p>

> **Requires the Atlabs MCP** for the illustrations (stickers, auto-rickshaw, card deck, venue painting). Setup below.

## What you get

A 25–35 s vertical (1080×1920) invite in two musical halves:

1. **The hook** runs on a voice or meme reel audio. Text slams land on each spoken phrase ("NAMASTE… BEHAN AUR BHAIYO… AAPKO DIKHANE JA RAHE HAIN… YEH, YEH, YEH!").
   On the drop, a kaleido sunburst spins up, an illustrated card deck falls in, and one illustrated playing card flips per beat.
   Finally a "YOU'RE INVITED!" joker card zooms through the camera.
2. **The details** run on the main song, cut in on its first hit:
   - A decorated auto-rickshaw drives across and leaves "NEXT STOP?" behind it.
   - Marigold strings and alta footprints come in, then hanging diyas drop over the title.
   - Split-colour slides show the date, time and dress code, followed by the venue illustration and address card.
   - "See you there!" plays with fireworks, then an end card holds every detail so guests can screenshot it.

Everything personal sits in two data files: `content.js` holds the words, colours and stickers, and `timing.js` holds the beats.
A full contact sheet is in [`examples/01-diwali-house-party`](examples/01-diwali-house-party/contact-sheet.jpg), along with a silent demo.

## Install

**Claude Code (plugin, includes the Atlabs MCP config):**
```bash
claude plugin marketplace add Chinmaya123-cyber/festive-invite-reel
claude plugin install festive-invite-reel@festive-invite-reel
```
Then run `/mcp`, pick **atlabs** and sign in with your Atlabs account.

**Claude Code (skill only):**
```bash
git clone https://github.com/Chinmaya123-cyber/festive-invite-reel
cp -R festive-invite-reel/skills/festive-invite-reel ~/.claude/skills/
claude mcp add --transport http atlabs https://mcp.atlabs.ai/mcp     # then /mcp → atlabs → sign in
```

**Claude Desktop / claude.ai:** upload the `.skill` file from the [latest release](../../releases), then go to
Settings → Connectors → Add custom connector → name `Atlabs`, URL `https://mcp.atlabs.ai/mcp` → Connect.

**Atlabs account:** https://app.atlabs.ai. Art uses Seedream 5 Pro at about 2 credits per sticker sheet. The shipped Diwali
set costs nothing to reuse, and a whole new festival set is about 12 credits.

**Local tools:** Node 18+, ffmpeg, Python 3.10–3.12. Run `cd skills/festive-invite-reel && npm install && npx playwright install chromium`
and `pip install -r requirements.txt`.

## Use it

Ask Claude something like:

> Make a Diwali party invite reel for Saturday 7 Nov, 8 PM onwards, dress code ethnic, at Flat 12, Sunrise Towers, MG Road.
> Use the audio from this reel for the intro and this song for the ending: `<links or files>`. Colours: hot magenta + golden yellow.

> Same style but for a Holi party, family-friendly, 25 seconds.

> Make an invite like this reel `<link>`, with my details.

Claude connects Atlabs, studies any reference reels, analyses both songs (beats, the drop, spoken words, seamless loop points),
builds the two-song mix, generates and cuts out any new illustrations, fills in `content.js` and `timing.js`, checks stills,
renders the film, and exports an HQ copy plus a WhatsApp-sized copy.

## Repo layout

```
skills/festive-invite-reel/
  SKILL.md                    the workflow Claude follows
  template/                   index.html (engine) · content.js · timing.js · spec.json · art/ · fonts/ (OFL)
  scripts/
    new_invite.sh             scaffold a project
    study_reference.py        contact sheet + visual change times of a reference reel
    analyze_audio.py          tempo, beats, drop, spoken words, seamless loop splice candidates
    build_mix.py              intro track + main song (with loop splices) → mix.wav + beat grid
    cutout.py                 sticker sheet → transparent PNGs
    render.mjs                deterministic Playwright renderer (stills, draft, full, segments)
  references/                 atlabs-art.md · music-sync.md · style.md · customise.md
examples/01-diwali-house-party/   contact sheet, preview GIFs, silent demo, its content.js + timing.js
```

## Notes

- **Music:** no audio ships with this repo. Use songs you have the right to use. A famous song plays fine on WhatsApp, but Instagram
  may mute it. If that happens, upload the video silent and add the track from Instagram's music library.
- **Placeholders:** the example details (Flat 12, Sunrise Towers…) are placeholders, so replace them with yours.
- **Checking by ear:** Claude measures beats but can't hear. Listen to the song cut and the loop splices before you share.
- **Licences:** fonts are SIL OFL (Google Fonts). The illustrations were generated with Atlabs (Seedream 5 Pro) for this template.
  Code is MIT.
