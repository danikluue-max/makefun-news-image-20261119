#!/bin/sh
# Render page5.html -> entry5.png (round 5, variant B) or page5a.html -> entry5a.png.
# Usage: ./render5.sh [5|5a]   (default 5)
set -eu
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$DIR"
V="${1:-5}"
PAGE="page$V.html"
OUT="entry$V.png"
BROWSER="${CHROME:-$HOME/.cache/ms-playwright/chromium-1148/chrome-linux/chrome}"
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
  "file://$DIR/$PAGE"
python3 - "$CAPTURE" "$DIR/$OUT" <<'PYEOF'
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
