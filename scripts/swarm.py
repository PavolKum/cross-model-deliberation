"""agent-swarm: run a multi-model adjudication on the agent-sync bus in two rounds.

Round 1: every lane answers the same task independently (no peer access).
Round 2: every lane reads the agreement matrix and all round-1 answers, posts one
position note, replies once if challenged, and votes with a fixed VOTE block.
The facilitator (the Claude Code session running this) tallies and decides.

Lanes come in two runners:
  opencode  - launched by this script: `opencode run -m <model> --variant <v>` on a
              subscription-backed provider (OpenAI endpoint). Logged to the run dir.
  subagent  - Claude Code subagents on the Max plan. This script cannot spawn them;
              it writes one ready prompt per lane under prompts/ and the facilitator
              launches each with the Agent tool (model fable / opus / sonnet).

Subcommands (run from anywhere; --run is the run directory):
  init          create a run: workspace, name, task body, roster
  round1        post one bus task per lane, launch opencode lanes, write subagent prompts
  status        who joined, who delivered, for a round
  wait          block until every lane delivered a round (or timeout)
  collect       dump task-done bodies to roundN/<lane>.md; round 2 also parses votes
  round2        post debate+vote tasks, launch opencode lanes, write subagent prompts
  matrix-prompt print the matrix-builder prompt for an Opus subagent
  relaunch      relaunch one opencode lane for a round (after a silent death)

Stdlib only. One bus write per subprocess call. Never deletes anything.
"""

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
TEMPLATES = os.path.join(SKILL_DIR, "templates")
ROSTERS = os.path.join(SKILL_DIR, "rosters")
HOME = os.path.expanduser("~")
SYNC_DEFAULT = os.environ.get("AGENT_SYNC_SCRIPT") or os.path.join(HOME, "Tools", "Stack", "scripts", "agent_sync.py")

VOTE_KEYS = ("WORK", "COMPANY", "A")  # overridable per run via run.json["vote_keys"]


# ----------------------------------------------------------------------------- helpers

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def load_run(run_dir):
    with open(os.path.join(run_dir, "run.json"), encoding="utf-8") as f:
        return json.load(f)


def save_run(run_dir, run):
    with open(os.path.join(run_dir, "run.json"), "w", encoding="utf-8") as f:
        json.dump(run, f, indent=1)


def render(template_name, values):
    """Fill {{key}} tokens; unknown tokens are left visible so mistakes show."""
    with open(os.path.join(TEMPLATES, template_name), encoding="utf-8") as f:
        text = f.read()
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(values.get(m.group(1), m.group(0))), text)


def sync_cmd(run, *args):
    return ["python", run["sync_script"], "--agent", run["lead_agent"], "--session", run["lead_session"], *args]


