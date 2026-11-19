#!/usr/bin/env python3
"""Build page5.html (variant B: 35 stories) and page5a.html (variant A: 42 stories)
for news-image-20261119 round 5, from the round-4 page.html.

Evidence from live top 1/2/3/10 (20 Nov 02:40 WIB):
- 33-36 stories, NOT 42. All four winners: masthead ~60-90px, 3 heroes with
  TALL scenes (~120-200px), hero headlines 26-30px, mid grid 2 rows x 5
  (10 cards), mid headlines 16-17px, ALSO list 18-23 one-liners.
- Our r4: masthead 46px, hero scenes 56px, hero headline 19.5px, mids 2x6,
  mid headline 13.5px, 42 stories. At 300px our headlines are mush (5.7px)
  while theirs read (8-9px).
Changes vs r4:
- masthead 46->60px, hero scene 56->120px, hero h2 19.5->27px, hero p 12.5->15px
- mids 6-per-row -> 5-per-row (10 cards); mid scene 20->40px, h3 13.5->17px,
  mid p 12->13.5px
- stats 7 -> 6 (drop Florida rain), numbers 21->26px, labels 9.5->11px
- timeline strip REMOVED (top 1/3/10 have none; frees ~45px for hero art)
- ALSO items 12->13px, line-height 1.28->1.38
- demote mids #10 Florida + #15 Caracas to ALSO (they stay stories)
- variant B cuts 7 weakest ALSO items -> 35 stories total
- region counts recomputed for variant B (42 -> 35)
- zero 'ICC' anywhere (grep-verified after build); 'ICJ:' prefix kept
"""
import re, sys

SRC = '/home/hatch/workspace/makefun/news-image-20261119/page.html'
OUT_B = '/home/hatch/workspace/makefun/news-image-20261119/page5.html'
OUT_A = '/home/hatch/workspace/makefun/news-image-20261119/page5a.html'

html = open(SRC).read()
assert 'ICC' not in html, 'source already contains ICC?!'

