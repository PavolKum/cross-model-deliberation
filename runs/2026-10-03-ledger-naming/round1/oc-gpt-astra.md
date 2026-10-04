# Round 1 answer: oc-gpt-astra (openai/gpt-6-astra, opencode), task 202

# Independent Adjudication

Recommendation: publish the ledger in its own fresh-history repository as `agent-usage-ledger`; retain `claude-quota-mcp` unchanged. Use "fleet economics" as the shared positioning, not as a reason to migrate an already-public tool or couple the releases.

Findings below are ranked by how much they change the current plan, not by the severity of the publication risks. Evidence is limited to the three assigned documents; no code, tests, network checks, images, or other lanes' results were consulted. Name availability is the supplied 2026-10-03 snapshot, not independently reverified.

## 1. A: Choose Separate Repositories, Not The Proposed Monorepo

**Plan change:** replace the proposed one-repository destination with a new `agent-usage-ledger` repository. Leave the existing quota repository, URLs, package, and publication workflow in place.

**Evidence:** `ledger-consolidation-2026-10-03.md`, section 3.4, recommends one repository partly because there is no existing public repository to preserve and the ledger needs fresh history anyway. That premise is now stale for the pair: `next-steps.md`, "Split of work," records the quota repository as public, tagged v0.2.0, with its own publishing workflow. The quota `README.md`, "Install," already directs users to that repository. The consolidation report's own section 3.4 counterargument favors the quota tool's standalone, sharply defined public identity.

Fresh ledger history is necessary whichever layout wins. It is not a benefit unique to a monorepo, and it does not make relocating the quota tool free. Preserve the public artifact and create only the repository that is still missing.

Comparison of the three choices:

| Choice | Assessment |
|---|---|
| Separate ledger repository | Best fit now. Independent installation, releases, issues, source-audit scope, and discoverable repository identity. Cost: a second small CI/publication setup and reciprocal documentation links. |
| One repository, two packages | Technically sound, but unearned migration and release-configuration work for this probe. There is no shared code or demonstrated need for atomic cross-package changes. |
| Fold ledger into quota repository | Avoids moving the quota URL but turns a precisely named, small-tool repository into a misleading home for a larger multi-harness analytics product. Worst match for scope and positioning. |

**Trust and cadence:** the ledger has a much broader ingestion/reporting surface; quota advertises one small MCP schema, documented local sources, and an auditable stdlib core. Keeping their source trees separate makes that distinction easiest to inspect. This is not a security guarantee: a properly configured monorepo can still build small, independent distributions. Likewise, two packages in one repository do not inherently require coupled versions; section 3.4's version-coupling argument supports separate packages, not necessarily separate repositories. The stronger repository argument is that no shared implementation benefit offsets migration and release-routing complexity here.

**One-person maintenance:** two simple package repositories are preferable to introducing a multi-package release setup solely for branding. Make the consolidated ledger the authoritative implementation and repair or retire the divergent mirror as already planned; do not maintain a separate public fork alongside two internal source-of-truth copies. This follows `next-steps.md`, "Decisions these force," on stopping mirror divergence.

**Agent discoverability:** use explicit package summaries, supported-harness names, MCP tool descriptions, working install commands, stable source URLs, and reciprocal README links. A shared repository does not by itself create better registry retrieval or future training-data citation. The recognizable pair can be explained in a short "Fleet economics" section in each README. No third umbrella repository, shared framework, or documentation site is needed for the probe.

Additional evidence: consolidation report section 3.4, "Why two packages, not one"; quota `README.md`, "Where the numbers come from" and "Design notes."

## 2. B: Name The Ledger `agent-usage-ledger`

**Plan change:** replace the proposed `fleet-ledger` package name with `agent-usage-ledger`; use the same name for the new public repository.

This is the clearest candidate for a stranger or registry-reading agent. It identifies the subject (agents), the measured activity (usage), and the recordkeeping role (ledger), without implying dependence on one harness. It also does not imply that a single-user installation must operate a large fleet.

| Candidate | Judgment |
|---|---|
| `agent-usage-ledger` | Best semantic match. Longer than `fleet-ledger`, but the extra word provides useful discrimination. |
| `agent-fleet-ledger` | Same length class, less informative: says whose fleet, not what the ledger records. |
| `ai-fleet-ledger` | Explicitly AI-related, but still ambiguous about usage, inventory, orchestration, or financial accounting. |
| `fleet-ledger` | Short and memorable; readily confused with vehicle-fleet accounting or asset records when seen without context. |
| `fleet-economics` | Good umbrella phrase, weak package description. Suggests broader economic analysis or optimization than local usage ingestion and pricing. |