def sync_run(run, *args, stdin_text=None):
    r = subprocess.run(sync_cmd(run, *args), input=stdin_text, capture_output=True, text=True,
                       cwd=run["workspace"], encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def ensure_joined(run):
    """Idempotent: a same-token join reacquires an expired lease."""
    rc, out = sync_run(run, "join", "--lease-ttl", "3600", f"{run['lead_agent']} swarm facilitator ({run['name']})")
    if rc != 0:
        log(f"WARNING join failed: {out.strip()[:200]}")


def post_task(run, agent, body):
    rc, out = sync_run(run, "task", "--stdin", agent, stdin_text=body)
    m = re.search(r"event (\d+) written", out)
    if rc != 0 or not m:
        raise SystemExit(f"task post failed for {agent}: {out.strip()[:300]}")
    return int(m.group(1))


def resolve_opencode():
    """Prefer the native executable: the npm .cmd shim trips the 8 KB command-line limit."""
    env = os.environ.get("AGENT_SWARM_OPENCODE_BIN")
    if env and os.path.isfile(env):
        return env
    npm = os.path.join(os.environ.get("APPDATA", ""), "npm", "node_modules", "opencode-ai", "bin", "opencode.exe")
    if os.path.isfile(npm):
        return npm
    found = shutil.which("opencode")
    if not found:
        raise SystemExit("opencode not found; set AGENT_SWARM_OPENCODE_BIN")
    return found


def lane_prompt_path(run_dir, lane, rnd):
    return os.path.join(run_dir, "prompts", f"{lane['agent']}-r{rnd}.md")


def lane_log_path(run_dir, lane, rnd):
    return os.path.join(run_dir, "logs", f"{lane['agent']}-r{rnd}.log")


def task_key(rnd):
    return f"task_id_r{rnd}"


def launch_opencode(run, run_dir, lane, rnd, prompt, use_variant=True):
    binary = resolve_opencode()
    cmd = [binary, "run", "-m", lane["model"]]
    if use_variant and lane.get("variant"):
        cmd += ["--variant", lane["variant"]]
    cmd += ["--auto", "--dir", run["workspace"], prompt]
    os.makedirs(os.path.dirname(lane_log_path(run_dir, lane, rnd)), exist_ok=True)
    fh = open(lane_log_path(run_dir, lane, rnd), "a", encoding="utf-8")
    fh.write(f"\n--- launch {datetime.now().isoformat()} variant={'on' if use_variant else 'off'}\n")
    fh.flush()
    flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    proc = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT, cwd=run["workspace"], creationflags=flags)
    log(f"launched {lane['agent']} pid={proc.pid} model={lane['model']} variant={'on' if use_variant else 'off'}")
    return proc


def room_text(run):
    _, out = sync_run(run, "room")
    return out


def inbox_text(run):
    _, out = sync_run(run, "inbox")
    return out


def lane_states(room):
    """{agent: 'online' | 'left' | 'not-joined'} from the room listing."""
    states = {}
    for line in room.splitlines():
        m = re.match(r"^- ([\w\-]+)(?: \(.*?\))?: (online|offline|not-joined)", line)
        if m:
            states[m.group(1)] = {"online": "online", "offline": "left"}.get(m.group(2), "not-joined")
    return states


def joined_agents(room):
    """Agents that have ever joined (online now, or joined and left)."""
    return {a for a, s in lane_states(room).items() if s in ("online", "left")}


def delivered_task_ids(inbox):
    return {int(m.group(1)) for m in re.finditer(r"^- #(\d+) [\w\-]+ -> [\w\-]+: done by", inbox, re.M)}


def lanes_for(run, runner=None):
    return [l for l in run["lanes"] if runner is None or l.get("runner") == runner]


def thread_body(run, task_id):
    _, out = sync_run(run, "thread", str(task_id))
    m = re.search(r"task-done -> task:\d+ \(completion of task \d+\): (.*)", out, re.S)
    return m.group(1).strip() if m else ""


def parse_votes(body, keys):
    votes = {}
    for key in keys:
        m = re.search(rf"VOTE\s+{re.escape(key)}\**\s*[=:]\s*\**\s*([^\n*]+)", body)
        votes[key] = m.group(1).strip().strip("`").strip() if m else "(missing)"
    changed = re.search(r"CHANGED\s*[=:]\s*\**\s*([^\n]+)", body)
    conf = re.search(r"CONFIDENCE\s*[=:]\s*\**\s*([HML])\b", body)
    votes["changed"] = changed.group(1).strip()[:200] if changed else "(missing)"
    votes["confidence"] = conf.group(1) if conf else "?"
    return votes


def tally(votes_by_lane, keys):
    out = {}
    for key in keys:
        counts = {}
        for v in votes_by_lane.values():
            if not v.get("delivered"):
                continue
            label = str(v["votes"].get(key, "(missing)")).split(" ")[0].lower()
            counts[label] = counts.get(label, 0) + 1
        out[key] = counts
    return out


# ----------------------------------------------------------------------------- subcommands

