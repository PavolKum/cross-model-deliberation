# agent-swarm

Two-round, multi-vendor adjudication for decisions a single model should not make alone. Several model lanes answer the same question blind, a matrix shows where they agree, then the lanes read each other, argue once on a shared bus, and vote. The facilitator is a human-driven Claude Code session; the lanes are GPT models via OpenCode on the OpenAI endpoint and Claude models as Claude Code subagents, all on subscriptions.

This is an internal tool published as-is, with the evidence from its first two runs. It is not a product. It is here because the measurements were worth more public than private.

## What the two runs showed

**The first harnessed run** (`runs/2026-10-03-ledger-naming/`): a package-naming and repository-layout decision, three vote keys.

| Measure | Value |
|---|---|
| Lanes | 5 (GPT 6 Astra, GPT 6.1 Sol, Claude Fable, Opus, Sonnet) |
| Rounds | 2 |
| Wall-clock, init to final tally | 12 minutes |
| Relaunches | 0 |
| Round one | split 3 to 2 on the name, cross-family (both GPT lanes on one side, Claude lanes 2 to 1) |
| Round two | unanimous on all three keys |

The two lanes that switched each brought a new argument rather than deferring to the count; one drafted its switch before seeing the other's. The two GPT lanes recorded that the tally did not move them. Round one was blind, so the run shows no cascade signature. Full transcripts, matrix, votes and the decision with dissent are in the run folder.

**The hand-driven run the harness was built from** (`reports/2026-10-03-routing-adjudication-mechanics.md`): eight lanes across four vendors, about fifty minutes, 5 of 8 delivered on first launch, three lanes needed human recovery, one lane flagged a plausible information cascade, five of seven changed a vote after debate, and the facilitator's own pick lost and was withdrawn. The same report measures a supervised read-only launcher against raw dispatch on the same task: the supervised lane enforced read-only tools and then correctly refused to commit its answer because the facilitator wrote files mid-run.

## Why two rounds

A single round of independent answers gives you a vote but no reasons for the disagreement. A single round of open debate gives you a cascade: later lanes cite earlier ones. Blind answers first, then a matrix, then one bounded exchange and a fixed vote block, separates "where do strong models disagree" from "does the disagreement survive contact". What moved between rounds, and why, is the output. The tally is secondary.

## Why subscriptions only

On the eight-lane run a prepaid OpenRouter balance hit zero mid-round and took three lanes down at once. No subscription lane failed that way. The roster in `rosters/default.json` therefore allows only GPT lanes on the OpenAI endpoint and Claude lanes as Claude Code subagents. Claude lanes never run through OpenCode or OpenRouter: the Claude Code token is bound to Claude Code by its terms, and routing it elsewhere is both a terms problem and, on this evidence, the less reliable path.

## What you need

- **An agent-sync bus.** The lanes coordinate through a local SQLite bus with six commands: `join`, `task-state`, `task-done`, `tell`, `working-note`, `leave`. Ours is not yet published; it is a large single-file script under scrub review. Until it is, this repository is the protocol, the harness, the templates and the evidence, not a turnkey install. The templates show exactly which bus calls a lane makes, so adapting them to another bus is a small job. Set `AGENT_SYNC_SCRIPT` to your bus script, or pass `--sync-script`.
- **OpenCode** with OpenAI authentication, for the GPT lanes. On Windows pass the native `opencode.exe`, not the npm `.cmd` shim.
- **Claude Code** with the Agent tool, for the Claude lanes and for the facilitator role.
- Python 3.11 or later, standard library only.

## Running a swarm

`SKILL.md` is the operating procedure, written as a Claude Code skill. In short:

```
python scripts/swarm.py init --workspace <ws> --run <name> --task task.md --vote-keys KEY1,KEY2
python scripts/swarm.py round1 --run <ws>/swarm-runs/<name>        # background; launches GPT lanes, writes subagent prompts
# launch each Claude lane as a subagent from prompts/<lane>-r1.md
python scripts/swarm.py collect --run <ws>/swarm-runs/<name> --round 1
python scripts/swarm.py matrix-prompt --run <ws>/swarm-runs/<name>  # give to one strong subagent; it writes round1/matrix.md
python scripts/swarm.py round2 --run <ws>/swarm-runs/<name>        # background; debate and vote
python scripts/swarm.py collect --run <ws>/swarm-runs/<name> --round 2
```

Then write `decision.md` yourself: both tallies, what moved and why, dissent on record, any cascade caveat, the next step. The harness never writes the decision.

Tests: `python tests/test_swarm.py` (vote parsing, tally, rendering, init; no bus, no network).

## Failure modes the harness handles

Each of these happened on the first run: silent lane exit on an unsupported variant flag (join check at two minutes, one relaunch without the variant); lost stdout from detached launches (foreground children with logs); a lane answering an older task (task id repeated in every prompt); a lane joining under the generic identity (lane name in every bus command); the facilitator's own bus lease expiring mid-run (re-join before each round); prepaid credits running out (roster rule).

## Reading a result

- Report round one and round two separately. The movement is the signal.
- A unanimous round two is not proof. Check whether later lanes re-derived or cited earlier ones. Treat a strong majority as medium confidence until a frozen-packet experiment shows the swarm beats one strong lane. We have not run that experiment yet.
- The facilitator's own position goes in the matrix as a labelled column, excluded from counts, and is withdrawn in writing when it loses.

## Layout

```
SKILL.md                 operating procedure (Claude Code skill)
scripts/swarm.py         the harness: init, round1, round2, status, wait, collect, matrix-prompt, relaunch
templates/               lane prompts (OpenCode and subagent), round-two task body, matrix prompt
rosters/default.json     the subscription-only roster as data
tests/test_swarm.py      harness tests
runs/                    complete run records: task, every lane's answer per round, matrix, votes, decision
reports/                 measurements from the hand-driven run and the launcher comparison
```

Live run folders also contain `run.json`, `prompts/` and `logs/`, which carry bus session tokens. They are gitignored here and were not copied into `runs/`.

## Status and next

Version 0.1, October 2026. Two runs, both on the authors' own decisions. Next: publish the bus so the harness installs end to end; run the frozen-packet experiment (does a five-lane swarm beat the single strongest lane on cases with known answers); per-lane worktrees so supervised lanes can be used for reviews that gate a merge.

Companion tools from the same lab: [claude-quota-mcp](https://github.com/PavolKum/claude-quota-mcp) (rate-limit and quota visibility for Claude Code). A usage ledger for multi-harness fleets follows.

MIT licence.
