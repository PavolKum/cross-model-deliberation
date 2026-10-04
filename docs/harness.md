# Supporting harness: requirements and operation

The harness supports the process described in the [technical report](../REPORT.md). It is an internal tool released with observational evidence. The required coordination bus is not included, so running the original workflow requires supplying a compatible implementation or adapting the harness and templates.

## Requirements

- Python 3.11+; the harness and local checks use the standard library.
- A local agent-sync bus implementing `join`, `task`, `task-state`, `task-done`, `tell`, `working-note`, `leave`, `room`, `inbox`, `thread`, `wait` and `drain`. Set `AGENT_SYNC_SCRIPT` or pass `--sync-script`. Inspect the harness and templates for the expected arguments and return formats; adaptation effort has not been measured.
- OpenCode configured for OpenAI authentication for the default GPT lanes. The operator used the native `opencode.exe` on Windows after problems with the `.cmd` shim.
- Claude Code with subagent support for the default Claude lanes and facilitator workflow.

The [default roster](../rosters/default.json) uses subscription-backed routes as a local response to a shared prepaid-balance incident. This is not evidence of general quota or reliability guarantees. Authentication and service terms remain the operator's responsibility.

## Run sequence

[SKILL.md](../SKILL.md) contains the detailed operating procedure. Replace the angle-bracket placeholders below with your own workspace and run name:

```text
python scripts/swarm.py init --workspace <ws> --run <name> --task task.md --vote-keys KEY1,KEY2
python scripts/swarm.py round1 --run <ws>/swarm-runs/<name>
```

Launch each Claude lane as a subagent using its generated `prompts/<lane>-r1.md`, then collect the results:

```text
python scripts/swarm.py collect --run <ws>/swarm-runs/<name> --round 1
python scripts/swarm.py matrix-prompt --run <ws>/swarm-runs/<name>
```

Give the matrix prompt to a synthesis lane, which writes `round1/matrix.md`. Start round two, launch its Claude subagent prompts, and collect after delivery:

```text
python scripts/swarm.py round2 --run <ws>/swarm-runs/<name>
python scripts/swarm.py collect --run <ws>/swarm-runs/<name> --round 2
```

The facilitator writes `decision.md`: both tallies, changes and reasons, dissent, execution failures and next steps. The harness does not make the final decision. Record any facilitator preference separately from lane counts.

## Local checks

```text
python tests/test_swarm.py
python scripts/report_metrics.py
```

The first checks harness behavior; the second recomputes published naming-run results. Neither requires a live bus or proves an end-to-end installation works.

## Files and publication boundary

| Path | Purpose |
|---|---|
| `scripts/swarm.py` | Initialization, dispatch, status, collection and relaunch operations |
| `templates/` | Lane and synthesis prompts |
| `rosters/default.json` | Default lane configuration |
| `tests/test_swarm.py` | Local harness checks |
| `runs/` | Selected historical task and final-answer artifacts |
| `reports/` | Historical operator account |

Live `run.json`, generated prompts and logs may contain session tokens. They are excluded from this evidence release. Published answer records are not full transcripts. Consult the technical report before reusing historical timing, confidence or answer-length claims.
