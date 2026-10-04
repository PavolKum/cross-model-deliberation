# Round 1 answer: cc-claude-fable (fable, subagent), task 204

# Task 204 - ledger layout and naming (cc-claude-fable, round 1, independent)

Inputs read, in order: `next-steps.md` (sections "Decisions these force", "Split of work", "Measurement"); `ledger-consolidation-2026-10-03.md` sections 0, 2.1-2.3, 3.1, 3.4, 4 (file-by-file diff skipped); `claude-quota-mcp/README.md` in full. No other lane's output read.

## Findings, ranked by how much they change the plan

### 1. Question A was largely settled by events on 2026-10-03 between 13:00 and 18:08. The "one repo for the pair" proposal is stale. Vote: separate repo.

- Evidence: `next-steps.md` "Decisions these force" still says "Proposed home: one GitHub repo for the pair, two PyPI packages". But "Split of work" item 1 records that the quota MCP shipped at 18:08 as a standalone public repo named after the package, tag `v0.2.0`, with a CI workflow that publishes via PyPI trusted publishing and a *pending publisher* keyed to owner + repository `claude-quota-mcp` + `publish.yml` + environment `pypi`. The README (Install section) now points `pip install git+https://github.com/PavolKum/claude-quota-mcp` at that repo.
- The consolidation report's monorepo case rested on "the monorepo is free at exactly this moment and expensive later" (section 3.4, "Why one repo, not two", point 1). That was true for the quota half at 13:00 and is false now. Moving the quota MCP into `packages/claude-quota/` would: re-key the pending PyPI publisher; change `[project.urls] Repository`; turn the one working install line into `git+...#subdirectory=packages/claude-quota`; and require per-package tag schemes and path filters in CI. All of that for a repo whose entire value is "small, stdlib, audit it yourself" (README "Design notes"; report 2.3, last paragraph; report 3.4 "Trust asymmetry").
- The report itself anticipated this outcome and endorsed it: "publish claude-quota-mcp standalone first ... keep the monorepo for the ledger when it is ready. That is the faster path ... the one I would take if forced to pick one thing to ship this week" (3.4, "The honest counter-argument"). That is what happened. The remaining question is only where the ledger goes, and the same "fresh history anyway" argument that made the monorepo free makes a separate repo equally free.
- Weighing the five factors the task lists:
  - Fresh history: neutral between one-repo and separate-repo; both are new repos for the ledger. It only argues against folding into the quota repo, which would import a 20-module engine into a 250-line tool's history.
  - Trust story: argues hard against fold-in and moderately against one-repo (a stranger auditing `quota.py` should land in a repo that *is* the quota tool, not a `packages/` subtree next to a 46 KB-per-module analytics engine; report 3.4 point 2).
  - Cadence and audience: report 3.4 points 1 and 4 (different questions, different people; an emergency quota fix should not ship a ledger release). Separate repos decouple fully; a monorepo decouples only with extra CI machinery.
  - Agent discoverability: registries and model-facing docs index *packages*, each with one README and one Repository URL. Two single-purpose repos each with a README that is the whole story index better than one monorepo README that has to split attention. The report's "one place where the thesis lives" benefit (3.4, "Why one repo", point 2) is achievable at zero structural cost with a cross-link paragraph in both READMEs and a shared GitHub topic (`fleet-economics`). An umbrella landing repo can be added later *if* the probe returns a positive signal; it is not needed to run the probe.
  - One-person maintenance: two small repos sharing a copied, already-proven `publish.yml` is less to maintain than one repo with path-filtered, two-publisher CI. The quota repo's CI is already green on tag; copy it.
- Fold-into-quota-repo is rejected outright: wrong name for a four-harness ledger, destroys the audit story, and couples cadences in the one direction that hurts most.

### 2. (D) The probe's measurement clock is under-specified now that the halves ship weeks apart. Not moot, but it needs one more decision before the 30 days start.

- Evidence: `next-steps.md` "Measurement for the probe": "Thirty days from publish: external installs and first successful calls ... or a recorded zero." Singular "publish". The quota MCP is public now (but PyPI is still pending one web step, so `uvx` does not resolve yet and only git installs can be counted). The ledger is behind: the lineage-direction decision (report 3.1), the merge (next-steps step 2), orphan/filter history (step 5), and repo + PyPI creation (step 4).
- Recommendation: start the quota MCP's 30-day clock at its PyPI release, not at the GitHub push, and run the ledger's clock separately from its own PyPI release. Record both. Do not block the quota clock on the ledger, and do not pretend the pair launched together. This is the single item in D that would actually change the plan text.
- Nothing in the inputs says the ledger should not ship at all. The leak findings (report 2.2) are all about *history*, and the engine modules are explicitly clean (report 2.1: ten named modules "clean of hardcoded user paths and machine names"). The fix (orphan history) is routine, just gated on the owner.

