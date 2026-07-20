#!/usr/bin/env python3
"""Generate the three static GitHub stat cards as self-contained SVGs.

HOW TO UPDATE THE NUMBERS
-------------------------
Each card's data lives in ONE labelled block at the top of its function
(stats_card / streak_card / langs_card), plus the ASOF date stamp below.
Edit those values, then from anywhere run:

    python3 scripts/gen_cards.py

It rewrites assets/stats-card.svg, assets/streak-card.svg and
assets/top-langs-card.svg. The accessibility description and the language-bar
segment widths are DERIVED from the numbers you edit, so they never drift.

NOTE: the README's own `alt="..."` text (assets/*.svg <img> tags in README.md)
also repeats some of these numbers and is NOT touched by this script — update
it by hand if you change the headline figures.

Data is a verified snapshot pulled from the public GitHub API. Bump ASOF
whenever you refresh the numbers. Palette matches the README:
bg #0d1117, accent #2C97DE, muted text #9f9f9f.
"""
import os

# ── date stamp shown on all three cards ──
ASOF = "21 Jul 2026"

NAME = "Emul Ahamed Sazib"

# assets dir, resolved relative to this file (<repo>/scripts/ -> <repo>/assets/)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

BG, ACCENT, TEXT, MUTED, FIRE = "#0d1117", "#2C97DE", "#9f9f9f", "#6b7681", "#FF6F00"
SANS = "Segoe UI, -apple-system, BlinkMacSystemFont, Helvetica Neue, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def head(w, h, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d" preserveAspectRatio="xMidYMid meet">\n'
            f'  <title id="t">{title}</title>\n  <desc id="d">{desc}</desc>\n'
            f'  <rect width="{w}" height="{h}" rx="6" fill="{BG}"/>\n')


def asof(w, h):
    return (f'  <text x="{w-14}" y="{h-9}" text-anchor="end" font-family="{MONO}" '
            f'font-size="9" fill="{MUTED}">as of {ASOF}</text>\n')


# tier ladder, lowest → highest, with the colour each tier is drawn in
TIERS = ["C", "B", "A", "AA", "AAA", "S", "SS", "SSS"]
TIER_COLOR = {
    "C": "#6b7681", "B": "#3FB950", "A": "#4FB0F0", "AA": "#2C97DE",
    "AAA": "#1f7fc4", "S": "#FFC93C", "SS": "#FFB000", "SSS": "#FFD700",
}


def rank(value, cutoffs):
    """Map a value to a tier using `cutoffs` (7 ascending thresholds for B..SSS).

    These thresholds are OUR tunable scheme — they are NOT ryo-ma/github-profile-
    trophy's private grading. Below the first cutoff is C; edit the cutoffs per
    metric in trophy_card() to taste. Returns (tier_label, progress_to_next 0..1).
    """
    t = 0
    for c in cutoffs:
        if value >= c:
            t += 1
        else:
            break
    if t >= len(cutoffs):                       # already at SSS
        prog = 1.0
    else:
        lower = cutoffs[t - 1] if t > 0 else 0
        span = cutoffs[t] - lower
        prog = max(0.0, min(1.0, (value - lower) / span)) if span else 1.0
    return TIERS[t], prog


