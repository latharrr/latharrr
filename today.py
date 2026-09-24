"""
Builds the terminal card at the top of the profile README (dark_mode.svg, light_mode.svg).

Everything static lives in PROFILE below; everything live comes from GitHub's GraphQL API.
The daily workflow runs this and commits the SVGs when they change. If an API call fails
the script exits before writing, so the card keeps its last good numbers.

    ACCESS_TOKEN=... USER_NAME=latharrr python today.py
"""
import datetime as dt
import os
import sys
import time
from html import escape
from pathlib import Path

import requests
from dateutil.relativedelta import relativedelta

ROOT = Path(__file__).parent
USER = os.environ.get('USER_NAME') or os.environ.get('GITHUB_REPOSITORY_OWNER') or 'latharrr'
TOKEN = os.environ.get('ACCESS_TOKEN') or os.environ.get('GITHUB_TOKEN')
BIRTHDAY = dt.date(2005, 6, 27)

PROFILE = [
    ('Host', "PicaPool · Founder's Office"),
    ('Role', 'Full-stack & AI Engineer'),
    ('Education', 'B.Tech CSE, LPU · 2024–28'),
    ('Location', 'Delhi NCR, India'),
    ('Uptime', None),  # filled in from BIRTHDAY
    None,
    ('Languages', 'TypeScript · JavaScript · Python · C++'),
    ('Stack', 'Next.js · Node · Supabase · LangGraph'),
    ('Automation', 'n8n · AI agents · WhatsApp API'),
    ('Shipped', 'ProofMart · Gapl · College-CLI'),
    None,
    ('Open to', 'Summer 2027 internships'),
    ('Website', 'deepanshulathar.com'),
]

# Markup and config files skew the language split toward landing pages, not code.
NOT_CODE = {'HTML', 'CSS', 'SCSS', 'Less', 'Dockerfile', 'Procfile', 'Makefile', 'Batchfile'}

THEMES = {
    'dark': dict(bg='#0d1117', bar='#161b22', border='#30363d', text='#e6edf3', key='#ffa657',
                 value='#a5d6ff', dim='#8b949e', faint='#484f58', rule='#30363d',
                 art_top='#79c0ff', art_bottom='#d2a8ff', track='#21262d'),
    'light': dict(bg='#ffffff', bar='#f6f8fa', border='#d0d7de', text='#1f2328', key='#953800',
                  value='#0a3069', dim='#59636e', faint='#8c959f', rule='#d0d7de',
                  art_top='#0550ae', art_bottom='#8250df', track='#eaeef2'),
}

# card geometry (px). Glyph width is 0.6em for every monospace font in the stack.
WIDTH, PAD, TITLE_H = 900, 28, 40
FONT, LINE = 14, 20
ART_FONT, ART_LINE = 8.5, 10.2   # keeps the glyph cell at the 0.5 aspect art/portrait.py assumes
KEY_COL = 16          # characters from the start of a key to the start of its value
TEXT_COLS = 62        # characters that fit in the right-hand column


# ---------------------------------------------------------------- GitHub

def graphql(query, **variables):
    for attempt in range(3):
        try:
            r = requests.post('https://api.github.com/graphql', timeout=30,
                              json={'query': query, 'variables': variables},
                              headers={'Authorization': f'bearer {TOKEN}'})
        except (requests.ConnectionError, requests.Timeout):
            if attempt == 2:
                raise
            time.sleep(5 * (attempt + 1))
            continue
        if r.status_code in (502, 503, 504) and attempt < 2:
            time.sleep(5 * (attempt + 1))
            continue
        r.raise_for_status()
        body = r.json()
        if body.get('errors') and not body.get('data'):
            raise RuntimeError(body['errors'])
        return body['data']


