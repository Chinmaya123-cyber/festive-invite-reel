# Art with the Atlabs MCP

All illustration comes from the Atlabs MCP (`https://mcp.atlabs.ai/mcp`). Default model: **`seedream_5_pro`, resolution `2K`**
(about 2 credits per image). It gives the indie gouache look: flat cut-paper shapes, risograph grain, soft inner shading.

## Process

1. `get_account` → balance. Tell the user the plan: N sheets × ~2 credits.
2. `generate_image` for every sheet **in one batch** (they run in parallel), then `get_result` for each request_id.
   If a `get_result` call is interrupted, just call it again: the job keeps running server-side.
3. Download each output: `curl -sL -o art/raw/<name>.png "<url>"`.
4. Cut out: `$PY -I $SK/scripts/cutout.py art/raw/<sheet>.png art/stickers 3000 14`
   (rembg isnet + a white-key for sparks; splits the sheet into one PNG per object, named `<sheet>_NN.png` in reading order,
   with their positions printed). Rename by position. White objects (kaju katli, kurtas) can get holes: fill with
   `scipy.ndimage.binary_fill_holes` on the alpha (see the snippet below).
5. Contact-sheet the cutouts on the dark maroon background and **look** before using them.
6. Downscale: stickers ≤ 900 px, garlands 150–300 px wide, the auto ≤ 1100 px.

```python
from PIL import Image; import numpy as np; from scipy import ndimage
a = np.array(Image.open(p)); f = ndimage.binary_fill_holes(a[..., 3] > 100)
a[..., 3] = np.maximum(a[..., 3], f * 255).astype(np.uint8); Image.fromarray(a).save(p)
```

## Shared style line (append to every prompt)

> Style: contemporary Indian indie 2D illustration, bold flat colour shapes like gouache cut-paper, subtle risograph paper-grain
> texture inside the shapes, soft painted inner shading and a gentle hand-drawn shadow under each object for depth, confident
> thin deep-plum outline. Indian maximalism, Gen-Z cool, playful slightly chunky proportions. Palette: hot magenta #FF006E,
> golden yellow #FFD60A, lime #D3F00A, vibrant red #F80E0B, electric purple #8338EC, mint green #88FF5F, sky blue #94DEFF,
> cherry pink #FF277F, marigold orange, teal.

## Sheet prompts (the ones the shipped Diwali set came from)

**Icons, 1:1** — "A sticker sheet of 9 separate Diwali objects arranged in a clean 3x3 grid, each object fully isolated on a plain
flat pure white background with wide empty white space between them, nothing touching or overlapping, no text, no letters.
Objects: 1) a clay diya with a tall glowing flame; 2) a lit phuljhadi sparkler; 3) a spinning chakri; 4) a rocket firework;
5) an anar flowerpot firework; 6) a brass plate of kaju katli; 7) a hanging akash kandil star lantern; 8) motichoor laddoos on a
banana leaf; 9) a gift box in block-print paper with a marigold. + style line"

**People and party, 1:1** — same frame; elements: namaste hands holding a marigold; a Gen-Z woman in a hot-pink lehenga with
oversized sunglasses dancing; a Gen-Z man in a mustard kurta + Nehru jacket with headphones in a bhangra pose; a hand fanning
three playing cards; a retro boombox draped with marigolds; a hand with alta and mehendi holding a lotus; hands with stacks of
glass bangles; a brass bell; an open box of mithai.

**Vehicle, 16:9** — "One Indian auto-rickshaw seen exactly from the side, facing RIGHT, centred and fully inside the frame,
isolated on plain white, no ground, no text, no numbers. Decked out for a Diwali party: magenta + yellow truck-art body,
teal canopy piled with marigolds and mango leaves, marigold garland along the canopy edge, fairy lights, a diya on the dashboard,
two Gen-Z friends in festive ethnic wear waving in the back, a driver in a white kurta." It must face right (it drives left→right).

**Decor, 9:16** — three long vertical marigold strings (genda phool ladi) top to bottom with a red rose at the end, plus
separately: a brass hanging diya on a chain, a pair of alta footprints with white dots, a round rangoli, a firework burst.

**Venue, 9:16 full-bleed** — the party place at night (e.g. a tower with a glowing penthouse terrace party, fairy lights,
lanterns, diyas, dancing silhouettes, fireworks) on a deep raspberry sky; **lower half calm and simple** for the address card;
no text or signs.

**Deck box, 1:1** — a closed playing-card box standing upright, three-quarter view, royal blue with a magenta/yellow truck-art
frame, a glowing diya in a lotus, paisley borders, **a plain empty magenta banner across the top of the front face** (the title
is overlaid in code there). If you change the box, re-measure the banner and adjust the overlay box in index.html (`deck` block).

## Rules

- Never generate text inside images; all words are typeset in code.
- One fixed outfit/description per character across sheets, so people look consistent.
- Real people: only from photos the user says they may use, and keep them illustrated.