def cmd_init(args):
    workspace = os.path.abspath(args.workspace)
    run_dir = os.path.join(workspace, "swarm-runs", args.run)
    if os.path.exists(os.path.join(run_dir, "run.json")):
        raise SystemExit(f"run already exists: {run_dir}")
    roster_path = args.roster if os.path.isfile(args.roster) else os.path.join(ROSTERS, args.roster)
    with open(roster_path, encoding="utf-8") as f:
        roster = json.load(f)
    for sub in ("prompts", "logs", "round1", "round2"):
        os.makedirs(os.path.join(run_dir, sub), exist_ok=True)
    shutil.copyfile(args.task, os.path.join(run_dir, "task-r1.md"))
    stamp = datetime.now().strftime("%y%m%d%H%M")
    run = {
        "name": args.run,
        "workspace": workspace,
        "run_dir": run_dir,
        "created": datetime.now().isoformat(timespec="seconds"),
        "sync_script": os.path.abspath(args.sync_script),
        "lead_agent": args.lead_agent,
        "lead_session": args.lead_session or f"{args.lead_agent}-swarm-{stamp}",
        "marker": args.marker,
        "vote_keys": [k.strip() for k in args.vote_keys.split(",")] if args.vote_keys else list(VOTE_KEYS),
        "lanes": [dict(l, token=f"{l['agent']}-{stamp}") for l in roster["lanes"]],
    }
    save_run(run_dir, run)
    log(f"run created: {run_dir}")
    log(f"lanes: {[l['agent'] + ':' + l.get('runner', '?') for l in run['lanes']]}")
    print(run_dir)


def _write_subagent_prompt(run, run_dir, lane, rnd, values):
    path = lane_prompt_path(run_dir, lane, rnd)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render("subagent-prompt.md", values))
    log(f"subagent prompt written: {path}  -> Agent tool, model={lane['model']}")


def _post_round(run, run_dir, rnd, body_for_lane, launch):
    ensure_joined(run)
    for lane in run["lanes"]:
        lane[task_key(rnd)] = post_task(run, lane["agent"], body_for_lane(lane))
        log(f"task {lane[task_key(rnd)]} -> {lane['agent']}")
    save_run(run_dir, run)
    time.sleep(1)
    procs = {}
    for lane in run["lanes"]:
        # Forward slashes everywhere a lane will paste a path into Bash: backslash
        # Windows paths get mangled in some shell positions (the agent-sync skill's
        # first gotcha), and forward slashes work in every host shell here.
        values = {
            "agent": lane["agent"], "model": lane["model"], "token": f"{lane['token']}-r{rnd}",
            "task_id": lane[task_key(rnd)], "workspace": run["workspace"].replace("\\", "/"),
            "run_dir": run_dir.replace("\\", "/"), "round": rnd, "lead_agent": run["lead_agent"],
            "sync_script": run["sync_script"].replace("\\", "/"), "marker": run.get("marker") or "",
        }
        if lane.get("runner") == "subagent":
            _write_subagent_prompt(run, run_dir, lane, rnd, values)
            continue
        prompt = render(f"lane-prompt-r{rnd}.md", values)
        with open(lane_prompt_path(run_dir, lane, rnd), "w", encoding="utf-8") as f:
            f.write(prompt)
        if launch:
            procs[lane["agent"]] = (lane, launch_opencode(run, run_dir, lane, rnd, prompt))
    return procs


def _supervise(run, run_dir, rnd, procs, timeout):
    """Wait for opencode lanes; relaunch once without variant if a lane died before joining."""
    if not procs:
        return
    start = time.time()
    checked_join = False
    relaunched = set()
    while time.time() - start < timeout:
        time.sleep(30)
        elapsed = int(time.time() - start)
        inbox = inbox_text(run)
        done = delivered_task_ids(inbox)
        pending = [a for a, (lane, _) in procs.items() if lane[task_key(rnd)] not in done]
        if elapsed >= 120 and not checked_join:
            checked_join = True
            joined = joined_agents(room_text(run))
            for agent, (lane, proc) in list(procs.items()):
                if agent not in joined and proc.poll() is not None and agent not in relaunched:
                    log(f"{agent} exited (rc={proc.returncode}) without joining; relaunching without variant")
                    with open(lane_prompt_path(run_dir, lane, rnd), encoding="utf-8") as f:
                        prompt = f.read()
                    procs[agent] = (lane, launch_opencode(run, run_dir, lane, rnd, prompt, use_variant=False))
                    relaunched.add(agent)
        log(f"round {rnd}: delivered {len(procs) - len(pending)}/{len(procs)} opencode lanes; pending {pending}")
        if not pending:
            break
    for agent, (lane, proc) in procs.items():
        if proc.poll() is None:
            log(f"{agent} still running (pid {proc.pid}); leaving it")
    save_run(run_dir, run)