"Ledger" can suggest financial accounting or a blockchain product, and "agent" is not uniquely an AI term. None of the candidates eliminates ambiguity. The package summary should do the remaining work: "Local usage and API-equivalent cost ledger for OpenCode, Claude Code, Cursor, and Codex; CLI and MCP server." Keep API-equivalent valuation distinct from actual subscription charges rather than presenting calculated API prices as cash spent.

**Evidence:** consolidation report section 2.1 describes the CLI/MCP packaging needs; section 3.4 records all five candidates as available and the existing name as taken. Section 2.2's monthly-export schema explicitly distinguishes `api_equivalent_cost`, `cash_cost`, and `implied_cost`, supporting precise cost language. `next-steps.md`, "Decisions these force," already requires a ledger rename.

This is a semantic recommendation, not evidence of superior search ranking or conversion. Recheck registry and repository-name availability immediately before publication; do not delay consolidation for naming research.

## 3. D: Keep The Quota-First Probe; Gate Ledger Publication, Not This Decision

**Plan impact:** preserve the existing quota-first sequence and remove superseded blockers from the reasoning. Naming and selecting a fresh repository now are useful; shipping the current ledger is not safe.

The consolidation report's sections 2.3 and 4 describe the quota repository as nonexistent and its advertised installation as broken. Those statements are superseded by `next-steps.md`, "Split of work," and the current quota `README.md`, "Install": the repository is public, direct GitHub installation is documented, and PyPI is explicitly pending. The report also describes credential-based quota access in its trust argument, whereas the current README makes documented local snapshots the default and the OAuth endpoint explicit opt-in. Use the current state, not the older audit snapshot.

Run the quota demand probe through the existing installation path while completing its pending PyPI publication step. Do not wait for the ledger's consolidation to obtain the first external install and successful call.

The ledger still needs these release gates:

1. Consolidate the lineages and settle the authoritative source and mirroring behavior.
2. Construct a sanitized public tree with fresh history; exclude private exports, generated reports containing embedded data, and private coordination material. A new repository or orphan history alone does not sanitize the files copied into the first commit. Review both the public tree and built distributions before publishing.
3. Establish the package directory, license, dependencies, supported Python declaration, entry points, and honest install documentation, removing local-machine assumptions.
4. Preserve or explicitly update the live MCP registration when paths move; validate the actual packaged install before release.

**Evidence:** `next-steps.md`, "Decisions these force" and "Split of work"; consolidation report sections 2.1, 2.2, 3.3, and 4. No fresh ledger verification was authorized for this lane, so these remain report-derived gates, not assertions about newly inspected code.

Quota success is evidence for quota demand, not proof that users want the retrospective cost ledger or a paid fleet-economics product. Likewise, quota failure does not automatically refute ledger demand. Keep the plan's 30-day install/first-call and reconciliation measurements attributable to each released tool, rather than giving an unreleased ledger an already-running observation window. Evidence: `next-steps.md`, "Measurement for the probe."

## 4. C: Do Not Rename `claude-quota-mcp`

**Plan impact:** none beyond explicitly rejecting family-name churn.

Retain the existing public repository, package identity, and commands. A shared prefix offers little benefit compared with preserving the precise quota use case, published URL, and documented host/hook configuration. No evidence here justifies changing them to `fleet-quota` for symmetry.

There is a genuine counterargument: the quota README's "Codex too" section shows the tool already supports more than Claude. The name is therefore narrower than its capabilities. Address that with a "Claude and Codex quota headroom" description and registry keywords now, not a migration during the demand probe. Revisit only if observed adoption shows the Claude-specific name materially obstructs the product's audience.

**Evidence:** quota `README.md`, opening positioning, "Install," "The hook," and "Codex too"; `next-steps.md`, "Split of work," records the already-public v0.2.0 identity and pending publisher configuration under the existing name.

Confidence is high on preserving independent releases, not migrating the public quota tool, and blocking unsafe ledger publication; medium on the name preference and untested discoverability effects. Overall confidence is medium because the requested vote includes those product-positioning judgments.

VOTE LAYOUT=separate-repo
VOTE NAME=agent-usage-ledger
VOTE RENAME=no
CONFIDENCE=M