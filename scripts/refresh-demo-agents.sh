#!/usr/bin/env bash
# Copies the demo agents from s2oserver into the website, ready to commit.
#
#   scripts/refresh-demo-agents.sh
#
# html/demo-agents.json       <- s2oserver docs/demo/agents.json (the list demo-agents.html draws)
# html/demo-agents/*.jsonc    <- s2oserver docs/demo/definitions/*.jsonc (the "Show source" files)
#
# The definitions folder is mirrored: a .jsonc that no longer exists in s2oserver is removed here.
# S2OSERVER overrides the location of the s2oserver checkout.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER="${S2OSERVER:-$ROOT/../s2oserver}"
SOURCE="$SERVER/docs/demo"
HTML="$ROOT/html"

[ -f "$SOURCE/agents.json" ] || { echo "Not found: $SOURCE/agents.json (set S2OSERVER)" >&2; exit 1; }
[ -d "$SOURCE/definitions" ] || { echo "Not found: $SOURCE/definitions" >&2; exit 1; }

cp "$SOURCE/agents.json" "$HTML/demo-agents.json"
rsync -a --delete --itemize-changes --include "*.jsonc" --exclude "*" \
    "$SOURCE/definitions/" "$HTML/demo-agents/"

echo
echo "Changes to commit:"
git -C "$ROOT" status --short -- html/demo-agents.json html/demo-agents
