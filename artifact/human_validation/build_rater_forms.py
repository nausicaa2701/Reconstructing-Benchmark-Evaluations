#!/usr/bin/env python3
"""Render a self-contained Markdown coding form for each human rater.

The form mirrors assignments/coder_{A,B}.csv one-to-one, in the same shuffled
order, so a completed form can be merged back with ingest_rater_forms.py and
analysed by analyze_labels.py.  Evidence excerpts are embedded so a rater never
has to open the JSON bundle, and benchmark identity is withheld to match the
pseudonymous packets the model judges received.
"""
from __future__ import annotations

import csv
import json
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARTIFACT = ROOT / "artifact"
LABELS = [
    ("documented-and-verifiable",
     "Public evidence states this and you can verify it in the packet."),
    ("partially-documented",
     "Some of it is stated but a bounded gap remains that you would have to guess."),
    ("claimed-but-not-verifiable",
     "The release asserts it exists but the packet does not let you confirm it."),
    ("not-documented",
     "You searched the packet and found no statement of this."),
    ("not-applicable",
     "The criterion does not apply to this kind of evaluation."),
    ("access-blocked",
     "Evidence is behind credentials, a dead link, or a gated service."),
]
CRITERION_GUIDE = {
    "Input/expected-output schema":
        "Could you write a file that this evaluator accepts, and do you know "
        "exactly what it returns? Field names, types, and file format count.",
    "Metric definition":
        "Is the metric named AND defined precisely enough to reimplement? "
        "'Accuracy' alone is partial unless what counts as correct is stated.",
    "Grading rules & tie-breaking":
        "What happens on ties, empty predictions, malformed output, timeouts, "
        "or partially correct answers? Silence on all of these is not-documented.",
    "Predictions->aggregate-score mapping":
        "How do per-item results become the single reported number? Mean over "
        "what denominator, weighted how, excluding what?",
    "Evaluator implementation available":
        "Is the code implementing THIS evaluation present and identifiable in "
        "the artifacts? Scoring buried in a training loop is not the same as "
        "an identifiable evaluator.",
    "Sample predictions / trajectories":
        "Is there at least one concrete example of model output in the format "
        "the evaluator consumes?",
}
INSTRUCTIONS = """\
# R2 Human Coding Form — Rater {coder}

You are coding **156 items**. Each item is one benchmark release paired with one
evaluation criterion. Work through them in the order given; the order is
deliberately shuffled so that you judge each criterion on its own evidence
rather than forming an impression of a release and carrying it across criteria.

## The question you are answering

For each item: **based only on the evidence packet, could an independent
researcher reconstruct this aspect of the evaluation without guessing?**

You are not judging whether the benchmark is good, whether its authors did
careful work, or whether the evaluation is sound. You are judging what the
public artifacts state.

## Rules

1. **Use only the evidence packet.** Do not search GitHub, the paper, or the
   web. If evidence is not in the packet, it is not available to you. This
   matches the constraint the model judges worked under.
2. **Do not discuss items with the other rater** until both forms are frozen.
3. **Do not look at** `artifact/audit/raw_labels/` or any model output. If you
   have already seen model labels for a release, say so now — you cannot rate
   it.
4. **Every item needs an evidence pointer**: a file path, section heading, or
   line range from the packet. For `not-documented`, the pointer is where you
   looked (`README.md, evaluate.py — no grading section`).
5. **Do not leave blanks.** If you genuinely cannot decide, pick the more
   conservative label and say why in the note. The analysis refuses blank cells.
6. Expect this to take **3–5 hours**. Split it across sessions; do not rush the
   last 40 items.

## The six labels

{labels}

## The hardest boundary

`partially-documented` vs `not-documented` drives the whole study, so be
deliberate here:

- **partially-documented** — you could get to a working reconstruction with one
  bounded, clearly-scoped assumption you could state in a sentence.
- **not-documented** — you would have to invent the behaviour, or you would
  need several assumptions, or you cannot tell which of two plausible
  behaviours the release means.

If you find yourself writing "probably it means…", that is `not-documented`.

## Evidence packets

Packets are in `artifact/audit/evidence/r2_evidence_bundles.json`, keyed by the
packet ID shown on each item. Each packet contains the release's README and its
evaluation-related source files at a frozen commit. Open it with:

```bash
python artifact/human_validation/show_packet.py <PACKET_ID>
```

Releases are identified only by packet ID. If you recognise a release from its
content, that is fine and expected — do not go looking for its name.

## How to fill this in

Edit this file directly. For each item, fill the three fields. Leave the
structure exactly as it is — the ingest script parses these markers.

When finished:

```bash
python artifact/human_validation/ingest_rater_forms.py
python artifact/human_validation/analyze_labels.py
```

---
"""


def load_packet_index() -> dict:
    bundles = json.loads(
        (ARTIFACT / "audit/evidence/r2_evidence_bundles.json").read_text(encoding="utf-8"))
    index = {}
    for position, name in enumerate(sorted(bundles), 1):
        bundle = bundles[name]
        index[name] = {
            "packet_id": f"PKT-{position:02d}",
            "commit": bundle.get("commit", ""),
            "readme_path": bundle.get("readme_path", ""),
            "eval_files": sorted((bundle.get("eval_files") or {}).keys()),
        }
    return index


def render(coder: str, index: dict) -> Path:
    rows = list(csv.DictReader(
        (HERE / "assignments" / f"coder_{coder}.csv").open(newline="", encoding="utf-8")))
    labels = "\n".join(f"- `{name}` — {gloss}" for name, gloss in LABELS)
    parts = [INSTRUCTIONS.format(coder=coder, labels=labels)]
    for row in rows:
        meta = index[row["benchmark"]]
        criterion = row["criterion"]
        files = ", ".join(f"`{path}`" for path in meta["eval_files"][:8]) or "(none in packet)"
        if len(meta["eval_files"]) > 8:
            files += f", and {len(meta['eval_files']) - 8} more"
        guide = textwrap.fill(CRITERION_GUIDE[criterion], 76)
        parts.append(f"""\
## {row['assignment_id']} — {criterion}

**Packet:** `{meta['packet_id']}` · commit `{meta['commit'][:12]}`
**Packet contains:** `{meta['readme_path']}`, {files}

> {guide}

- **Label:**
- **Evidence pointer:**
- **Note:**

---
""")
    out = HERE / f"rater_form_{coder}.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    return out


def main() -> None:
    index = load_packet_index()
    (HERE / "packet_key.json").write_text(
        json.dumps({meta["packet_id"]: name for name, meta in index.items()},
                   indent=2) + "\n", encoding="utf-8")
    paths = [render(coder, index) for coder in ("A", "B")]
    print("wrote " + ", ".join(str(path.relative_to(ROOT)) for path in paths))
    print("packet key written to artifact/human_validation/packet_key.json "
          "(do not share with raters until both forms are frozen)")


if __name__ == "__main__":
    main()