def fetch_stats():
    user = graphql('''
        query($login: String!) {
          user(login: $login) {
            createdAt
            repositories(ownerAffiliations: OWNER, isFork: false) { totalCount }
            pullRequests(states: MERGED) { totalCount }
          }
        }''', login=USER)['user']

    # contributionsCollection spans at most a year, so ask for each year since the account began
    today = dt.datetime.now(dt.timezone.utc)
    first_year = int(user['createdAt'][:4])
    years = '\n'.join(
        f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{min(dt.datetime(y, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc), today).isoformat()}") '
        '{ totalCommitContributions restrictedContributionsCount contributionCalendar { totalContributions } }'
        for y in range(first_year, today.year + 1))
    history = graphql(f'query($login: String!) {{ user(login: $login) {{ {years} }} }}', login=USER)['user']

    languages, cursor = {}, None
    while True:
        page = graphql('''
            query($login: String!, $cursor: String) {
              user(login: $login) {
                repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, isFork: false) {
                  nodes { languages(first: 20, orderBy: {field: SIZE, direction: DESC}) {
                    edges { size node { name color } } } }
                  pageInfo { hasNextPage endCursor }
                }
              }
            }''', login=USER, cursor=cursor)['user']['repositories']
        for repo in filter(None, page['nodes']):  # null for repos the token can't read
            for edge in repo['languages']['edges']:
                name = edge['node']['name']
                if name not in NOT_CODE:
                    size = languages.get(name, (0, None))[0]
                    languages[name] = (size + edge['size'], edge['node']['color'] or '#8b949e')
        if not page['pageInfo']['hasNextPage']:
            break
        cursor = page['pageInfo']['endCursor']

    return {
        'repos': user['repositories']['totalCount'],
        'merged_prs': user['pullRequests']['totalCount'],
        'contributions': sum(y['contributionCalendar']['totalContributions'] for y in history.values()),
        'commits': sum(y['totalCommitContributions'] for y in history.values()),
        'languages': sorted(((n, s, c) for n, (s, c) in languages.items()), key=lambda l: -l[1]),
    }


# ---------------------------------------------------------------- card

def uptime(today):
    d = relativedelta(today, BIRTHDAY)
    unit = lambda n, word: f"{n} {word}{'' if n == 1 else 's'}"
    return f"{unit(d.years, 'year')}, {unit(d.months, 'month')}, {unit(d.days, 'day')}"


def field(key, value, width=KEY_COL):
    """A key, dot leaders to column `width`, then the value: one aligned row of the card."""
    dots = '.' * max(1, width - len(key) - 2)
    return [(key, 'key'), (f' {dots} ', 'faint'), (value, 'value')]


def rule(label=''):
    lead = f'── {label} ' if label else ''
    return [(lead, 'dim'), ('─' * (TEXT_COLS - len(lead)), 'rule')]


def language_split(languages, top=5):
    total = sum(size for _, size, _ in languages) or 1
    head = [(name, size / total, color) for name, size, color in languages[:top] if size / total >= 0.01]
    rest = 1 - sum(share for _, share, _ in head)
    if rest > 0.005:
        head.append(('Other', rest, None))
    return head


def build_rows(stats, today):
    rows = [[('deepanshu', 'value'), ('@', 'dim'), ('lathar', 'value')], rule()]
    for item in PROFILE:
        if item is None:
            rows.append([])
        else:
            key, value = item
            rows.append(field(key, value if value is not None else uptime(today)))
    rows.append([])
    rows.append(rule('github'))
    n = lambda v: f'{v:,}'
    pairs = [
        (('Contributions', n(stats['contributions'])), ('Commits', n(stats['commits']))),
        (('Repositories', n(stats['repos'])), ('Merged PRs', n(stats['merged_prs']))),
    ]
    for (lk, lv), (rk, rv) in pairs:
        left = field(lk, lv)
        pad = 28 - sum(len(t) for t, _ in left)
        rows.append(left + [(' ' * pad, ''), ('│ ', 'rule')] + field(rk, rv, width=14))
    return rows


def spans(row):
    return ''.join(f'<tspan class="{cls}">{escape(text)}</tspan>' if cls else escape(text)
                   for text, cls in row)


