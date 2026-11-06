# Customising

## Same festival, new party (no art needed)
Edit `content.js`: slides (date/time/dress code), `address.lines`, `endcard.rows`, `deck.top`, `title`, `finale`.
Address lines: 4 short lines on the card (≤ 14 chars each at 128 px Anton; the last two lines are smaller).
End-card rows: icon + label; a row with an empty icon is a continuation line (smaller, indented).

## Different festival
| Swap | Diwali | Holi | Navratri / Garba | Eid | Christmas / New Year |
| --- | --- | --- | --- | --- | --- |
| Cards (8) | diya, phuljhadi, mithai, teen patti, DJ, naach, bhangra, patakhe | gulaal, pichkari, thandai, gujiya, dhol, balloons… | dandiya, chaniya choli, garba pot, dhol… | crescent, lantern, sheer khurma, mehendi, attar… | tree, gifts, cake, star, disco ball… |
| Title / greeting | DIWALI PARTY · Happy DIWALI | HOLI PARTY · Bura na mano | GARBA NIGHT | EID MILAN · Eid Mubarak | X-MAS PARTY |
| Vehicle | auto-rickshaw | auto with colour splashes | auto with dandiya | horse cart / car | auto with fairy lights |
| Decor | marigolds, hanging diyas, alta feet | colour clouds, water balloons | torans, mirror-work | lanterns, arches | baubles, tinsel |

Generate a new set with `references/atlabs-art.md` prompts (swap the objects), keep the file names the template uses
(`diya`, `sparkler`, `garland1..3`, `hangdiya`, `footL/footR`, `firework`, `auto`, `deck`, …) or update the names in
`content.js` / `index.html`.

## Different intro audio
Rewrite `intro.slams` to its words. Slam types: `lines` (1–3 lines, `lineAt` per line), `sparkle` (star bursts + stickers on
`steps`), `jitter` (size steps every 1/3 s), `zoom` (last slam flies through the camera into the drop), `stars` (corner twinkles).

## Different length
Change `TIMING.plan`; sections end where the next starts. Keep the reading-time rule (slides ≥ 3 beats, dense ones 4).
More or fewer info slides: add/remove `content.slides` entries and the matching `plan.slides` indices.

## Horizontal / square
The engine is 1080×1920. For 1:1 or 16:9, change `spec.json` and `#stage`, then re-place elements (y positions are absolute).
