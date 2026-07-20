# scripts/

## `gen_cards.py` — regenerate the GitHub stat cards

Generates the static SVGs shown in the **GitHub Analytics** section of the
profile README:

| Output | Card | Selector |
|--------|------|----------|
| `assets/stats-card.svg`     | Stars / commits / PRs / issues / repos + contributions ring | `stats` |
| `assets/streak-card.svg`    | Total contributions, current streak, longest streak | `streak` |
| `assets/top-langs-card.svg` | Most-used languages bar + legend | `langs` |
| `assets/trophy-card.svg`    | Achievement tiles with letter ranks per metric | `trophy` |
| `assets/snake.svg`          | Animated snake eating the contribution grid (SMIL) | `snake` |

These are **static snapshots**, not live widgets — that's deliberate (no reliance
on a third-party rendering service), so the numbers only change when you re-run
this script.

### Update the numbers

1. Open [`gen_cards.py`](gen_cards.py). Each card has an `── EDIT THESE ──` block
   at the top of its function (`stats_card`, `streak_card`, `langs_card`, `trophy_card`).
2. Change the values. Also bump `ASOF` (the "as of" date stamp near the top).
3. Regenerate — run from anywhere, the output path is resolved relative to the script:

   ```bash
   python3 scripts/gen_cards.py          # all cards
   python3 scripts/gen_cards.py trophy   # just one (or several, space-separated)
   ```

4. Commit the changed `assets/*.svg`.

The accessibility `<desc>` text, the language-bar segment widths, and the trophy
letter ranks are all **derived** from the values you edit, so they can't drift.

### About the snake

`assets/snake.svg` is a **self-hosted replacement** for the Platane/snk GitHub
Action (which was never set up here — the `output` branch didn't exist, so the old
image 404'd). It's an animated SVG: a snake follows a serpentine path across the
53-week grid and "eats" each active day as it passes, looping forever via SMIL.

Because it's a static snapshot, it does **not** auto-update. To refresh: re-scrape
the contribution calendar, replace the `END` date and `filled` day→count map in
`snake_card()`, then `python3 scripts/gen_cards.py snake`. The animation uses
SMIL (`<animateMotion>` + `<animate>`); it renders as a still first frame in
non-animating contexts but animates in any modern browser (i.e. on GitHub).

### About the trophy ranks

The `trophy` card assigns a letter tier (C → SSS) to each metric. Those tiers use
**our own tunable thresholds** defined in `trophy_card()` — they are **not**
ryo-ma/github-profile-trophy's official grading. Edit each metric's `cutoffs`
list (7 ascending numbers = the bar to reach B, A, AA, AAA, S, SS, SSS) to
recalibrate how generous the grades are.

### One thing the script does NOT touch

The `<img alt="...">` text in `README.md` repeats some headline numbers for
screen-reader users. If you change the big figures (e.g. total contributions),
update those `alt` strings by hand too.

### Where the numbers came from

A snapshot pulled from the public GitHub API + the contribution calendar:

- **Languages** are weighted **per repository** (each repo counts equally) rather
  than by raw bytes. Byte-weighting is skewed here because one repo vendors a full
  CPython source tree, which would otherwise report ~86% Python. The card is
  labelled *"normalised per repository"* to make that explicit.
- **Streaks** are computed from the daily contribution calendar, capped at the
  snapshot date.

No dependencies beyond the Python 3 standard library.