def cmd_round1(args):
    run = load_run(args.run)
    with open(os.path.join(args.run, "task-r1.md"), encoding="utf-8") as f:
        body = f.read()
    if run.get("marker"):
        body += f"\n\nDELIVERY MARKER: end your task-done body with a standalone line reading exactly:\n{run['marker']}\n"
    procs = _post_round(run, args.run, 1, lambda lane: body, launch=not args.no_launch)
    log("round 1 posted. Launch the subagent lanes now with the Agent tool (prompts under prompts/).")
    _supervise(run, args.run, 1, procs, args.timeout)


def cmd_round2(args):
    run = load_run(args.run)
    r1 = os.path.join(args.run, "round1")
    if not glob.glob(os.path.join(r1, "*.md")):
        raise SystemExit("collect round 1 first: swarm.py collect --run <dir> --round 1")
    matrix = os.path.join(r1, "matrix.md")
    if not os.path.isfile(matrix):
        log("WARNING: round1/matrix.md missing; lanes will read raw answers only (run matrix-prompt first)")
    fs = lambda p: p.replace("\\", "/")  # noqa: E731  (paths pasted into lane shells)
    values = {"workspace": fs(run["workspace"]), "run_dir": fs(args.run), "round1_dir": fs(r1),
              "matrix_path": fs(matrix), "vote_keys": ", ".join(run["vote_keys"]), "lead_agent": run["lead_agent"]}

    def body_for(lane):
        return render("task-r2.md", dict(values, task_id_r1=lane[task_key(1)], agent=lane["agent"]))

    procs = _post_round(run, args.run, 2, body_for, launch=not args.no_launch)
    log("round 2 posted. Launch the subagent lanes now with the Agent tool (prompts under prompts/).")
    _supervise(run, args.run, 2, procs, args.timeout)


def cmd_status(args):
    run = load_run(args.run)
    rnd = args.round
    states = lane_states(room_text(run))
    done = delivered_task_ids(inbox_text(run))
    print(f"{'lane':20s} {'runner':9s} {'task':>5s} {'bus':11s} delivered")
    for lane in run["lanes"]:
        tid = lane.get(task_key(rnd))
        print(f"{lane['agent']:20s} {lane.get('runner', '?'):9s} {str(tid):>5s} "
              f"{states.get(lane['agent'], 'not-joined'):11s} {'yes' if tid in done else 'no'}")


def cmd_wait(args):
    run = load_run(args.run)
    rnd = args.round
    start = time.time()
    while time.time() - start < args.timeout:
        done = delivered_task_ids(inbox_text(run))
        pending = [l["agent"] for l in run["lanes"] if l.get(task_key(rnd)) not in done]
        log(f"round {rnd}: delivered {len(run['lanes']) - len(pending)}/{len(run['lanes'])}; pending {pending}")
        if not pending:
            return
        time.sleep(args.interval)
    log("wait timed out")
    sys.exit(3)