# ─────────────────────────── card 1: overview stats ───────────────────────────
def stats_card():
    W, H = 460, 165
    # ── EDIT THESE ──
    stars, commits, prs, issues, repos = "20", "125", "6", "0", "24"
    contribs = 375
    # ────────────────
    rows = [
        ("Total Stars Earned",  stars),
        ("Total Commits",       commits),
        ("Total PRs",           prs),
        ("Total Issues",        issues),
        ("Public Repositories", repos),
    ]
    desc = (f"Static snapshot of GitHub statistics: {stars} stars, {commits} commits, "
            f"{prs} pull requests, {issues} issues, {repos} public repositories, "
            f"{contribs} total contributions.")
    s = head(W, H, f"{NAME}'s GitHub Stats", desc)
    s += (f'  <text x="22" y="30" font-family="{SANS}" font-size="15" font-weight="600" '
          f'fill="{ACCENT}">{NAME}\'s GitHub Stats</text>\n')

    y = 58
    for label, val in rows:
        s += (f'  <circle cx="27" cy="{y-4}" r="2.5" fill="{ACCENT}"/>\n'
              f'  <text x="40" y="{y}" font-family="{SANS}" font-size="12.5" fill="{TEXT}">{label}</text>\n'
              f'  <text x="300" y="{y}" font-family="{SANS}" font-size="12.5" font-weight="700" '
              f'text-anchor="end" fill="{ACCENT}">{val}</text>\n')
        y += 21

    # contributions ring. A full ring, not a partial arc: a partial arc would imply
    # a percentage-of-something, and there is no such denominator here.
    cx, cy, r = 385, 88, 40
    s += (f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1f2630" stroke-width="6"/>\n'
          f'  <circle cx="{cx}" cy="{cy}" r="{r-9}" fill="none" stroke="{ACCENT}" stroke-width="2" '
          f'opacity="0.55"/>\n'
          f'  <text x="{cx}" y="{cy+1}" text-anchor="middle" font-family="{SANS}" font-size="23" '
          f'font-weight="700" fill="#ffffff">{contribs}</text>\n'
          f'  <text x="{cx}" y="{cy+17}" text-anchor="middle" font-family="{MONO}" font-size="6.5" '
          f'letter-spacing="0.5" fill="{MUTED}">CONTRIBUTIONS</text>\n')
    return s + asof(W, H) + '</svg>\n'


# ─────────────────────────── card 2: streak ───────────────────────────
def streak_card():
    W, H = 470, 165
    # ── EDIT THESE ──
    contribs, current, longest = 375, 6, 6
    span_all     = "Jan 1, 2022 – Jul 21, 2026"
    span_current = "Jul 16 – Jul 21, 2026"
    span_longest = "Jun 13 – Jun 18, 2026"
    # ────────────────
    desc = (f"Static snapshot: {contribs} total contributions since 2022, "
            f"current streak {current} days, longest streak {longest} days.")
    s = head(W, H, "GitHub Contribution Streak", desc)
    cols = [
        (78,  str(contribs), "Total Contributions", span_all,     TEXT),
        (235, str(current),  "Current Streak",      span_current, FIRE),
        (392, str(longest),  "Longest Streak",      span_longest, TEXT),
    ]
    for x, big, label, sub, colour in cols:
        s += (f'  <text x="{x}" y="62" text-anchor="middle" font-family="{SANS}" font-size="30" '
              f'font-weight="700" fill="#ffffff">{big}</text>\n'
              f'  <text x="{x}" y="87" text-anchor="middle" font-family="{SANS}" font-size="12.5" '
              f'font-weight="600" fill="{colour}">{label}</text>\n'
              f'  <text x="{x}" y="106" text-anchor="middle" font-family="{MONO}" font-size="9" '
              f'fill="{MUTED}">{sub}</text>\n')

    # flame above the current-streak column — kept clear of the digit's cap height (~y41)
    s += (f'  <path d="M235 11 c 6 6 9 10 9 14 a 9 9 0 0 1 -18 0 c 0 -4 3 -8 9 -14 z" '
          f'fill="none" stroke="{FIRE}" stroke-width="1.8"/>\n')
    for x in (156, 313):
        s += f'  <path d="M{x} 42 V 116" stroke="#1f2630" stroke-width="1.5"/>\n'
    return s + asof(W, H) + '</svg>\n'