### 3. (B) Name: `fleet-ledger`. Reserve `fleet-economics` for the umbrella, not a package.

- `fleet-economics` is the thesis name (report 3.4 proposed it as the *repo* name; `next-steps.md` opening line calls the whole probe "fleet economics"). Spending it on one half misleads a stranger into expecting both tools, or a framework. Keep it as a GitHub topic / future landing README; do not squat it on PyPI.
- `ai-fleet-ledger`: the `ai-` prefix carries no information in this registry; every neighbour is AI. Rejected.
- `agent-usage-ledger`: most literal description of the code (every MCP tool is `usage_*`; the current name is `opencode-usage`; a third internal lineage is already called `agent-usage`, report 1.5). But it drops "fleet", and the probe's whole purpose is to test the "fleet economics" framing. A name that does not carry the frame does not test it. Rejected for the probe; it is the right fallback if the framing is dropped.
- `fleet-ledger` vs `agent-fleet-ledger`: this is the real contest.
  - Stranger-agent comprehension: `agent-fleet-ledger` is self-explaining; `fleet-ledger` alone could read as vehicle-fleet accounting or a Kubernetes/Elastic "Fleet" add-on. But a name is never read alone in a registry: the summary line and keywords sit next to it, and the quota MCP's own README already shows the audience uses "fleet" for coding agents. Within the audience that would install it, "fleet" is understood.
  - Harness-agnostic: both pass, and both are count-agnostic, which matters because the ledger may ship with five readers, not four, if the Copilot reader goes public (report 3.1, 4).
  - Collision: `fleet-ledger` has mild overlap with vehicle-fleet software; `agent-fleet-ledger` has none. "Ledger" overlaps accounting/blockchain in both, but "a record of spend" is the intended sense, so that is not a collision, it is the meaning.
  - Length: 12 vs 18 characters. The name gets typed (`uvx fleet-ledger`, `claude mcp add usage -- fleet-ledger`), becomes the import (`fleet_ledger`), the console script and the MCP server name. Short wins at every one of those sites.
  - Tiebreaker: the ledger genuinely pools across *machines* as well as harnesses (report 2.2 `pool/aggregates`, `machine_label`), so "fleet" describes the data, not just the marketing.
- Vote `fleet-ledger`, confidence M on this sub-question. Explicit runner-up: `agent-fleet-ledger`, to be preferred if the "fleet economics" frame is dropped before publish or if a registry search at publish time shows `fleet-*` crowded by vehicle or k8s packages.
- This answer is needed *now*, independent of the repo decision: agent-safe step 2 in `next-steps.md` ("add `pyproject` with a package directory, choose the new name") is blocked on it, and the package directory name (`fleet_ledger/`) is a rename later if changed.

### 4. (C) Do not rename the quota MCP. Strong no.

- The name is load-bearing in the shipped artefact, not just a label: three console scripts (`claude-quota-mcp`, `claude-quota-hook`, `claude-quota-statusline`), the env-var family (`CLAUDE_QUOTA_*`), the snapshot path (`%LOCALAPPDATA%\claude-quota-mcp\`), the pending PyPI publisher, and, most importantly, the honesty line in the README: "The request then identifies itself honestly as `claude-quota-mcp`; nothing here impersonates Claude Code" (README, "Where the numbers come from"). Renaming churns every one of those for family cohesion that a cross-link already provides.
- `fleet-quota` would be *less* accurate. The tool reports one account's windows (README: "account-wide windows only"; Codex "snapshot only"). It does not aggregate across a fleet. The name would overclaim exactly the thing the README is careful not to claim.
- `claude-` and `-mcp` are the two tokens a human or an agent searches for in a registry; `fleet-` is neither. The only real misnomer is that it also covers Codex, and the README handles that in its own section. Not worth a rename.

### 5. Minor: what the plan text should change

- `next-steps.md` "Decisions these force", bullet 1: replace "one GitHub repo for the pair" with "two repos, cross-linked, shared topic". Bullet 3: "Rename the ledger package" becomes "Rename to `fleet-ledger`".
- `next-steps.md` "Measurement": two clocks, both from PyPI release.

## Confidence by sub-question
A separate-repo: H (the facts moved; the report's own counter-argument is now the executed state). B `fleet-ledger`: M (runner-up stated). C no rename: H. D: H that nothing makes the ledger moot; the clock rule is the one gap.

VOTE LAYOUT=separate-repo
VOTE NAME=fleet-ledger
VOTE RENAME=no
CONFIDENCE=H