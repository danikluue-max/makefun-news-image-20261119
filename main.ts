// Entry program for news-image-20261119, round 1 (Node 22, standard library only).
// Round 1 is the first attempt at "Sum up 19 November's world news in one image":
// a light cream newspaper front page, 1024x1024, with 40 verified stories —
// 6 lead cards with drawn photo-style SVG scenes (Shenzhen trilateral summit,
// Anthropic's record $81.3bn IPO, the ICJ Myanmar ruling with NO outcome stated,
// GTA VI's release, Iran's Gulf retaliation, Israel's Gaza ground operation),
// a small world map with 8 pinned places, field bars that sum to 40, and a
// 34-item ALSO list. The image is entry.png beside this file; the program
// copies it to /output/entry.png, where the judge reads exactly those bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
