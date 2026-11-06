// WHAT the guest reads. Change words here; timings live in timing.js.
// Fonts: rozha (desi serif), anton (tall condensed), shrikhand (funky italic), bowlby (chunky), playfair (italic 900),
//        playfairLight (italic 500), marcellus (spaced serif), bricolage (condensed 800), yatra (Devanagari display).
// Stickers are file names in art/stickers (without .png). Colours are the swatch-poster pairs.
window.CONTENT = {
  // Part A — text slams synced to the intro track's VOICE (one slam per spoken phrase; no image over a spoken line)
  intro: {
    bg: '#FF006E', ink: '#FFD60A',
    slams: [
      { at: 0.00, to: 0.46, lines: ['NAMASTE'], font: 'rozha', size: 190 },
      { at: 0.46, to: 1.67, lines: ['BEHAN', 'AUR BHAIYO'], lineAt: [0.46, 0.80], font: 'anton', size: [250, 200], stepAt: 1.25 },
      { at: 1.67, to: 3.00, sparkle: true, steps: [1.67, 2.0, 2.33, 2.67], stickers: ['diya', 'sparkler', 'chakri', 'anar'] },
      { at: 3.00, to: 4.75, lines: ['AAPKO', 'DIKHANE', 'JA RAHE HAIN'], lineAt: [3.0, 3.22, 3.44], font: 'rozha', size: [190, 180, 150], jitter: true, stars: true },
      { at: 4.75, to: 5.25, lines: ['YEH'], font: 'rozha', size: 330 },
      { at: 5.25, to: 5.55, lines: ['YEH'], font: 'anton', size: 520 },
      { at: 5.55, to: 'drop', lines: ['YEH!'], font: 'shrikhand', size: 440, zoom: true },
    ],
  },
  deck: { title: 'DIWALI PARTY', top: "DIWALI '26", pill: 'LIMITED EDITION' },
  cards: [
    { art: 'diya',     word: 'DIYE',       pip: 'A',  bg: '#D3F00A', ink: '#F80E0B' },
    { art: 'sparkler', word: 'PHULJHADI',  pip: 'K',  bg: '#8338EC', ink: '#88FF5F' },
    { art: 'laddoo',   word: 'MITHAI',     pip: 'Q',  bg: '#94DEFF', ink: '#FF277F' },
    { art: 'cards',    word: 'TEEN PATTI', pip: 'J',  bg: '#C8154B', ink: '#FFF8B6' },
    { art: 'boombox',  word: 'DJ NIGHT',   pip: '10', bg: '#FFD60A', ink: '#FF006E' },
    { art: 'girl',     word: 'NAACH',      pip: '9',  bg: '#F80E0B', ink: '#D3F00A' },
    { art: 'boy',      word: 'BHANGRA',    pip: '8',  bg: '#88FF5F', ink: '#8338EC' },
    { art: 'rocket',   word: 'PATAKHE',    pip: '7',  bg: '#FF006E', ink: '#FFD60A' },
  ],
  joker: { lines: ["YOU'RE", 'INVITED!'], art: 'gift', bg: '#FF277F', ink: '#94DEFF' },

  // Part B — main song
  ride: { call: 'BHAIYA, CHALOGE?', reply: 'HAAN JI!', nextStop: ['NEXT', 'STOP?'] },
  title: { a: 'DIWALI', b: 'PARTY', hi: 'दिवाली पार्टी' },
  // split-colour info slides (one per TIMING.plan.slides entry). Beat offsets (`at`) are relative to the slide's first beat.
  slides: [
    { top: '#FF006E', bot: '#FFD60A', fromLeft: true,
      label: { text: 'SATURDAY', font: 'anton', size: 96, color: '#FFD60A', spacing: '.2em' },
      big: { text: '7TH', font: 'anton', size: 560, color: '#FFD60A', slam: true },
      sub: { text: 'NOVEMBER', font: 'bowlby', size: 150, color: '#FF006E' },
      note: { text: 'save the date!', color: '#FF006E', at: 1 },
      stickers: [{ art: 'diya', x: 900, y: 940, w: 250, r: 8, at: 0.2 }] },
    { top: '#D3F00A', bot: '#F80E0B', fromLeft: false,
      big: { text: '6:30 PM', font: 'anton', size: 290, color: '#F80E0B', y: 560 },
      sub: { text: 'ONWARDS', font: 'bowlby', size: 150, color: '#D3F00A' },
      note: { text: 'jaldi aao, late jao', color: '#D3F00A', at: 1 },
      stickers: [{ art: 'sparkler', x: 170, y: 900, w: 260, r: -25, at: 0.2 }] },
    { top: '#88FF5F', bot: '#8338EC', fromLeft: true,
      label: { text: 'dress code', font: 'playfairLight', size: 110, color: '#8338EC' },
      big: { text: 'ETHNIC', font: 'anton', size: 330, color: '#8338EC', stretch: 1.55 },
      note: { text: 'full desi. no excuses.', color: '#88FF5F', at: 2, y: 1050 },
      stickers: [{ art: 'girl', x: 300, y: 1450, w: 360, r: -4, at: 1 }, { art: 'boy', x: 790, y: 1450, w: 360, r: 4, at: 1.15 }] },
  ],
  address: { ask: 'kahaan?', lines: ['FLAT 12', 'SUNRISE TOWERS', 'MG ROAD', 'YOUR CITY'], scene: 'art/scenes/venue.jpg' },
  finale: { a: 'SEE YOU', b: 'THERE!', c: 'Happy', d: 'DIWALI' },
  endcard: {
    title: ['DIWALI', 'PARTY'],
    rows: [
      ['diya', 'SAT, 7TH NOVEMBER'],
      ['sparkler', '6:30 PM ONWARDS'],
      ['girl', 'DRESS CODE: ETHNIC'],
      ['lantern', 'FLAT 12, SUNRISE TOWERS'],
      ['', 'MG ROAD, YOUR CITY'],
    ],
    sign: 'see you there!',
  },
};