# ---------- 1. CSS changes ----------
css = [
    # masthead
    ('font-weight: 900; font-size: 46px; line-height: 1.05; letter-spacing: -0.01em;',
     'font-weight: 900; font-size: 60px; line-height: 1.02; letter-spacing: -0.02em;'),
    ('font-size: 14.5px; line-height: 1.25;', 'font-size: 16px; line-height: 1.25;'),
    # regions
    ('font-size: 11px; font-weight: 700; letter-spacing: 0.06em;',
     'font-size: 12px; font-weight: 700; letter-spacing: 0.06em;'),
    # stat numbers + labels
    ('font-size: 21px; line-height: 1.05; color: var(--red);',
     'font-size: 26px; line-height: 1.05; color: var(--red);'),
    ('font-size: 9.5px; font-weight: 700;\n    letter-spacing: 0.08em;',
     'font-size: 11px; font-weight: 700;\n    letter-spacing: 0.08em;'),
    # hero scenes + headlines + dek
    ('.hero svg.scene { display: block; width: 100%; height: 56px; }',
     '.hero svg.scene { display: block; width: 100%; height: 120px; }'),
    ('font-size: 19.5px; line-height: 1.15;', 'font-size: 27px; line-height: 1.12;'),
    ('.hero p { font-size: 12.5px; line-height: 1.5;',
     '.hero p { font-size: 15px; line-height: 1.45;'),
    # mid scenes + headlines + dek
    ('.mid svg.scene { display: block; width: 100%; height: 20px; }',
     '.mid svg.scene { display: block; width: 100%; height: 40px; }'),
    ('font-size: 13.5px; line-height: 1.22;', 'font-size: 17px; line-height: 1.2;'),
    ('.mid p { font-size: 12px; line-height: 1.45;',
     '.mid p { font-size: 13.5px; line-height: 1.45;'),
    # ALSO items
    ('.alsoitem { font-size: 12px; line-height: 1.28;',
     '.alsoitem { font-size: 13px; line-height: 1.32;'),
    # mid dek line-height (tighter, still >= 1.35 for 2-line text)
    ('.mid p { font-size: 13.5px; line-height: 1.45;',
     '.mid p { font-size: 13.5px; line-height: 1.35;'),
    # mid scenes 40 -> 36px
    ('.mid svg.scene { display: block; width: 100%; height: 40px; }',
     '.mid svg.scene { display: block; width: 100%; height: 36px; }'),
    # verdict + legend + markets rail (tighten the tallest bottom column)
    ('font-size: 15px; line-height: 1.2; margin-top: 3px;',
     'font-size: 14px; line-height: 1.2; margin-top: 3px;'),
    ('.legend .li { font-size: 11px; line-height: 1.4; color: #33302a; margin-top: 2px; }',
     '.legend .li { font-size: 11px; line-height: 1.3; color: #33302a; margin-top: 1px; }'),
    # shave vertical gaps across sections (1-2px each, ~9px total)
    ('display: flex; margin-top: 4px; padding: 3px 0 2px;',
     'display: flex; margin-top: 3px; padding: 2px 0 1px;'),
    ('.heroes { display: flex; gap: 12px; margin-top: 3px; }',
     '.heroes { display: flex; gap: 12px; margin-top: 2px; }'),
    ('.mids { display: flex; gap: 12px; margin-top: 4px; }',
     '.mids { display: flex; gap: 12px; margin-top: 3px; }'),
    ('.bottom { display: flex; gap: 10px; margin-top: 4px; padding-top: 3px;',
     '.bottom { display: flex; gap: 10px; margin-top: 3px; padding-top: 2px;'),
    ('margin-top: 4px; padding: 4px 8px; border: 1.5px solid var(--red);',
     'margin-top: 3px; padding: 3px 8px; border: 1.5px solid var(--red);'),
    # topbar
    ('font-size: 10px; font-weight: 700; letter-spacing: 2.4px;',
     'font-size: 11px; font-weight: 700; letter-spacing: 2.4px;'),
    # datecheck + footer
    ('font-size: 11px; line-height: 1.4; color: #33302a;\n  }\n  .datecheck b',
     'font-size: 12px; line-height: 1.45; color: #33302a;\n  }\n  .datecheck b'),
    ('font-size: 9.5px; line-height: 1.45; color: var(--mut);',
     'font-size: 10.5px; line-height: 1.45; color: var(--mut);'),
    # ---- second-stage height trims (run AFTER the first-stage values exist) ----
    # masthead 60 -> 50px (still bigger than r4's 46px)
    ('font-weight: 900; font-size: 60px; line-height: 1.02; letter-spacing: -0.02em;',
     'font-weight: 900; font-size: 50px; line-height: 1.02; letter-spacing: -0.02em;'),
    # hero scenes 120 -> 88px (still ~60% taller than r4's 56px; near true aspect)
    ('.hero svg.scene { display: block; width: 100%; height: 120px; }',
     '.hero svg.scene { display: block; width: 100%; height: 88px; }'),
    # hero headlines 27 -> 25px (still 2 lines)
    ('font-size: 27px; line-height: 1.12;', 'font-size: 25px; line-height: 1.12;'),
    # mid scenes 36 -> 28px
    ('.mid svg.scene { display: block; width: 100%; height: 36px; }',
     '.mid svg.scene { display: block; width: 100%; height: 28px; }'),
    # ALSO 13 -> 12px (12.5px overflowed the ~260px columns on the longest items)
    ('.alsoitem { font-size: 13px; line-height: 1.32;',
     '.alsoitem { font-size: 12px; line-height: 1.30;'),
]
for old, new in css:
    assert old in html, f'CSS pattern missing: {old[:60]}'
    html = html.replace(old, new, 1)

# ---------- 1b. Body trims so everything fits 1024px (measured overflow: 182px) ----------
# Drop the 7th stat (Florida rain) -> 6 stats, wider columns, 1-line labels.
m = re.search(r'<div class="stat"><div class="n">15\.3 in</div>.*?</div>\n', html, re.S)
assert m, '7th stat not found'
html = html[:m.start()] + html[m.end():]
# Shorten stat labels to one line each.
body = [
    ('Anthropic IPO &mdash; biggest ever', 'Anthropic IPO &mdash; record'),
    ('Between GTA V and GTA VI', 'GTA V to GTA VI'),
    ('ICJ vote: Myanmar guilty', 'ICJ: Myanmar guilty'),
    ('Rohingya fled in 2017', 'Rohingya fled'),
    ('Van Gogh &mdash; artist record', 'Van Gogh record'),
    ('Australia jobless, 5-year high', 'Australia jobless'),
    # Hero 1 + 3 headlines: 3 lines -> 2 lines at 27px.
    ('Trump, Xi and Putin hold first three-way summit',
     'Trump, Xi and Putin hold first summit'),
    ('Anthropic debuts in the biggest IPO on record',
     'Anthropic debuts in record $81.3bn IPO'),
    # Hero 1 + 3 deks: 3 lines -> 2 lines at 15px.
    ('US, China and Russia leaders met at APEC; nuclear arms, Ukraine and Iran on agenda.',
     'US, China and Russia leaders met at APEC; nuclear arms and Ukraine on agenda.'),
    ('Claude&rsquo;s maker raised $81.3bn at $83 a share, past SpaceX&rsquo;s $75bn. Trading starts today.',
     'Claude&rsquo;s maker raised $81.3bn at $83 a share, past SpaceX&rsquo;s $75bn record.'),
    # Markets rail: 4 rows -> 3 (drop RBA cash rate).
    ('<div class="mi"><span>RBA cash rate</span><b>4.85%</b></div>', ''),
    # Shorten ALSO items that overflow the ~260px columns at 12px (nowrap).
    ('St Johns River flood record.', 'St Johns River record.'),
    ('MEASLES</b> &mdash; US loses elimination status.',
     'MEASLES</b> &mdash; Elimination status lost.'),
    ('Litton Das sets Test record.', 'Litton Das sets record.'),
    # Verdict header wraps to 2 lines -> shorten to 1 line.
    ('THE VERDICT &middot; THE HAGUE &middot; 10:00', 'THE VERDICT &middot; 10:00'),
    # Verdict body 3 lines -> 2 lines.
    ('First state the court holds liable. Must allow return, make reparations.',
     'First state held liable. Must allow return, pay reparations.'),
]
for old, new in body:
    assert old in html, f'body pattern missing: {old[:60]}'
    html = html.replace(old, new, 1)

