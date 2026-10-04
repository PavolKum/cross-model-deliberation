ADJUDICATION (read-only, independent): repo layout and package name for the usage-ledger half of the "fleet economics" pair. This is a small decision used to test the agent-swarm harness; answer it properly anyway. Do not read other lanes' tasks or results before you deliver; the agreement matrix is computed afterwards from independent answers.

Background. Today's swarm chose a company-route demand probe: publish two tools as "fleet economics" for people who run fleets of coding agents on subscriptions. Tool 1, `claude-quota-mcp`, is already public at github.com/PavolKum/claude-quota-mcp (v0.2.0, MIT, one MCP tool plus a hook plus a statusline script; PyPI release pending). Tool 2, the usage ledger (working name `opencode-usage`, which is taken on PyPI), reads local usage logs of four harnesses (OpenCode, Claude Code, Cursor, Codex) and prices them against a verified pricing table; it exposes an MCP server (usage_summary, usage_by_model, usage_sessions, ...) and a CLI. It must be re-created from a clean history (its current git history tracks private per-message exports) and consolidated from two diverged lineages before it can ship. The two tools share no code.

Read, in this order (all paths absolute, forward slashes work):
1. C:/Users/pavol/Repos_Local/General/review-swarm/fleet-economics-probe/next-steps.md (the plan; sections "Decisions these force" and "Split of work").
2. C:/Users/pavol/Repos_Local/General/review-swarm/fleet-economics-probe/ledger-consolidation-2026-10-03.md, only the sections on packaging state, publication blockers and the naming recommendation (search for "Naming" and "PyPI"). Skip the file-by-file diff.
3. C:/Users/pavol/Tools/claude-quota-mcp/README.md (the public tool's positioning and install story).

Questions (answer every one; rank by how much the answer changes the plan):
A. Layout. One GitHub repo for the pair with two PyPI packages; a separate repo for the ledger; or fold the ledger into the claude-quota-mcp repo as a second package. Weigh: the ledger needs a fresh history anyway; the quota MCP's trust story is "small, stdlib, audit it yourself"; different release cadences and audiences; discoverability by agents (registries, docs for models, training-data citation); maintenance burden for one person.
B. Name for the ledger package. Candidates verified free on PyPI on 2026-10-03: fleet-ledger, fleet-economics, agent-fleet-ledger, agent-usage-ledger, ai-fleet-ledger. Weigh: what a stranger agent reading a registry would understand; not tied to one harness (it reads four); collision with existing concepts (ledger, fleet); length.
C. Should the quota MCP be renamed to match the family (e.g. fleet-quota) or stay `claude-quota-mcp`? It is already public under that name.
D. Anything in the inputs that makes this decision moot or premature (e.g. the ledger should not ship at all until the lineage merge, or the probe should run with the quota MCP alone first).

Deliver: ranked findings with evidence (file + section), then EXACTLY these lines at the end:
VOTE LAYOUT=<one-repo-two-packages | separate-repo | fold-into-quota-repo>
VOTE NAME=<fleet-ledger | fleet-economics | agent-fleet-ledger | agent-usage-ledger | ai-fleet-ledger | other:<name>>
VOTE RENAME=<yes | no>
CONFIDENCE=<H | M | L>
Keep the output free of client, portfolio or named-person specifics and do not repeat an employer's name even if a file contains it. Do not edit or create files in the workspace; your only writes are bus commands.
