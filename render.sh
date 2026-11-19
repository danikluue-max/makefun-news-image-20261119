#!/bin/sh
# Render page.html to the 1024x1024 entry.png for news-image-20261119.
#
# How it works, in plain terms: open the page in headless Chromium and
# take a screenshot, then trim the capture down to the top 1024x1024
# square with Pillow. The page itself is exactly 1024px tall, so the
# crop only removes whatever extra strip the browser window adds below
# it. The browser is the Playwright Chromium on this machine unless
# $CHROME points somewhere else. No network is needed: all fonts come
# from the system fontconfig set and every picture is inline SVG.
#
# Usage: ./render.sh   (run from this directory; writes entry.png here)

set -eu

DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$DIR"

BROWSER="${CHROME:-$HOME/.cache/ms-playwright/chromium-1148/chrome-linux/chrome}"

# Headless Chrome's viewport ends up a little shorter than the window
# height, so ask for a taller window and crop back to the square.
CAPTURE=$(mktemp --suffix=.png /tmp/ni19-capture-XXXXXX)

"$BROWSER" \
  --headless=new \
  --no-sandbox \
  --disable-gpu \
  --hide-scrollbars \
  --force-device-scale-factor=1 \
  --virtual-time-budget=5000 \
  --window-size=1024,1111 \
  --screenshot="$CAPTURE" \
  "file://$DIR/page.html"

python3 - "$CAPTURE" "$DIR/entry.png" <<'PYEOF'
import sys
from PIL import Image

capture_path, out_path = sys.argv[1], sys.argv[2]
with Image.open(capture_path) as shot:
    print("captured size:", shot.size)
    square = shot.crop((0, 0, 1024, 1024))
    square.save(out_path)
with Image.open(out_path) as finished:
    print("entry size:", finished.size, "->", out_path)
PYEOF

rm -f "$CAPTURE"
