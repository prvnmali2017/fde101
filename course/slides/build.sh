#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

BUILD_DIR="build"
THEME="theme/mlopsguru.css"
mkdir -p "$BUILD_DIR"

# Prefer a locally installed Marp CLI (reliable, offline); fall back to npx.
if [ -x "node_modules/.bin/marp" ]; then
  MARP="node_modules/.bin/marp"
else
  echo "Local Marp not found; installing (one-time)..."
  npm install --no-audit --no-fund @marp-team/marp-cli >/dev/null 2>&1
  MARP="node_modules/.bin/marp"
fi

# Decks: core chapters + bonus modules
declare -a SOURCES=(
  "../chapter-01-fde-role-mindset/courseware.md:ch01"
  "../chapter-02-discovery-scoping/courseware.md:ch02"
  "../chapter-03-rapid-prototyping/courseware.md:ch03"
  "../chapter-04-ai-llm-integration/courseware.md:ch04"
  "../chapter-05-deploy-demo-handoff/courseware.md:ch05"
  "../bonus-modules/aws/courseware.md:bonus-aws"
  "../bonus-modules/azure/courseware.md:bonus-azure"
  "../bonus-modules/gcp/courseware.md:bonus-gcp"
)

# Output format: html (default), pdf, or pptx
FORMAT="${1:-html}"

for entry in "${SOURCES[@]}"; do
  src="${entry%%:*}"
  name="${entry##*:}"
  if [ ! -f "$src" ]; then
    echo "skip (missing): $src"
    continue
  fi

  marp_md="$BUILD_DIR/$name.marp.md"
  python3 convert.py "$src" "$marp_md"

  out="$BUILD_DIR/$name.$FORMAT"
  echo "==> Rendering $name → $out"
  if [ "$FORMAT" = "html" ]; then
    "$MARP" --theme-set "$THEME" "$marp_md" -o "$out"
  else
    # PDF/PPTX need Chrome; allow override via CHROME_PATH
    "$MARP" --theme-set "$THEME" --"$FORMAT" --allow-local-files "$marp_md" -o "$out"
  fi
done

echo ""
echo "Done. Decks in $BUILD_DIR/ (format: $FORMAT)"
echo "Tip: ./build.sh pdf   or   ./build.sh pptx   (requires Chrome)"
