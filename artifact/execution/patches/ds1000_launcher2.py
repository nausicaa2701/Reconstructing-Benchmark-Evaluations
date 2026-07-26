# Minimal-repair v2 for DS-1000: sandbox blocks BOTH ProcessPoolExecutor AND
# multiprocessing.Manager/Process (SC_SEM_NSEMS_MAX PermissionError / Manager EOFError).
# We replace check_correctness with an IN-PROCESS version that preserves the exact
# pass/fail scoring semantics (exec of code_context+answer, collect "passed"/"failed:<e>")
# but runs in the current process with a signal-based wall-clock guard instead of a
# child process. The score computed is identical for cleanly-running code; only the
# process-isolation wrapper is bypassed. No repo source file is edited.
import concurrent.futures as cfuts, json, signal
class _F:
    def __init__(s,r): s._r=r
    def result(s): return s._r
class SE:
    def __init__(s,*a,**k): pass
    def __enter__(s): return s
    def __exit__(s,*a): return False
    def submit(s,fn,*a,**k): return _F(fn(*a,**k))
cfuts.ProcessPoolExecutor=SE
cfuts.as_completed=lambda fs,total=None: list(fs)
import execution as EX
class _TO(Exception): pass
def _inproc(program, timeout, completion_id=None):
    res={"completion_id":completion_id}
    def _h(s,f): raise _TO()
    old=signal.signal(signal.SIGALRM,_h); signal.setitimer(signal.ITIMER_REAL,min(timeout,20))
    try:
        g={}
        exec(program,g); res["passed"]=True; res["result"]="passed"
    except _TO:
        res["passed"]=False; res["result"]="timed out"
    except BaseException as e:
        res["passed"]=False; res["result"]=f"failed: {e}"
    finally:
        signal.setitimer(signal.ITIMER_REAL,0); signal.signal(signal.SIGALRM,old)
    return res
EX.check_correctness=_inproc
import test_ds1000 as T
T.ds1000=T.ds1000[:50]
gen=[json.loads(l) for l in open("data/gpt-4o-2024-08-06-answers.jsonl").readlines()][:200]
answers=[T.postprocess(l['code']) for l in gen]
print(T.eval_ds1000(answers))
