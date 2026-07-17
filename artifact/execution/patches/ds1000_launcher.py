# Minimal-repair launcher for DS-1000: the sandbox blocks ProcessPoolExecutor
# (os.sysconf SC_SEM_NSEMS_MAX -> PermissionError). We substitute a SERIAL executor
# (env shim; the scoring logic in execution.check_correctness is unchanged) and bound
# to a smoke-test slice of 50 problems. No repo source file is edited.
import concurrent.futures as cfuts, sys, json, gzip
class _SerialFut:
    def __init__(self,r): self._r=r
    def result(self): return self._r
class SerialExecutor:
    def __init__(self,*a,**k): pass
    def __enter__(self): return self
    def __exit__(self,*a): return False
    def submit(self,fn,*a,**k): return _SerialFut(fn(*a,**k))
cfuts.ProcessPoolExecutor=SerialExecutor
def _as_completed(fs,total=None): return list(fs)
cfuts.as_completed=_as_completed
import test_ds1000 as T
T.ds1000 = T.ds1000[:50]   # smoke-test slice
gen=[json.loads(l) for l in open("data/gpt-4o-2024-08-06-answers.jsonl").readlines()][:200]
answers=[T.postprocess(l['code']) for l in gen]
print(T.eval_ds1000(answers))