def cmd_collect(args):
    run = load_run(args.run)
    rnd = args.round
    out_dir = os.path.join(args.run, f"round{rnd}")
    os.makedirs(out_dir, exist_ok=True)
    index = {}
    for lane in run["lanes"]:
        tid = lane.get(task_key(rnd))
        body = thread_body(run, tid) if tid else ""
        with open(os.path.join(out_dir, f"{lane['agent']}.md"), "w", encoding="utf-8") as f:
            f.write(f"# Round {rnd} answer: {lane['agent']} ({lane['model']}, {lane.get('runner')}), task {tid}\n\n")
            f.write(body if body else "(not delivered yet)\n")
        entry = {"task_id": tid, "model": lane["model"], "family": lane.get("family"),
                 "delivered": bool(body), "bytes": len(body)}
        if rnd == 2 and body:
            entry["votes"] = parse_votes(body, run["vote_keys"])
        index[lane["agent"]] = entry
        print(f"{lane['agent']:20s} task {tid} {len(body):6d} bytes" + (f" votes={entry.get('votes')}" if rnd == 2 and body else ""))
    with open(os.path.join(out_dir, "index.json" if rnd == 1 else "votes.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=1)
    if rnd == 2:
        counts = tally(index, run["vote_keys"])
        for key, c in counts.items():
            print(f"TALLY {key}: {c}")
        pending = [a for a, e in index.items() if not e["delivered"]]
        print("pending:", pending)


def cmd_matrix_prompt(args):
    run = load_run(args.run)
    r1 = os.path.join(args.run, "round1")
    fs = lambda p: p.replace("\\", "/")  # noqa: E731
    print(render("matrix-prompt.md", {
        "round1_dir": fs(r1), "matrix_path": fs(os.path.join(r1, "matrix.md")),
        "task_path": fs(os.path.join(args.run, "task-r1.md")), "vote_keys": ", ".join(run["vote_keys"]),
        "lanes": ", ".join(f"{l['agent']} ({l.get('family')})" for l in run["lanes"]),
        "lead_agent": run["lead_agent"], "workspace": fs(run["workspace"]), "sync_script": fs(run["sync_script"]),
    }))


def cmd_relaunch(args):
    run = load_run(args.run)
    lane = next((l for l in run["lanes"] if l["agent"] == args.agent), None)
    if not lane or lane.get("runner") != "opencode":
        raise SystemExit("unknown opencode lane")
    with open(lane_prompt_path(args.run, lane, args.round), encoding="utf-8") as f:
        prompt = f.read()
    proc = launch_opencode(run, args.run, lane, args.round, prompt, use_variant=not args.no_variant)
    log(f"waiting for pid {proc.pid}")
    proc.wait()
    log(f"exit {proc.returncode}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("--workspace", required=True)
    p.add_argument("--run", required=True, help="run name (folder under <workspace>/swarm-runs/)")
    p.add_argument("--task", required=True, help="round-1 task body (markdown)")
    p.add_argument("--roster", default="default.json", help="roster file or name under rosters/")
    p.add_argument("--lead-agent", default="claude")
    p.add_argument("--lead-session", default=None)
    p.add_argument("--sync-script", default=SYNC_DEFAULT)
    p.add_argument("--marker", default=None, help="required standalone completion line (supervised lanes)")
    p.add_argument("--vote-keys", default=None, help="comma list; default WORK,COMPANY,A")
    p.set_defaults(func=cmd_init)

    for name, func in (("round1", cmd_round1), ("round2", cmd_round2)):
        p = sub.add_parser(name)
        p.add_argument("--run", required=True)
        p.add_argument("--no-launch", action="store_true", help="post tasks and write prompts only")
        p.add_argument("--timeout", type=int, default=900)
        p.set_defaults(func=func)

    for name, func in (("status", cmd_status), ("collect", cmd_collect)):
        p = sub.add_parser(name)
        p.add_argument("--run", required=True)
        p.add_argument("--round", type=int, default=1)
        p.set_defaults(func=func)

    p = sub.add_parser("wait")
    p.add_argument("--run", required=True)
    p.add_argument("--round", type=int, default=1)
    p.add_argument("--timeout", type=int, default=540)
    p.add_argument("--interval", type=int, default=45)
    p.set_defaults(func=cmd_wait)

    p = sub.add_parser("matrix-prompt")
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_matrix_prompt)

    p = sub.add_parser("relaunch")
    p.add_argument("--run", required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--round", type=int, default=1)
    p.add_argument("--no-variant", action="store_true")
    p.set_defaults(func=cmd_relaunch)

    args = ap.parse_args()
    if hasattr(args, "run") and args.cmd != "init":
        args.run = os.path.abspath(args.run)
    args.func(args)


if __name__ == "__main__":
    main()
