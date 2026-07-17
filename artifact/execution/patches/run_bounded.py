import subprocess, sys, time, os
# usage: run_bounded.py <cap_seconds> <logfile> <cwd> <cmd...>
# Establishes STANDARD CPython path semantics: script/cwd dir on sys.path.
# The sandbox exports PYTHONSAFEPATH=1 which suppresses this; we neutralize it
# uniformly for ALL benchmarks so first-pass behavior matches the documented
# `python <script>.py` invocation on a default interpreter (env config, not per-repo repair).
cap=int(sys.argv[1]); logf=sys.argv[2]; cwd=sys.argv[3]; cmd=sys.argv[4:]
env=dict(os.environ); env.pop("PYTHONSAFEPATH",None)
env["PYTHONPATH"]=cwd+((os.pathsep+env["PYTHONPATH"]) if env.get("PYTHONPATH") else "")
t0=time.time()
with open(logf,'a') as lf:
    lf.write(f"CMD: {' '.join(cmd)} (cwd={cwd}, cap={cap}s, std_path_semantics=on)\n--- output ---\n"); lf.flush()
    p=subprocess.Popen(cmd,cwd=cwd,stdout=lf,stderr=subprocess.STDOUT,env=env)
    try:
        p.wait(timeout=cap); ec=p.returncode; status="COMPLETED"
    except subprocess.TimeoutExpired:
        p.kill(); ec=124; status="CAP_EXCEEDED"
    dt=time.time()-t0
    lf.write(f"\nEXIT={ec}\nSTATUS={status}\nRUNTIME_S={dt:.2f}\n"); lf.flush()
print(f"EXIT={ec} STATUS={status} RUNTIME_S={dt:.2f}")
