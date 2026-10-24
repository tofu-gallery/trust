# The Evolution of Trust on Tofu

The Evolution of Trust by Nicky Case is an interactive explanation of cooperation and game theory. Players make choices in repeated games, compare strategies in tournaments, and experiment with a sandbox. This fork preserves the upstream name, artwork, favicon, story, and credits.

## Running a copy

- Tofu framework preset: `static`.
- Site root / output directory: repository root (`.`); entry page: `index.html`.
- Install command: none. There is no package manifest or dependency installation.
- Build command: none. The repository already contains the finished site and its libraries.
- Database: none.
- Environment variables / secrets / external accounts: none.
- Serve over HTTP or HTTPS. Opening `index.html` as a `file:` URL will not load the text and sprite manifests correctly.
- For a local check: `python3 -I -m http.server 62231 --bind 127.0.0.1 --directory /private/tmp/gallery-batch2/trust`, then `curl --fail --silent --show-error --output /dev/null --write-out '%{http_code}\n' http://127.0.0.1:62231/`.

All application scripts, styles, images, fonts, music, and sound effects load from the same site. There are no analytics scripts, advertising integrations, API keys, or Tofu-owned external services. The original sharing buttons, credits, reading links, and fan-translation links remain; opening them deliberately leaves the copy. Sharing metadata and buttons still refer to the original upstream site. The bundled game is English; translations are separate external sites.

## Adaptations and their reasons

- Added this file to make the static hosting contract and provenance explicit.
- Replaced the 15 sound-effect MP3s (all files in `assets/sounds/` except `bg_music.mp3`) with original synthesized CC0 cues. The upstream README credits both a CC BY-NC sound collection and a CC Sampling+ recording without providing a complete file-to-source map. Replacing the whole effects set removes that ambiguity for copies offered through Tofu. No original recordings are sampled; cue filenames and game code stay unchanged.
- Removed `tools/generate-tofu-sounds.py`, the Python 3 script that produced those cues, because Tofu's Free static hosting publishes only finished-site file types and refuses a site that contains a `.py` file. The game never loaded it. How the cues were made is written down in the next section instead, and the script itself stays in the history at the `pin/2026-10-23` tag.
- Kept the CC0 music by Komiku, all original attribution, the upstream README, and LICENSE unchanged.
- **Tofu note, 2026-10-24:** added `css/FONT-LICENSE.txt` next to the font file. It quotes the terms the Futura Handwritten font is offered under, with the address they were read from and the date; see *License and redistribution notes* below. The font file and every file that uses it are unchanged.

## How the replacement sound effects were made

The 15 effects in `assets/sounds/` (everything except `bg_music.mp3`) are synthesized from the formulas below; no recording is sampled. They came out of a short Python 3 script that is no longer in the tree (see above), and this is its recipe in full.

- Audio is mono, 44,100 Hz, 16-bit, `round(44100 · length)` samples per cue. `t` is seconds since the cue starts, `p` is `t` divided by the cue's length, and `phase` is `t` modulo the pulse length for the cues that have pulses.
- `tone(t, f)` is `sin(2π·f·t)`. `bell(t, f)` is `(tone(t, f) + 0.3·tone(t, 2.7·f)) · e^(−15·t)`.
- Each sample is multiplied by a fade, `min(1, t / 0.005, (length − t) / 0.02)` (5 ms in, 20 ms out), then by 0.45, clipped to the range −1 to 1, multiplied by 32767 and rounded.
- `noise` is `random.Random(seed).uniform(-1, 1)`, drawn once per sample from a generator created fresh for each cue. The seed is the cue's number in the table, counting from 0.
- Each cue is written as a WAV in memory and piped through `ffmpeg -f wav -i pipe:0 -map_metadata -1 -c:a libmp3lame -b:a 96k -write_xing 0 <name>.mp3`. The committed files came from ffmpeg 9.0.2.

| # | File | Length | Value before the fade, gain and clipping |
|---|------|--------|------------------------------------------|
| 0 | `button1.mp3` | 0.20 s | `bell(t, 520)` |
| 1 | `button2.mp3` | 0.20 s | `bell(t, 660)` |
| 2 | `button3.mp3` | 0.20 s | `bell(t, 820)` |
| 3 | `coin_insert.mp3` | 0.28 s | `bell(t, 1100)`, plus `0.35 · bell(t − 0.07, 1650)` once t > 0.07 s |
| 4 | `coin_get.mp3` | 0.45 s | `bell(t, 880)` while t < 0.12 s, then `bell(t − 0.12, 1320)` |
| 5 | `machine_start.mp3` | 0.80 s | `bell(phase, 360 + 480·p) · (1 − p)`, pulse length 0.09 s |
| 6 | `drumroll.mp3` | 1.60 s | `noise · e^(−100·phase) · (0.2 + 0.8·p)`, pulse length 0.045 s |
| 7 | `evil_laugh.mp3` | 0.80 s | `tone(t, 180) · e^(−18·phase) · (0.6 + 0.4·tone(t, 7))`, pulse length 0.2 s |
| 8 | `scratch_in.mp3` | 0.30 s | `noise · sin(π·p)² · (0.4 + 0.6·p)` |
| 9 | `scratch_out.mp3` | 0.30 s | `noise · sin(π·p)² · (0.4 + 0.6·(1 − p))` |
| 10 | `whoosh.mp3` | 0.30 s | `noise · sin(π·p)² · (0.4 + 0.6·p)` |
| 11 | `squeak.mp3` | 0.18 s | `sin(2π·(900·t + 700·t²)) · sin(π·p)` |
| 12 | `bonk.mp3` | 0.20 s | `tone(t, 150) · e^(−20·t)` |
| 13 | `thump.mp3` | 0.25 s | `tone(t, 75) · e^(−20·t)` |
| 14 | `fart.mp3` | 0.45 s | `(tone(t, 65) + 0.3·noise) · e^(−5·t)` |

