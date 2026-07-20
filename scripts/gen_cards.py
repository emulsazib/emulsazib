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


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("stats-card.svg", stats_card),
                     ("streak-card.svg", streak_card),
                     ("top-langs-card.svg", langs_card)]:
        p = os.path.join(OUT, name)
        with open(p, "w") as f:
            f.write(fn())
        print(f"wrote {p} ({os.path.getsize(p)} bytes)")
