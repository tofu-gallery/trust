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
- Added `tools/generate-tofu-sounds.py` to reproduce those cues with Python 3 and ffmpeg. Neither tool is needed to host or play the committed site. Run `python3 -I tools/generate-tofu-sounds.py --output assets/sounds` from the repository root to regenerate them.
- Kept the CC0 music by Komiku, all original attribution, the upstream README, and LICENSE unchanged.

## Source and branches

- Upstream: https://github.com/ncase/trust
- Upstream default branch: `gh-pages`.
- Base commit: `6ec45d73befdb922bd40654dd1c1c903a953562f`.
- Gallery fork: https://github.com/tofu-gallery/trust
- `main` mirrors that upstream commit without adaptation commits; `gh-pages` is the fork's original upstream branch.
- `tofu` contains the adaptations. The gallery uses the verified commit tagged `pin/2026-10-23`.
- This preparation does not deploy the application or turn on GitHub Pages.

## Local verification

Verified on 2026-10-23 without deploying: the Python HTTP server served `/`, `/words.html`, `/notes/`, and `/peeps/` with HTTP 200. Every JavaScript file passed `node --check`, all 41 runtime asset paths existed, and ffmpeg decoded all 16 audio files. A real browser loaded all 16 sounds, entered the game, and selected CHEAT; the explanation advanced correctly. The browser requested no external resources. Its only captured console error came from an installed wallet extension (`chrome-extension://.../inpage.js`), not application code. This is a smoke check, not completion of the full 30-minute game or a mobile audit.

## License and redistribution notes

The upstream project is dedicated to the public domain under CC0 1.0 Universal; see the unchanged `LICENSE`. The generated effects and their generator are dedicated under the same CC0 terms. Original library notices and copyright lines remain intact. Third-party libraries retain their own licenses; the upstream README is the original source-credit inventory and describes the upstream recordings, not the replacement effects in this branch.

The bundled Futura Handwritten font by Bill Snyder is unchanged. Its embedded copyright names `BillySnyderPixelfailurecom`; the repository links to the font's source but includes no separate font-license text. Font redistribution terms should be confirmed before promoting this as a fully cleared commercial template. Local technical verification does not establish those rights.
