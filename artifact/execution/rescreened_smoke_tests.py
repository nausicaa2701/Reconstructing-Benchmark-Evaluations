#!/usr/bin/env python3
"""Replay CPU-only scorer smoke tests for the four post-freeze additions."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time


CASES = {
    "MMTU": r'''import json,pandas as pd
from evaluators.tableqa_evaluator import TQAEvaluator
raw=pd.DataFrame([
 {"metadata":json.dumps({"dataset":"synthetic","tag":"v1","note":"cpu-smoke","label":"42"}),"prompt":"q","response":"{\"answer\": \"42\"}"},
 {"metadata":json.dumps({"dataset":"synthetic","tag":"v1","note":"cpu-smoke","label":"42"}),"prompt":"q","response":"{\"answer\": \"0\"}"}])
avg,_,_=TQAEvaluator().evaluate(raw,n_jobs=1)
print(json.dumps({"score":float(avg.acc.iloc[0]),"records":2}))
assert avg.acc.iloc[0]==0.5''',
    "tapilot_code": r'''import importlib.util,json,tempfile,pathlib
spec=importlib.util.spec_from_file_location("ecg","eval/eval_code_gen.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
root=pathlib.Path(tempfile.mkdtemp())/"normal_case"; (root/"pred_result").mkdir(parents=True)
(root/"pred_result"/"x.txt").write_text("prediction")
(root/"meta_data.json").write_text(json.dumps({"result_type":"number"}))
(root/"eval.py").write_text("print(0.75)\n")
results,scores,n=m.eval_main({str(root):"schema-valid-synthetic"},"pred_code.py","base","cpu-smoke","None")
print(json.dumps({"results":results,"scores":scores,"records":n}))
assert results==["True"] and scores==[1] and n==1''',
    "databench_eval": r'''import sys,types,json
d=types.ModuleType("datasets"); d.Dataset=dict; d.load_dataset=lambda *a,**k: None; sys.modules["datasets"]=d
from databench_eval.eval import Evaluator
qa={"answer":["C","C"],"type":["category","category"],"sample_answer":["C","C"]}
score=Evaluator(qa=qa).eval(["C","A"])
print(json.dumps({"score":score,"records":2}))
assert score==0.5''',
    "sciencebenchmark_dataset": r'''import json,pathlib
files=list(pathlib.Path(".").glob("*/*.json")); [json.load(open(p)) for p in files]
evaluators=list(pathlib.Path(".").glob("**/*eval*"))
print(json.dumps({"valid_json_files":len(files),"evaluator_files":len(evaluators)}))
assert len(files)==12 and not evaluators''',
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True,
                        help="Directory containing MMTU, tapilot_code, databench_eval, and sciencebenchmark_dataset clones")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = {}
    for name, code in CASES.items():
        repo = args.repo_root / name
        env = os.environ.copy()
        if name == "databench_eval":
            env["PYTHONPATH"] = str(repo / "src")
        started = time.perf_counter()
        run = subprocess.run([sys.executable, "-c", code], cwd=repo, env=env,
                             text=True, capture_output=True)
        results[name] = {
            "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(),
            "returncode": run.returncode,
            "runtime_s": round(time.perf_counter() - started, 4),
            "stdout": run.stdout.strip(),
            "stderr": run.stderr.strip(),
        }
        if run.returncode:
            raise SystemExit(f"{name} failed:\n{run.stderr}")
    text = json.dumps({"audit_date": "2026-07-16", "hardware": "CPU-only", "results": results}, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
