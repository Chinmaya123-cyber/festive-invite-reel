// WHEN things happen. Seconds on the film clock.
// Fill these from scripts/analyze_audio.py + scripts/build_mix.py (build_mix writes timing.json; copy its numbers here).
// The defaults are the beat grid of the reference build (intro voice track + a 124 BPM main song with three loop splices).
window.TIMING = {
  // ---- Part A: intro track (voice slams are timed in content.js -> intro.slams)
  drop: 5.96,                                  // the intro track's drop: sunburst + deck falls in
  deckBeats: [6.484, 6.972, 7.419],            // deck wiggles on these; title + pill appear on the first two
  cardBeats: [7.79, 8.249, 8.702, 9.16, 9.619, 10.072, 10.524, 10.983], // one card per beat (one per content.cards item)
  joker: 11.436,                               // "YOU'RE INVITED" card; it zooms through the camera into Part B

  // ---- Part B: main song, starts at mainStart so its first hit lands on mainStart + beats[0]
  mainStart: 11.836,
  beats: [0.064, 0.595, 1.126, 1.614, 2.09, 2.572, 3.059, 3.547, 4.023, 4.505, 4.992, 5.48, 5.956, 6.443, 6.925, 7.413,
          7.889, 8.377, 8.858, 9.346, 9.828, 10.31, 10.786, 11.273, 11.755, 12.225, 12.706, 13.194, 13.676, 14.158, 14.634,
          15.121, 15.603, 16.073, 16.549, 17.036, 17.518, 18.0, 18.476, 18.963, 19.439, 19.886],

  // Section starts, as indices into `beats`. A section ends where the next begins.
  // ride needs 11 beats (auto in/park/out, NEXT STOP? font flips, garlands, footprints).
  // Give every info slide >= 3 beats and dense ones 4 — 2 beats (~1 s) is too fast to read.
  plan: { ride: 0, title: 11, slides: [14, 17, 20], address: 24, finale: 29, end: 33 },

  end: 32.11,                                  // film length (= mix length)
};
