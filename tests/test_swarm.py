"""Tests for the agent-swarm harness: vote parsing, tally, rendering, init. No bus, no network.

Run: python tests/test_swarm.py  (from the skill folder, or anywhere)
"""

import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SKILL, "scripts"))

import swarm  # noqa: E402

FAILURES = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


# vote parsing: markdown noise, missing keys, confidence letter
body = """**Independent lane** summary

VOTE WORK=cre-uk-intel-decision-tool
**VOTE COMPANY**: usage-ledger+approvals
VOTE A = `neither`
CHANGED=yes: moved COMPANY after reading the matrix
CONFIDENCE=M

reasoning follows...
"""
v = swarm.parse_votes(body, ["WORK", "COMPANY", "A", "D"])
check("vote plain", v["WORK"] == "cre-uk-intel-decision-tool")
check("vote bold key", v["COMPANY"] == "usage-ledger+approvals")
check("vote backticks", v["A"] == "neither")
check("vote missing", v["D"] == "(missing)")
check("changed line", v["changed"].startswith("yes: moved COMPANY"))
check("confidence", v["confidence"] == "M")

# tally ignores undelivered lanes and normalises on the first token, lowercase
index = {
    "a": {"delivered": True, "votes": {"WORK": "cre-uk-intel-decision-tool", "COMPANY": "usage-ledger+approvals"}},
    "b": {"delivered": True, "votes": {"WORK": "Cre-uk-intel-decision-tool (second)", "COMPANY": "other:usage-ledger-probe"}},
    "c": {"delivered": False},
}
t = swarm.tally(index, ["WORK", "COMPANY"])
check("tally work", t["WORK"] == {"cre-uk-intel-decision-tool": 2})
check("tally company", t["COMPANY"] == {"usage-ledger+approvals": 1, "other:usage-ledger-probe": 1})

# rendering: tokens replaced, unknown tokens left visible, no stray braces from JSON-like text
text = swarm.render("lane-prompt-r1.md", {"agent": "oc-x", "model": "m", "token": "t", "task_id": 7,
                                           "workspace": "W", "lead_agent": "claude", "sync_script": "S"})
check("render replaces tokens", "--agent oc-x --session t" in text and "thread 7" in text)
check("render no unknown tokens left", "{{" not in text)
r2 = swarm.render("task-r2.md", {"task_id_r1": 3, "round1_dir": "R1", "matrix_path": "M", "vote_keys": "WORK, COMPANY",
                                  "lead_agent": "claude"})
check("render r2 vote keys", "VOTE WORK, COMPANY" in r2 and "R1" in r2)

# bus text parsers
room = """Agent lanes:
- claude (lead): online/responsive/available session=active
- oc-gpt-sol (Read-only lane): online/idle/available session=active
- oc-claude-opus: not-joined/not_joined/available session=unfenced
- codex-map (x): offline/offline/available session=ended
"""
check("joined_agents", swarm.joined_agents(room) == {"claude", "oc-gpt-sol", "codex-map"})
check("lane_states", swarm.lane_states(room) == {"claude": "online", "oc-gpt-sol": "online",
                                                   "oc-claude-opus": "not-joined", "codex-map": "left"})
inbox = """Completed tasks you assigned:
- #25 claude -> oc-gpt-astra: done by oc-gpt-astra - Independent
- #26 claude -> oc-gpt-sol: done by oc-gpt-sol - INDEPENDENT
"""
check("delivered_task_ids", swarm.delivered_task_ids(inbox) == {25, 26})

# init in a temp workspace: no bus touched
tmp = tempfile.mkdtemp(prefix="swarm-test-")
task = os.path.join(tmp, "task.md")
open(task, "w", encoding="utf-8").write("Q1. Pick one.\n")


class A:  # minimal argparse stand-in
    workspace = tmp; run = "demo"; task = task; roster = "default.json"; lead_agent = "claude"
    lead_session = None; sync_script = os.path.join(tmp, "agent_sync.py"); marker = None; vote_keys = "X,Y"


import io  # noqa: E402
from contextlib import redirect_stdout  # noqa: E402
buf = io.StringIO()
with redirect_stdout(buf):
    swarm.cmd_init(A)
run_dir = os.path.join(tmp, "swarm-runs", "demo")
run = json.load(open(os.path.join(run_dir, "run.json"), encoding="utf-8"))
check("init creates run.json", run["name"] == "demo" and run["vote_keys"] == ["X", "Y"])
check("init lanes from roster", len(run["lanes"]) == 5 and all("token" in l for l in run["lanes"]))
check("init runners", {l["runner"] for l in run["lanes"]} == {"opencode", "subagent"})
check("init copies task", os.path.isfile(os.path.join(run_dir, "task-r1.md")))
check("init dirs", all(os.path.isdir(os.path.join(run_dir, d)) for d in ("prompts", "logs", "round1", "round2")))

print()
if FAILURES:
    print(f"{len(FAILURES)} failure(s): {FAILURES}")
    sys.exit(1)
print("all agent-swarm tests passed")