# ---------- 2. Remove the timeline strip ----------
m = re.search(r'\n  <div class="timeline">.*?\n  </div>\n', html, re.S)
assert m, 'timeline block not found'
html = html[:m.start()] + '\n' + html[m.end():]

# ---------- 3. Split out the mid cards ----------
def split_blocks(s, pattern):
    """Split sibling <div ...> blocks matching regex `pattern` by div-depth counting."""
    blocks, pos = [], 0
    while True:
        m = re.search(pattern, s[pos:])
        if not m:
            break
        i = pos + m.start()
        depth = 0
        j = i
        while True:
            nxt_open = s.find('<div', j)
            nxt_close = s.find('</div>', j)
            if nxt_close < 0:
                raise ValueError('unbalanced divs')
            if nxt_open >= 0 and nxt_open < nxt_close:
                depth += 1
                j = nxt_open + 4
            else:
                depth -= 1
                j = nxt_close + 6
                if depth == 0:
                    break
        blocks.append((i, j))
        pos = j
    return blocks

# find the two .mids containers and extract their .mid children
mids_spans = split_blocks(html, r'<div class="mids[\s"]')
assert len(mids_spans) == 2, f'expected 2 .mids, got {len(mids_spans)}'
mid_cards = []
for (a, b) in mids_spans:
    seg = html[a:b]
    for (x, y) in split_blocks(seg, r'<div class="mid"'):
        mid_cards.append(seg[x:y])
assert len(mid_cards) == 12, f'expected 12 mid cards, got {len(mid_cards)}'

def card_num(card):
    m = re.search(r'<span class="num">(\d+)</span>', card)
    return int(m.group(1))

by_num = {card_num(c): c for c in mid_cards}
# demote #10 Florida and #15 Caracas to ALSO; keep 10 mids
DEMOTE = {10, 15}
kept = [by_num[n] for n in sorted(by_num) if n not in DEMOTE]
assert len(kept) == 10
# renumber mids 4..13 in order
renumbered_mids = []
for i, card in enumerate(kept, start=4):
    renumbered_mids.append(re.sub(r'<span class="num">\d+</span>',
                                  f'<span class="num">{i}</span>', card, count=1))

def build_mids(cards):
    out = []
    for row in (cards[:5], cards[5:]):
        inner = '\n    '.join(row)
        out.append(f'  <div class="mids">\n    {inner}\n  </div>')
    return '\n\n  '.join(out)

# rebuild the mids region: replace from first .mids start to second .mids end
new_mids_html = build_mids(renumbered_mids)
# second row keeps class "mids mids2" for the margin rule
new_mids_html = new_mids_html.replace('<div class="mids">\n    <div class="mid">\n      <svg class="scene" viewBox="0 0 155 42"',
                                      '<div class="mids mids2">\n    <div class="mid">\n      <svg class="scene" viewBox="0 0 155 42"', 1) \
    if False else new_mids_html
# simpler: mark the second container explicitly
parts = new_mids_html.split('  <div class="mids">')
assert len(parts) == 3, parts
new_mids_html = parts[0] + '  <div class="mids">' + parts[1] + '  <div class="mids mids2">' + parts[2]

html = html[:mids_spans[0][0]] + new_mids_html + html[mids_spans[1][1]:]

# ---------- 4. ALSO list ----------
also_items = re.findall(r'<div class="alsoitem">.*?</div>', html, re.S)
assert len(also_items) == 27, f'expected 27 also items, got {len(also_items)}'

