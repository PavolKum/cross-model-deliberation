# Swarm decision: ledger repo layout and package name (2026-10-03, first run of the agent-swarm skill)

Facilitator: Claude (Fable 5.1) session, no position of its own on this question. Lanes: GPT 6 Astra (xhigh), GPT 6.1 Sol (xhigh) via OpenCode on the OpenAI endpoint; Claude Fable, Opus, Sonnet as Claude Code subagents. Task: `task-r1.md`. Round-one answers: `round1/*.md`, matrix `round1/matrix.md`. Round-two votes: `round2/*.md`, `round2/votes.json`. Bus tasks 202-206 (round 1) and 233-237 (round 2).

Timing: init 21:32, round one delivered 21:36 (four minutes for five lanes), matrix 21:40, round two delivered 21:44. Twelve minutes end to end, one facilitator, no relaunches.

## Tallies

| Key | Round 1 (5 of 5) | Round 2 (5 of 5) |
|---|---|---|
| LAYOUT | separate-repo 5 | separate-repo 5 |
| NAME | agent-usage-ledger 3 (Astra, Sol, Opus), fleet-ledger 2 (Fable, Sonnet) | agent-usage-ledger 5 |
| RENAME quota MCP | no 5 | no 5 |
| Confidence | H 1, M 4 | M 5 |

## What moved, and why

- **Fable** (fleet-ledger -> agent-usage-ledger): with RENAME unanimous at no, the sibling package never carries "fleet", so a fleet-prefixed ledger name buys no family coherence; the length objection dissolves because the distribution name need not equal the console script. A new argument, not a concession to the count.
- **Sonnet** (fleet-ledger -> agent-usage-ledger): "usage" is the author's own token in the shipped surface (`usage_*` MCP tools, the server registered as `usage`, a third lineage folder already named `agent-usage`); "fleet" appears only in the planning prose. Drafted its switch before seeing Fable's.
- **Opus** (no vote moved, three sub-arguments did): conceded the probe clock starts per tool at the PyPI release, withdrew its "a PyPI name cannot be renamed in place" argument as future lock-in rather than a cost already paid, and demoted the blast-radius argument after Astra showed an orphan-history fresh tree has no rewrite to misfire.
- **Astra and Sol** held: function clarity and avoiding migration outweigh the branding value of "fleet"; both said the tally did not move them.

The one round-one split was cross-family (the two GPT lanes agreed, the Claude lanes split 2 to 1), round one was blind, and both switches carried fresh arguments rather than a count, so this run shows no cascade signature.

## Decision

1. **Separate repository for the ledger.** The quota MCP is already public under its own name with a pending PyPI publisher bound to that repo; the monorepo recommendation in the consolidation report rested on a timing window that closed the same day. The ledger needs a fresh, clean history anyway.
2. **Package name `agent-usage-ledger`**, decided now, applied after the lineage merge. A shorter console script is fine. `fleet-economics` stays free as the umbrella label for the pair in docs and cross-links, not as a package name.
3. **`claude-quota-mcp` keeps its name.**
4. **Probe clock rule (raised by three lanes, not in the task):** one thirty-day window per tool, starting at that tool's PyPI release; GitHub installs before that count as early evidence, not as the window. The plan text had left the channel undefined.

## Dissent and residuals on record

- Fable's reputation-lens objection that `agent-usage-ledger` is descriptive but forgettable was not answered by any lane; Sonnet weighted the cold-read case as stronger for a demand probe specifically, not as a universal naming rule.
- Opus: the name is less consequential than the clock rule and the pending-publisher web step, which remains the real critical path.

## Harness notes from this run

- Five lanes, two rounds, twelve minutes, zero relaunches, all logs captured. The GPT lanes finished in about four minutes per round; the Claude subagents in three to four.
- Defect found: `swarm.py status` shows lanes that delivered and left as "joined: no". Fixed the same evening (left / online / not-joined).
- Defect found: the matrix template rendered one path with a backslash glob; fixed.
- The round-two task's "wait once for peers" produced real exchange: Opus addressed Astra directly, Fable and Sonnet addressed Opus by name, and the two GPT lanes recorded that the count did not move them.
