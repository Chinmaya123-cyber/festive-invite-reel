#!/usr/bin/env bash
# Scaffold a new invite project from the template.
#   bash new_invite.sh ~/Downloads/my-diwali-invite
set -euo pipefail
SK="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:?usage: new_invite.sh <project-dir>}"
if [ -e "$DEST" ]; then echo "already exists: $DEST" >&2; exit 1; fi
cp -R "$SK/template" "$DEST"
mkdir -p "$DEST/refs" "$DEST/out" "$DEST/art/raw"
if [ ! -d "$SK/node_modules/playwright" ]; then (cd "$SK" && npm install --silent && npx playwright install chromium >/dev/null); fi
cat > "$DEST/mix.json" <<'EOF'
{
  "intro": {"file": "refs/intro.wav", "end": 11.905, "fade": 0.07},
  "main":  {"file": "refs/main.wav", "hit": 0.064, "segments": [[0, null]]},
  "cut_at": 11.90,
  "out": "audio/mix.wav",
  "timing": "timing.json"
}
EOF
echo "project: $DEST"
echo "stills:  node $SK/scripts/render.mjs $DEST --stills"
echo "render:  node $SK/scripts/render.mjs $DEST --workers 6"
