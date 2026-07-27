#!/usr/bin/env bash
# Commit, tag and archive the artifact release.
#
#   cd /Users/nausicaa/Documents/GitHub/reconstructing-benchmark-evaluations
#   bash finish_release.sh
#
# ORDER MATTERS for the DOI. Zenodo's GitHub webhook only archives releases
# published AFTER the repository toggle is switched on, and it only fires on a
# GitHub *Release*, not on a bare git tag. The tag v1.0.0 currently points at a
# commit that predates the human study, the golden fixtures and the
# official-environment runs, so it must be moved before it means anything.
set -euo pipefail
cd "$(dirname "$0")"

rm -rf artifact/llm_judges/work

# 1. Integrity gates. Both must pass before anything is tagged.
python3 artifact/reproduce.py --check
python3 tools/build_release_manifest.py --verify

git add -A
git status --short
git commit -F COMMIT_MESSAGE.txt

cat <<'NEXT'

Committed. The remaining steps are manual and order-dependent:

  1. Make the repository public
       GitHub -> Settings -> General -> Danger Zone -> Change visibility
     Then verify anonymously, which is the exact test the reviewer ran:
       curl -sI -o /dev/null -w '%{http_code}\n' \
         https://github.com/nausicaa2701/reconstructing-benchmark-evaluations
     Expect 200. A 404 here means the paper's accessibility claim is still false.

  2. Enable Zenodo BEFORE publishing the release
       https://zenodo.org -> log in with GitHub -> GitHub tab
       -> flip the toggle for this repository ON
     Zenodo ignores anything released while the toggle was off.

  3. Move the stale tag, then publish a GitHub Release from it
       git tag -d v1.0.0
       git push origin :refs/tags/v1.0.0
       git tag -a v1.0.0 -m 'KDD 2027 artifact; audit frozen 2026-07-13; released 2026-07-27'
       git push origin main --tags
     Then GitHub -> Releases -> Draft a new release -> choose tag v1.0.0
     -> Publish. Publishing is what fires the Zenodo webhook.

  4. Collect the VERSION DOI (not the concept DOI) from the Zenodo record and
     put it in three places:
       - CITATION.cff        (uncomment the identifiers block, fill both DOIs)
       - .zenodo.json        (nothing to do; Zenodo assigns it)
       - the paper           (replace \TBA{artifact DOI} in sections/00-abstract.tex)

  5. Re-verify from a clean clone on a different machine or an empty directory:
       git clone https://github.com/nausicaa2701/reconstructing-benchmark-evaluations
       cd reconstructing-benchmark-evaluations
       python3 artifact/reproduce.py --check
       python3 tools/build_release_manifest.py --verify

  6. Recompile the paper after the DOI edit; main.pdf's SHA-256 changes, so
     rebuild the manifest and amend the release if you want the pinned hash to
     match the submitted PDF:
       python3 tools/build_release_manifest.py --version v1.0.0 \
         --paper-sha256 $(shasum -a 256 ../KDD2027/main.pdf | cut -d' ' -f1)

NEXT