def also_num(item):
    return int(re.search(r'<span class="no">(\d+)</span>', item).group(1))

# demoted mids become ALSO items (Florida, Caracas)
florida = '<div class="alsoitem"><span class="no">XX</span> &nbsp;<b>FLORIDA</b> &mdash; Floods shut schools.</div>'
caracas = '<div class="alsoitem"><span class="no">XX</span> &nbsp;<b>CARACAS</b> &mdash; US signs military pact.</div>'

# variant A: all 27 + 2 demoted = 29 ALSO items, total 3+10+29 = 42
also_A = also_items + [florida, caracas]
# variant B: cut 7 weakest (Senegal boat, Ebola trials, England ODI, Nigeria miners,
# Bancroft, Badminton Sindhu, CAF assembly) from the 29 -> 22 ALSO, total 35
CUT_MARKERS = ['SENEGAL', 'Trials of two new vaccines', 'England win ODI',
               'Justice for 37 miners', 'Bancroft: all knew',
               'Sindhu back in top five', 'Assembly opens in Abuja']
also_B = [it for it in also_A if not any(c in it for c in CUT_MARKERS)]
assert len(also_B) == 22, f'variant B ALSO count {len(also_B)}'

def renumber_also(items, start=14):
    out = []
    for i, it in enumerate(items, start=start):
        out.append(re.sub(r'<span class="no">[^<]+</span>',
                          f'<span class="no">{i}</span>', it, count=1))
    return out

def build_also(items, more_n):
    cols = [items[:len(items)//2 + len(items) % 2], items[len(items)//2 + len(items) % 2:]]
    # balance: 22 -> 11/11; 29 -> 15/14
    c1 = '\n          '.join(cols[0])
    c2 = '\n          '.join(cols[1])
    return (f'<div class="sect"><span>&#9679;</span> Also on Thursday 19 November &mdash; {more_n} more stories</div>\n'
            f'      <div class="alsocols">\n        <div class="alsocol">\n          {c1}\n        </div>\n'
            f'        <div class="alsocol">\n          {c2}\n        </div>\n      </div>')

# replace the ALSO section (from its sect div to the end of alsocols)
m = re.search(r'<div class="sect"><span>&#9679;</span> Also on Thursday 19 November.*?</div>\n      </div>', html, re.S)
assert m, 'ALSO section not found'

def make_variant(also_list, total, region_counts):
    h = html[:m.start()] + build_also(renumber_also(also_list), len(also_list)) + html[m.end():]
    h = h.replace('42 stories &middot; 7 regions', f'{total} stories &middot; 7 regions')
    # region bar counts
    for cls, n in region_counts.items():
        h = re.sub(rf'(<div class="{cls}">)([A-Za-z\- ]+) \d+(</div>)',
                   rf'\g<1>\g<2> {n}\g<3>', h, count=1)
    # datebox stays; title tag update
    assert 'ICC' not in h, 'ICC leaked into variant!'
    return h

# variant A: 42 stories, original region counts
regions_A = {'r-af': 9, 'r-ap': 8, 'r-am': 7, 'r-me': 5, 'r-oc': 5, 'r-wo': 5, 'r-eu': 3}
# variant B: 35 stories; cuts: Senegal(Africa), Nigeria miners(Africa), CAF(Africa),
# Badminton(Asia-Pacific), England ODI(Europe), Ebola trials(World), Bancroft(Oceania)
regions_B = {'r-af': 6, 'r-ap': 7, 'r-am': 7, 'r-me': 5, 'r-oc': 4, 'r-wo': 4, 'r-eu': 2}

html_A = make_variant(also_A, 42, regions_A)
html_B = make_variant(also_B, 35, regions_B)

# sanity: story counts
for name, h, total in (('A', html_A, 42), ('B', html_B, 35)):
    heroes = len(re.findall(r'<div class="hero">', h))
    mids = len(re.findall(r'<div class="mid">', h))
    also = len(re.findall(r'<div class="alsoitem">', h))
    assert heroes + mids + also == total, (name, heroes, mids, also, total)
    nums = [int(x) for x in re.findall(r'<span class="num">(\d+)</span>', h)]
    nos = [int(x) for x in re.findall(r'<span class="no">(\d+)</span>', h)]
    assert nums == list(range(1, 14)), (name, 'hero/mid nums', nums)
    assert nos == list(range(14, total + 1)), (name, 'also nums', nos)
    print(f'variant {name}: heroes={heroes} mids={mids} also={also} total={total} OK')

open(OUT_A, 'w').write(html_A)
open(OUT_B, 'w').write(html_B)
print('wrote', OUT_A, len(html_A), 'bytes')
print('wrote', OUT_B, len(html_B), 'bytes')