# ─────────────────────────── card 3: top languages ───────────────────────────
def langs_card():
    W, H = 350, 188
    # ── EDIT THESE ── (name, percent, hex colour). Bar widths are derived from the
    # percentages; each repo is weighted equally so one vendored tree can't dominate.
    langs = [
        ("Python",           65.0, "#3572A5"),
        ("JavaScript",       57.0, "#f1e05a"),
        ("Java",             59.1, "#b07219"),
        ("Kotlin",           19.1, "#A97BFF"),
        ("C++",              39.0, "#f34b7d"),
        ("C",                38.6, "#555555"),
        ("TypeScript",       27.2, "#3178c6"),
        ("Jupyter Notebook", 26.0, "#DA5B0B"),
    ]
    # ────────────────
    s = head(W, H, "Most Used Languages",
             "Static snapshot of language usage, normalised per repository: " +
             ", ".join(f"{n} {p} percent" for n, p, _ in langs) + ".")
    s += (f'  <text x="20" y="30" font-family="{SANS}" font-size="15" font-weight="600" '
          f'fill="{ACCENT}">Most Used Languages</text>\n')

    # stacked bar, scaled so the shown languages fill the full width
    bx, bw, tot = 20, W - 40, sum(p for _, p, _ in langs)
    s += f'  <mask id="bar"><rect x="{bx}" y="44" width="{bw}" height="10" rx="5" fill="#fff"/></mask>\n'
    s += '  <g mask="url(#bar)">\n'
    x = bx
    for _, p, c in langs:
        w = bw * p / tot
        s += f'    <rect x="{x:.2f}" y="44" width="{w:.2f}" height="10" fill="{c}"/>\n'
        x += w
    s += '  </g>\n'

    # two-column legend
    y0 = 82
    for i, (name, p, c) in enumerate(langs):
        col, row = i % 2, i // 2
        x = 22 + col * 158
        y = y0 + row * 21
        s += (f'  <circle cx="{x+4}" cy="{y-4}" r="5" fill="{c}"/>\n'
              f'  <text x="{x+15}" y="{y}" font-family="{SANS}" font-size="10.5" fill="{TEXT}">{name}</text>\n'
              f'  <text x="{x+146}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="10" '
              f'fill="{MUTED}">{p:.1f}%</text>\n')

    s += (f'  <text x="20" y="{H-9}" font-family="{MONO}" font-size="8.5" fill="{MUTED}">'
          f'normalised per repository</text>\n')
    return s + asof(W, H) + '</svg>\n'


# ─────────────────────────── card 4: trophies / achievements ───────────────────────────
def trophy_card():
    W, H = 880, 175
    # ── EDIT THESE ── (label, value, cutoffs for B,A,AA,AAA,S,SS,SSS).
    # Cutoffs are a tunable scheme, NOT GitHub's official trophy grading — see rank().
    metrics = [
        ("Stars",     20,  [5, 20, 50, 150, 500, 1000, 2000]),
        ("Commits",   125, [30, 100, 500, 1000, 2000, 5000, 10000]),
        ("Followers", 11,  [5, 25, 75, 250, 1000, 3000, 10000]),
        ("Repos",     24,  [5, 20, 50, 100, 200, 500, 1000]),
        ("PRs",       6,   [3, 15, 40, 100, 300, 500, 1000]),
        ("Issues",    0,   [3, 15, 40, 100, 300, 500, 1000]),
        ("Contribs",  375, [100, 400, 1000, 2000, 5000, 10000, 20000]),
    ]
    # ────────────────
    graded = [(lbl, val, *rank(val, cut)) for lbl, val, cut in metrics]  # (label, value, tier, prog)

    desc = "GitHub achievements (tunable thresholds): " + ", ".join(
        f"{lbl} rank {tier} ({val})" for lbl, val, tier, _ in graded) + "."
    s = head(W, H, "GitHub Achievements", desc)
    s += (f'  <text x="16" y="30" font-family="{SANS}" font-size="15" font-weight="600" '
          f'fill="{ACCENT}">GitHub Achievements</text>\n')

    pad, gap, n = 16, 8, len(graded)
    tw = (W - 2 * pad - gap * (n - 1)) / n
    top, th = 46, 104
    for i, (lbl, val, tier, prog) in enumerate(graded):
        tx = pad + i * (tw + gap)
        cx = tx + tw / 2
        col = TIER_COLOR[tier]
        fs = {1: 26, 2: 21, 3: 16}[len(tier)]           # shrink so "SSS" still fits
        # tile + tier-coloured top accent
        s += (f'  <rect x="{tx:.1f}" y="{top}" width="{tw:.1f}" height="{th}" rx="6" '
              f'fill="#0e1622" stroke="{col}" stroke-opacity="0.4" stroke-width="1"/>\n'
              f'  <rect x="{tx:.1f}" y="{top}" width="{tw:.1f}" height="3" rx="1.5" fill="{col}"/>\n'
              f'  <text x="{cx:.1f}" y="{top+42}" text-anchor="middle" font-family="{SANS}" '
              f'font-size="{fs}" font-weight="700" fill="{col}">{tier}</text>\n'
              f'  <text x="{cx:.1f}" y="{top+63}" text-anchor="middle" font-family="{SANS}" '
              f'font-size="9.5" fill="{MUTED}">{lbl}</text>\n'
              f'  <text x="{cx:.1f}" y="{top+83}" text-anchor="middle" font-family="{SANS}" '
              f'font-size="15" font-weight="700" fill="#ffffff">{val}</text>\n')
        # progress-to-next-tier bar
        bx, bw = tx + 12, tw - 24
        s += (f'  <rect x="{bx:.1f}" y="{top+92}" width="{bw:.1f}" height="4" rx="2" fill="#1f2630"/>\n'
              f'  <rect x="{bx:.1f}" y="{top+92}" width="{bw*prog:.1f}" height="4" rx="2" fill="{col}"/>\n')
    return s + asof(W, H) + '</svg>\n'