## Source and branches

- Upstream: https://github.com/ncase/trust
- Upstream default branch: `gh-pages`.
- Base commit: `6ec45d73befdb922bd40654dd1c1c903a953562f`.
- Gallery fork: https://github.com/tofu-gallery/trust
- `main` mirrors that upstream commit without adaptation commits; `gh-pages` is the fork's original upstream branch.
- `tofu` contains the adaptations. The newest pin, `pin/2026-10-24`, adds the font's terms. The earlier pins are unchanged: `pin/2026-10-23.1` is the commit before it, and `pin/2026-10-23` still contains the sound generator script.
- This preparation does not deploy the application or turn on GitHub Pages.

## Local verification

Verified on 2026-10-23 without deploying: the Python HTTP server served `/`, `/words.html`, `/notes/`, and `/peeps/` with HTTP 200. Every JavaScript file passed `node --check`, all 41 runtime asset paths existed, and ffmpeg decoded all 16 audio files. A real browser loaded all 16 sounds, entered the game, and selected CHEAT; the explanation advanced correctly. The browser requested no external resources. Its only captured console error came from an installed wallet extension (`chrome-extension://.../inpage.js`), not application code. This is a smoke check, not completion of the full 30-minute game or a mobile audit.

Checked again on 2026-10-23, without deploying, after `tools/generate-tofu-sounds.py` was removed. Tofu's file-type check for Free static hosting refuses no file and treats the repository as a finished static site. Served over HTTP from a copy without the folders an import drops, the game loaded in a real browser: the server answered every request with 200 or 304 and none went to another site, all 16 audio files reached the loaded state, and all 15 effects started playing. Pressing PLAY and then CHEAT on both opening questions showed the expected explanations ("Exactly! Why let that moocher mooch off of you?" and "Wow, that's mean... and also the correct answer!"). The only console error again came from an installed wallet extension. Rebuilding the 15 effects from the recipe above, using only that text, reproduced the committed MP3s byte for byte.

Checked on 2026-10-24, without deploying, after `css/FONT-LICENSE.txt` was added. Copies of `pin/2026-10-23.1` and of this branch were served side by side with the Python HTTP server and opened in headless Chromium, 1280 px wide and as a 390 px wide phone. In both copies and at both sizes, the title screen, the introduction, the three slides of the first game, the start of the repeated game, the tournament's bets, its introduction and its first match, and the notes and credits pages loaded with no uncaught page error, no failed request, no answer of 400 or above, and no request to another site. Chromium drew the text in FuturaHandwritten, as before, apart from the arrow "→" and the dash "–", which the font does not have and which come from the system's fallback fonts; the tournament's scores, drawn on a canvas, use the font too. Every text sat in the same place in both copies, and none ran outside its box or the game's area.

## License and redistribution notes

The upstream project is dedicated to the public domain under CC0 1.0 Universal; see the unchanged `LICENSE`. The generated effects and the recipe above are dedicated under the same CC0 terms. Original library notices and copyright lines remain intact. Third-party libraries retain their own licenses; the upstream README is the original source-credit inventory and describes the upstream recordings, not the replacement effects in this branch.

The bundled Futura Handwritten font (`css/FuturaHandwritten.ttf`) by Billy Snyder stays, unchanged, because its author allows any use of it. Its terms are on the page the upstream README links to: the font's page on DaFont, which hosts its download. That page labels it "100% Free", and the author's note there says: "Feel free to use this font for anything you want. Crediting me would be absolutely wonderful, but I can't expect everyone to do it, so it isn't required." The note also asks: "If anything, at least send me a copy of the work when you use it. I love seeing my fonts in action." `css/FONT-LICENSE.txt` quotes the whole note, with the page's address and the date it was read, 2026-10-24.

DaFont calls its licence labels an indication, and points to the readme in the download and the author's own site for details. The download holds only the font file, byte for byte the bundled one, with no readme or licence file. The author's webcomic site, which the note names, says nothing about the font, and the font's name table gives only `BillySnyderPixelfailurecom` as its copyright line. Some font mirror sites show other labels (one calls it Creative Commons Attribution 4.0), but none of them is the author's or the download's own page. The upstream README's credit for the font stays.
