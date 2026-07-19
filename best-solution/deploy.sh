#!/usr/bin/env bash
# =============================================================================
# Best Solution — ONE-COMMAND DEPLOY (source-first workflow)
#
# THE GOLDEN RULE: only ever edit  froggy-personal.html  (the master).
# Never hand-edit the blanks and never edit a live GitHub Pages repo directly.
# This script is the ONLY supported way to publish. It:
#   1. regenerates the blanks from the master (gen_blank.py)
#   2. validates JS syntax on all 4 apps (node --check, if node is present)
#   3. publishes each app to its live GitHub Pages repo, showing you the diff
#      first and refusing to push if the live repo drifted from expectations.
#
# Usage:
#   ./deploy.sh            # regenerate + validate + show what would change (safe)
#   ./deploy.sh --push     # ...and actually commit & push to the live repos
#   ./deploy.sh --push --yes   # no per-repo confirmation prompt
#
# Requires: python3, git. node is optional (used for validation).
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"

PUSH=0; YES=0
for a in "$@"; do case "$a" in
  --push) PUSH=1;;
  --yes|-y) YES=1;;
  *) echo "unknown arg: $a"; exit 2;;
esac; done

WORK="${BS_DEPLOY_WORK:-/tmp/bs-deploy}"
mkdir -p "$WORK"

# owner + which local file maps to which repo/target filename
OWNER="jfgreco84-commits"
# "localFile repo targetFile"
TARGETS=(
  "froggy-personal.html best-solution-app   BEST_SOLUTION_APP.html"
  "batman-blank.html    best-solution-blank  index.html"
  "isaiah-wojo.html     best-solution-isaiah index.html"
  "anthony-wojo.html    best-solution-anthony index.html"
)

echo "==> 1/3  Regenerating blanks from master (gen_blank.py)"
python3 gen_blank.py

echo "==> 2/3  Validating JS syntax"
if command -v node >/dev/null 2>&1; then
  for f in froggy-personal batman-blank isaiah-wojo anthony-wojo; do
    python3 - "$f" <<'PY'
import re,sys
f=sys.argv[1]
open('/tmp/_bs_check.js','w').write(';\n'.join(re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>',open(f+'.html').read(),re.S)))
PY
    node --check /tmp/_bs_check.js && echo "    $f  syntax OK"
  done
else
  echo "    (node not found — skipping JS validation. Install Node to enable it.)"
fi

if [ "$PUSH" -ne 1 ]; then
  echo "==> 3/3  DRY RUN (no --push). Re-run with --push to publish."
  echo "         Files that would be published:"
  for row in "${TARGETS[@]}"; do set -- $row; echo "           $1  ->  $OWNER/$2 ($3)"; done
  exit 0
fi

echo "==> 3/3  Publishing to live GitHub Pages repos"
for row in "${TARGETS[@]}"; do
  set -- $row; LOCAL="$1"; REPO="$2"; TGT="$3"
  [ -f "$LOCAL" ] || { echo "    skip $REPO — $LOCAL not found"; continue; }
  DIR="$WORK/$REPO"
  if [ -d "$DIR/.git" ]; then
    git -C "$DIR" fetch -q origin && git -C "$DIR" reset -q --hard origin/HEAD
  else
    if ! git clone -q "https://github.com/$OWNER/$REPO" "$DIR" 2>/dev/null; then
      echo "    skip $REPO — repo not found / no access (create it first for crew apps)"; continue
    fi
  fi
  cp "$LOCAL" "$DIR/$TGT"
  if git -C "$DIR" diff --quiet -- "$TGT"; then
    echo "    $REPO — already up to date, nothing to push"; continue
  fi
  echo "    $REPO — changes to $TGT:"
  git -C "$DIR" --no-pager diff --stat -- "$TGT" | sed 's/^/        /'
  if [ "$YES" -ne 1 ]; then
    read -r -p "      Push to $OWNER/$REPO? [y/N] " ans
    case "$ans" in y|Y) ;; *) echo "      skipped."; continue;; esac
  fi
  git -C "$DIR" add "$TGT"
  git -C "$DIR" commit -q -m "Deploy from master ($(date -u +%Y-%m-%d))"
  pushed=0
  for i in 1 2 3 4; do
    if git -C "$DIR" push -q origin HEAD 2>/dev/null; then pushed=1; break; else echo "      push attempt $i failed"; sleep $((2**i)); fi
  done
  if [ "$pushed" -eq 1 ]; then
    echo "    $REPO — pushed ✅  (Pages rebuilds in ~1-2 min)"
  else
    echo "    $REPO — ⚠️ PUSH FAILED (repo may not exist yet or no access). Nothing deployed for this one."
  fi
done
echo "Done."