# ─────────────────────────── card 5: contribution-grid snake ───────────────────────────
# An animated SVG: a snake sweeps the real contribution grid in a serpentine path,
# "eating" each filled cell as its head passes (SMIL, synced to one clock, loops forever).
# Self-hosted replacement for the Platane/snk GitHub Action image.
def snake_card():
    import datetime
    # ── EDIT THESE ── grid window end + the filled days in it (date -> contribution count).
    # Missing days in the 53-week window are treated as empty. Regenerate this block by
    # re-running the contribution scrape; see scripts/README.md.
    END = "2026-07-21"
    filled = {
        "2025-08-05": 1, "2025-08-06": 1, "2025-08-16": 3, "2025-10-05": 3,
        "2025-10-26": 31, "2025-10-27": 4, "2025-10-30": 2, "2025-11-01": 12,
        "2025-11-02": 2, "2025-11-03": 4, "2025-11-07": 35, "2025-11-08": 4,
        "2025-11-09": 6, "2025-11-20": 1, "2025-11-21": 6, "2025-11-22": 2,
        "2025-11-29": 10, "2025-12-01": 4, "2025-12-02": 4, "2025-12-03": 3,
        "2025-12-04": 11, "2025-12-12": 1, "2025-12-13": 2, "2026-02-04": 2,
        "2026-02-21": 1, "2026-02-22": 1, "2026-02-24": 1, "2026-03-09": 1, "2026-03-10": 4,
        "2026-03-11": 2, "2026-04-03": 1, "2026-04-06": 3, "2026-04-07": 1, "2026-04-12": 2,
        "2026-04-27": 1, "2026-04-28": 7, "2026-04-29": 1, "2026-06-08": 2, "2026-06-09": 5,
        "2026-06-10": 2, "2026-06-13": 4, "2026-06-14": 5, "2026-06-15": 1, "2026-06-16": 1,
        "2026-06-17": 1, "2026-06-18": 3, "2026-06-20": 2, "2026-06-21": 2, "2026-06-22": 2,
        "2026-06-23": 7, "2026-06-24": 1, "2026-06-25": 12, "2026-06-28": 1,
        "2026-07-01": 2, "2026-07-02": 11, "2026-07-03": 3, "2026-07-05": 9,
        "2026-07-06": 5, "2026-07-09": 5, "2026-07-11": 3, "2026-07-12": 2, "2026-07-13": 3,
        "2026-07-14": 10, "2026-07-16": 4, "2026-07-17": 15, "2026-07-18": 3,
        "2026-07-19": 5, "2026-07-20": 11, "2026-07-21": 12,
    }
    DUR = 15.0            # seconds per full sweep (loops forever)
    # blue level ramp on the #0d1117 panel, to match the rest of the profile
    LVL = ["#161b22", "#0e3a5c", "#155e8b", "#1f7fc4", "#2C97DE"]
    SNAKE = "#FF6F00"     # warm contrast against the blue grid (matches the streak flame)
    # ────────────────

    def level(n):
        return 0 if n <= 0 else 1 if n < 3 else 2 if n < 6 else 3 if n < 10 else 4

    end = datetime.date.fromisoformat(END)
    start = end - datetime.timedelta(days=(end.weekday() + 1) % 7) - datetime.timedelta(weeks=52)
    COLS, ROWS = 53, 7
    cell, gap = 11, 3
    pitch = cell + gap
    ox, oy = 16, 34                      # grid origin (leaves room for a title row)
    W = ox * 2 + COLS * pitch - gap
    H = oy + ROWS * pitch - gap + 16

    # visit order = vertical boustrophedon; collect drawable cells + the snake path
    order, cells = [], {}
    for c in range(COLS):
        rows = range(ROWS) if c % 2 == 0 else range(ROWS - 1, -1, -1)
        for r in rows:
            d = start + datetime.timedelta(weeks=c, days=r)
            if d > end:
                continue
            x = ox + c * pitch
            y = oy + r * pitch
            cells[(c, r)] = (x, y, filled.get(d.isoformat(), 0))
            order.append((c, r, x + cell / 2, y + cell / 2))

    V = len(order)
    idx = {(c, r): i for i, (c, r, *_ ) in enumerate(order)}   # cell -> visit index
    path = "M" + " L".join(f"{cx:.1f},{cy:.1f}" for _, _, cx, cy in order)

    desc = (f"Animated contribution grid for the 53 weeks ending {END}: a snake sweeps the "
            f"grid and eats each active day. {len(filled)} active days.")
    s = head(W, H, "Contribution snake", desc)
    s += (f'  <text x="{ox}" y="24" font-family="{SANS}" font-size="14" font-weight="600" '
          f'fill="{ACCENT}">Contribution Snake</text>\n')

    # grid cells; filled ones get a SMIL "eaten" transition synced to the head's arrival
    eat = 0.15 / DUR                     # fraction of the loop the fade takes
    for c in range(COLS):
        for r in range(ROWS):
            if (c, r) not in cells:
                continue
            x, y, n = cells[(c, r)]
            lv = level(n)
            s += (f'  <rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" '
                  f'fill="{LVL[lv]}">')
            if lv > 0:
                a = idx[(c, r)] / (V - 1)     # head arrives here at this fraction of the loop
                b = min(a + eat, 1.0)
                s += (f'<animate attributeName="fill" values="{LVL[lv]};{LVL[lv]};{LVL[0]};{LVL[0]}" '
                      f'keyTimes="0;{a:.4f};{b:.4f};1" dur="{DUR}s" begin="0s" '
                      f'repeatCount="indefinite" calcMode="discrete"/>')
            s += '</rect>\n'

    # snake: head + trailing body segments, all following the shared path
    seg = [(SNAKE, 1.0, cell + 1), (SNAKE, 0.85, cell), (SNAKE, 0.7, cell - 1),
           (SNAKE, 0.55, cell - 2), (SNAKE, 0.4, cell - 3)]
    step = 0.45                          # seconds each body segment trails the one ahead
    for i, (col, op, sz) in enumerate(seg):
        off = sz / 2
        s += (f'  <rect x="{-off:.1f}" y="{-off:.1f}" width="{sz}" height="{sz}" rx="{sz/3:.1f}" '
              f'fill="{col}" opacity="{op}">'
              f'<animateMotion path="{path}" dur="{DUR}s" begin="{i*step:.2f}s" '
              f'repeatCount="indefinite" calcMode="linear"/></rect>\n')

    return s + asof(W, H) + '</svg>\n'


CARDS = {
    "stats":  ("stats-card.svg",     stats_card),
    "streak": ("streak-card.svg",    streak_card),
    "langs":  ("top-langs-card.svg", langs_card),
    "trophy": ("trophy-card.svg",    trophy_card),
    "snake":  ("snake.svg",          snake_card),
}

if __name__ == "__main__":
    import sys
    os.makedirs(OUT, exist_ok=True)
    # optional args pick which cards to write; no args = all of them
    selected = sys.argv[1:] or list(CARDS)
    for key in selected:
        if key not in CARDS:
            print(f"unknown card '{key}'; choose from {', '.join(CARDS)}")
            continue
        name, fn = CARDS[key]
        p = os.path.join(OUT, name)
        with open(p, "w") as f:
            f.write(fn())
        print(f"wrote {p} ({os.path.getsize(p)} bytes)")