def render(theme, stats, rows, art, split, today):
    t = THEMES[theme]
    char_w = FONT * 0.6
    art_w = max(len(line) for line in art) * ART_FONT * 0.6
    text_x = PAD + art_w + 36
    bar_y = TITLE_H + 26 + len(rows) * LINE + 6
    height = round(bar_y + 12 + LINE + PAD)
    body_top = TITLE_H + 26
    art_y = TITLE_H + (height - TITLE_H - len(art) * ART_LINE) / 2 + ART_FONT

    text_rows = '\n'.join(
        f'<tspan x="{text_x:.1f}" y="{body_top + i * LINE:.1f}">{spans(row)}</tspan>'
        for i, row in enumerate(rows) if row)
    art_rows = '\n'.join(
        f'<tspan x="{PAD}" y="{art_y + i * ART_LINE:.1f}">{escape(line)}</tspan>'
        for i, line in enumerate(art))

    # language bar: one segment per language, clipped to a rounded track
    bar_w = TEXT_COLS * char_w
    x, segments, legend, lx = text_x, [], [], text_x
    for name, share, color in split:
        w = share * bar_w
        segments.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{w + 0.5:.1f}" height="8" fill="{color or t["faint"]}"/>')
        x += w
        label = f'{name} {share * 100:.0f}%'
        legend.append(f'<circle cx="{lx + 4:.1f}" cy="{bar_y + 24:.1f}" r="4" fill="{color or t["faint"]}"/>'
                      f'<text x="{lx + 12:.1f}" y="{bar_y + 28:.1f}" class="legend">{escape(label)}</text>')
        lx += 12 + (len(label) + 2) * 12 * 0.6

    updated = today.strftime('%-d %b %Y')
    summary = (f"Deepanshu Lathar, full-stack and AI engineer. {stats['contributions']:,} contributions, "
               f"{stats['commits']:,} commits, {stats['repos']} repositories and {stats['merged_prs']} merged "
               f"pull requests on GitHub. Updated {updated}.")
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title desc" font-family="ui-monospace,'SFMono-Regular','SF Mono',Menlo,Consolas,'Liberation Mono',monospace">
<title id="title">deepanshu@lathar</title>
<desc id="desc">{escape(summary)}</desc>
<style>
text, tspan {{ white-space: pre; }}
.body {{ font-size: {FONT}px; fill: {t['text']}; }}
.key {{ fill: {t['key']}; }}
.value {{ fill: {t['value']}; }}
.dim {{ fill: {t['dim']}; }}
.faint {{ fill: {t['faint']}; }}
.rule {{ fill: {t['rule']}; }}
.art {{ font-size: {ART_FONT}px; fill: url(#art); }}
.legend {{ font-size: 12px; fill: {t['dim']}; }}
.chrome {{ font-size: 12px; fill: {t['dim']}; }}
.cursor {{ animation: blink 1.1s step-end infinite; }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
@media (prefers-reduced-motion: reduce) {{ .cursor {{ animation: none; }} }}
</style>
<defs>
<linearGradient id="art" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t['art_top']}"/><stop offset="1" stop-color="{t['art_bottom']}"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0.6" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0.25"/></linearGradient>
<mask id="fade-art"><rect x="0" y="{art_y - ART_FONT:.1f}" width="{PAD + art_w:.1f}" height="{len(art) * ART_LINE:.1f}" fill="url(#fade)"/></mask>
<clipPath id="card"><rect width="{WIDTH}" height="{height}" rx="12"/></clipPath>
<clipPath id="track"><rect x="{text_x:.1f}" y="{bar_y}" width="{bar_w:.1f}" height="8" rx="4"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{WIDTH}" height="{height}" fill="{t['bg']}"/>
<rect width="{WIDTH}" height="{TITLE_H}" fill="{t['bar']}"/>
<rect y="{TITLE_H - 1}" width="{WIDTH}" height="1" fill="{t['border']}"/>
</g>
<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="11.5" fill="none" stroke="{t['border']}"/>
<circle cx="22" cy="20" r="6" fill="#ff5f57"/><circle cx="42" cy="20" r="6" fill="#febc2e"/><circle cx="62" cy="20" r="6" fill="#28c840"/>
<text x="{WIDTH / 2}" y="24.5" text-anchor="middle" class="chrome">deepanshu@lathar: ~<tspan class="cursor"> ▍</tspan></text>
<text x="{WIDTH - 20}" y="24.5" text-anchor="end" class="chrome">updated {escape(updated)}</text>
<text class="art" aria-hidden="true" mask="url(#fade-art)">
{art_rows}
</text>
<text class="body">
{text_rows}
</text>
<rect x="{text_x:.1f}" y="{bar_y}" width="{bar_w:.1f}" height="8" rx="4" fill="{t['track']}"/>
<g clip-path="url(#track)">{''.join(segments)}</g>
{''.join(legend)}
</svg>
'''


def main():
    if not TOKEN:
        sys.exit('Set ACCESS_TOKEN (or GITHUB_TOKEN) to a token that can read your GitHub profile.')
    started = time.perf_counter()
    stats = fetch_stats()
    today = dt.date.today()
    rows = build_rows(stats, today)
    split = language_split(stats['languages'])
    art = (ROOT / 'art' / 'portrait.txt').read_text().rstrip('\n').split('\n')
    for theme in THEMES:
        (ROOT / f'{theme}_mode.svg').write_text(render(theme, stats, rows, art, split, today), encoding='utf-8')
    print(f"{USER}: {stats['contributions']:,} contributions, {stats['commits']:,} commits, "
          f"{stats['repos']} repos, {stats['merged_prs']} merged PRs, "
          f"top language {split[0][0] if split else 'n/a'} ({time.perf_counter() - started:.1f}s)")


if __name__ == '__main__':
    main()
