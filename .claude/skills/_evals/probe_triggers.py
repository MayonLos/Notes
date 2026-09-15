import json, subprocess, os, sys, time
from concurrent.futures import ThreadPoolExecutor

T = "/tmp/claude-1000/-home-mayon-Vaults/skilltest"
QS = json.load(open("/home/mayon/Vaults/.claude/skills/_evals/queries.json", encoding="utf-8"))
KNOWN = {"note", "query", "review", "lint"}
env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

def probe(item):
    """跑一条 query，返回它第一个选中的 skill（没选就是 None）。抓到即掐断。"""
    p = subprocess.Popen(
        ["claude", "-p", item["q"], "--output-format", "stream-json", "--verbose",
         "--disallowedTools", "Write,Edit,NotebookEdit,Bash,Task"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=T, env=env, text=True)
    picked, t0 = None, time.time()
    try:
        for line in p.stdout:
            if time.time() - t0 > 120:
                break
            try:
                e = json.loads(line)
            except Exception:
                continue
            if e.get("type") != "assistant":
                continue
            for c in e.get("message", {}).get("content", []):
                if c.get("type") == "tool_use" and c["name"] == "Skill":
                    picked = c.get("input", {}).get("skill")
                    break
                # 用了别的工具却没先选 skill —— 视为「不触发 skill，直接答」
                if c.get("type") == "tool_use":
                    picked = picked or "(直接用工具)"
            if picked:
                break
    finally:
        p.kill(); p.wait()
    base = (picked or "").split(":")[-1]
    return {**item, "picked": base if base in KNOWN else (picked or "none")}

with ThreadPoolExecutor(max_workers=6) as ex:
    res = list(ex.map(probe, QS))

json.dump(res, open("/home/mayon/Vaults/.claude/skills/_evals/real-trigger.json", "w"),
          ensure_ascii=False, indent=1)

ok = sum(1 for r in res if r["picked"] == r["owner"])
print(f"\n准确率：{ok}/{len(res)}\n")
print(f"{'期望':<7}{'实际':<14}{'查询'}")
print("-" * 76)
for r in res:
    flag = "✓" if r["picked"] == r["owner"] else "✗"
    print(f"{flag} {r['owner']:<6}{r['picked']:<14}{r['q'][:40]}")
