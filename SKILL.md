---
name: agent-swarm
description: Run a multi-model adjudication in two rounds (independent answers, then debate and vote) with GPT lanes via OpenCode and Claude lanes as Claude Code subagents; collect, build an agreement matrix, tally votes, decide. Use for "swarm", "council", "adjudicate", "get several models to vote", "cross-family review of a decision", or any time one strong model's answer should be checked by independent lanes before the operator acts on it. Subscription-backed lanes only.
allowed-tools: Read Bash PowerShell Glob Grep Write Edit Agent
---

# Agent swarm: independent answers, then debate and vote

Built 2026-10-03 from a hand-driven eight-lane adjudication (four model families, two rounds, the swarm reversing the facilitator's own pick). The mechanics of that run are in `reports/2026-10-03-routing-adjudication-mechanics.md`. This skill is the harness that run was hand-driven through, with the failure modes fixed. The first harnessed run is in `runs/2026-10-03-ledger-naming/`.

## When to use

- A decision with a real fork (allocation, architecture, go/no-go) where the operator wants several model families to weigh in independently before acting.
- Review experiments: frozen evidence packet, blinded cases, lanes answer alone, then the matrix.
- Not for routine code review, not for anything that must write files (lanes are read-only by contract), not when one lane and a hostile prompt would do.

## The roster rule

Subscription-backed lanes only. GPT lanes run through OpenCode on the OpenAI endpoint (`openai/gpt-6-astra`, `openai/gpt-6.1-sol`, variant `xhigh`). Claude lanes run as Claude Code subagents (Agent tool, model `fable` / `opus` / `sonnet`), never through OpenCode or OpenRouter: the Claude Code token is bound to Claude Code by its terms. No Gemini, Grok or OpenRouter prepaid lanes: a prepaid balance ran out mid-round and took three lanes down. `rosters/default.json` encodes this; copy it to make a variant.

## Flow (the facilitator is you, in Claude Code)

All commands: `python scripts/swarm.py <sub> ...` (forward slashes in Bash). The run lives under `<workspace>/swarm-runs/<name>/`. The workspace needs an agent-sync room (`agent_sync.py init` if `.agent-sync/` is missing); point `AGENT_SYNC_SCRIPT` or `--sync-script` at the bus script.

1. **Write the task body** (markdown): background, exclusions, the files to read in order, lettered questions, and the vote keys with their allowed options. Say explicitly "do not read other lanes' results". Keep it under about 6 KB; it travels as one argument.
2. **Init:** `swarm.py init --workspace <ws> --run <name> --task task.md [--roster default.json] [--vote-keys LAYOUT,NAME]`. Prints the run dir.
3. **Round 1:** run `swarm.py round1 --run <dir>` **in the background** (Bash `run_in_background`, timeout 600000). It posts one bus task per lane, launches the OpenCode lanes with logs under `logs/`, checks at two minutes that each joined and relaunches once without the variant if one died silently, and waits for delivery. It also writes `prompts/<lane>-r1.md` for every subagent lane.
4. **Launch the Claude lanes yourself,** one Agent call per subagent lane, `subagent_type: general-purpose`, `model` from the roster, prompt = the contents of `prompts/<lane>-r1.md`. Launch them in one message so they run concurrently. They join the bus, read their task, deliver with `task-done`, and leave.
5. **Collect:** when `swarm.py status --run <dir> --round 1` shows every lane delivered (or `swarm.py wait --run <dir> --round 1` returns), run `swarm.py collect --run <dir> --round 1`. Answers land in `round1/<lane>.md` plus `index.json`.
6. **Matrix:** `swarm.py matrix-prompt --run <dir>` prints the prompt; give it to one strong subagent. It writes `round1/matrix.md` and returns the tallies.
7. **Round 2:** `swarm.py round2 --run <dir>` in the background (same pattern as step 3). Each lane reads the matrix and all answers, posts one position note, waits once for peers, replies once if challenged, and votes with the fixed block (`VOTE <KEY>=...`, `CHANGED=`, `CONFIDENCE=`). Launch the subagent lanes from `prompts/<lane>-r2.md` as in step 4.
8. **Tally:** `swarm.py collect --run <dir> --round 2` writes `round2/votes.json` and prints the tally per key. Write `decision.md` yourself: both tallies, what moved between rounds and why, dissent on record, the cascade caveat if a lane raised one, and the next step. File it wherever your team keeps decisions.

Five lanes and two rounds took twelve minutes on the first harnessed run; the hand-driven eight-lane run took about fifty minutes of wall-clock plus recoveries.

## What the harness fixes (each one bit the first run)

- **Silent lane death:** OpenRouter-hosted Anthropic models exited on `--variant high` without joining; the launcher now checks joins at two minutes and relaunches once without the variant. Prefer the roster rule and this never triggers.
- **Lost stdout:** detached `.cmd` launches logged nothing. Lanes now run the native `opencode.exe` as a child with stdout to `logs/<lane>-rN.log`; the script waits, so run it in the background.
- **Wrong task:** one lane answered an older task. Prompts now repeat the task id and say "ignore any other task".
- **Generic identity:** one lane joined under the harness's default name. Prompts carry the lane name in every bus command.
- **Lease expiry:** the facilitator's own bus lease expired twice; `round1`/`round2` re-join with the stored token before posting.
- **Credits:** three lanes died when a prepaid balance ran out. Roster rule above.

## Supervised (heavyweight) lanes

A supervisor with a read-only launcher can give a lane a deny-by-default tool policy, parent-owned join/leave, a required completion marker and a before/after workspace hash. Two findings from the comparison run: pass the native `opencode.exe` as the binary (the npm `.cmd` shim fails on large prompts under the Windows 8 KB command-line limit), and whole-workspace attestation fails if anyone writes in the workspace during the run, which includes this script's `collect`. Use supervised lanes only in a quiescent per-lane worktree that holds just the frozen inputs; then the attestation is the receipt.

## Interpreting the result

- Report round-one and round-two tallies separately; what moved between them is the signal.
- A unanimous round two is not proof. Ask whether later lanes re-derived or cited earlier ones (a lane raised exactly this on the first run). Treat a strong majority as medium confidence until a frozen-packet experiment shows the swarm beats one strong lane.
- The facilitator's own position goes in the matrix as a labelled column, excluded from counts, and is withdrawn in writing when it loses.

## Privacy and hygiene

Task bodies and prompts tell lanes not to repeat names of employers, clients, portfolios or private individuals, and the matrix prompt repeats it. Bus notes posted by other lanes may still contain such names; the bus is local, but anything copied to a shared write-up is scrubbed first. Lanes write only to the bus and to `%TEMP%`; the run folder is written by this script and the matrix subagent only. Never commit `run.json`, `prompts/` or `logs/` from a live run: they carry session tokens.

## Files

- `scripts/swarm.py`: init, round1, round2, status, wait, collect, matrix-prompt, relaunch. Stdlib only. `python scripts/swarm.py -h`.
- `templates/`: `lane-prompt-r1.md`, `lane-prompt-r2.md` (OpenCode lanes), `subagent-prompt.md` (Claude lanes, both rounds), `task-r2.md` (debate-and-vote task body), `matrix-prompt.md`.
- `rosters/default.json`: the roster rule as data.
- `tests/test_swarm.py`: vote parsing, tally, template rendering, init in a temp workspace. `python tests/test_swarm.py`.
