// Entry program for news-image-20261119, round 2 (Node 22, standard library only).
// Round 2 rebuilds the page on the winning structure: a light cream newspaper
// front page, 1024x1024, with 42 verified stories — 3 hero cards with large
// drawn scenes (Shenzhen trilateral summit, GTA VI's release, Anthropic's
// record $81.3bn IPO), 12 mid cards with small drawings (the ICJ's 9-6 Myanmar
// genocide verdict, Iran's Gulf retaliation, the Kerch Bridge collapse, Cyclone
// Akvan, COP31, Florida floods and more), a region bar, a 7-number strip, a
// day-by-hours timeline, a small world map with 9 pinned places, a 27-item
// ALSO list, a THE VERDICT box, a confidence legend and a DATE CHECK strip.
// The image is entry.png beside this file; the program copies it to
// /output/entry.png, where the judge reads exactly those bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
