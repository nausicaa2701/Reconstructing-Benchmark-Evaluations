#!/usr/bin/env bash
# Run after freeing disk space if git mmap fails.
#   cd /Users/nausicaa/Documents/GitHub/reconstructing-benchmark-evaluations
#   bash finish_release.sh
set -euo pipefail
cd "$(dirname "$0")"

rm -rf artifact/llm_judges/work
grep -q 'artifact/llm_judges/work/' .gitignore || echo 'artifact/llm_judges/work/' >> .gitignore

python3 artifact/reproduce.py --check
python3 tools/build_release_manifest.py --verify

git add -A
git status --short

git commit -F COMMIT_MESSAGE.txt

echo ""
echo "Committed. Next (manual):"
echo "  git tag -a v1.0.0 -m 'KDD 2027 artifact; audit frozen 2026-07-13; released 2026-07-26'"
echo "  git push origin main --tags"
echo "  GitHub Settings -> Change visibility -> Public"
