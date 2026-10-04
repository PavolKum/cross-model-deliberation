# Round 1 answer: oc-gpt-sol (openai/gpt-6.1-sol, opencode), task 203

# Independent Adjudication: Ledger Layout And Name

Recommendation: publish the ledger as `agent-usage-ledger` in its own fresh GitHub repo; keep `claude-quota-mcp` where it is and under its existing name. Treat "fleet economics" as the shared positioning, not a requirement for shared source control. Publish the quota package independently while the ledger clears its release gates.

Findings below are ranked by how much they change the execution plan, not by the order of the questions.

## 1. Publication Gates Matter More Than The Layout Vote (D)

The ledger must not ship from either existing lineage as-is. The inputs establish three separate gates: consolidate the engine and report pipeline, build a genuinely installable package, and publish only a clean code/docs tree with fresh history. A new repo name fixes none of those by itself.

Evidence: `next-steps.md`, "What the audits found" (lines 8-10), "Decisions these force" (lines 15-17), and "Split of work" (lines 26-33); `ledger-consolidation-2026-10-03.md`, "2.1 ... not packaged at all" and "2.2 What would leak ...". The latter records private exports throughout the history and a generated HTML file embedding raw records. Ignoring files or deleting them from the latest commit is insufficient. The flat module layout, missing packaging metadata and licence are additional release blockers.

Create the public ledger from an explicitly selected clean tree after consolidation, using synthetic examples, rather than pushing the private repo or its history. Preserve the private archive separately. Keep the live MCP working during the package move and update its configured path at the planned handoff.

These gates make ledger publication premature, not this decision moot: choosing the distribution name now avoids packaging twice. They do not justify delaying the quota probe. `next-steps.md`, "Split of work" (lines 22-25), records the quota tool's completed v0.2.0 work and public repo; its current `README.md`, "Install" (lines 58-74), provides an honest GitHub install while PyPI remains pending.

Start with the quota tool, then add the ledger. Track outcomes separately: quota installs demonstrate quota demand, not demand for historical usage reconciliation. Do not count an unavailable ledger as a zero-demand result or give it only the remainder of the quota tool's observation window. Evidence: `next-steps.md`, "Measurement for the probe" (lines 35-37), calls for installs, successful calls and an external reconciliation check.

## 2. Use A Separate Ledger Repo; Do Not Migrate The Public Quota Repo (A)

The strongest argument for the proposed monorepo is now partly obsolete. `ledger-consolidation-2026-10-03.md`, "3.4 Naming - two packages, one repo", argues that the monorepo is free at this moment because the ledger needs fresh history and the quota repo is not yet public. The later "Split of work" in `next-steps.md` records that the quota repo is already public, tagged and wired to its own publishing workflow. The current quota README also points users directly to it. The ledger's fresh start does not make moving the quota tool free.

- **Separate repo, recommended:** preserves existing links, installation instructions and the quota tool's small audit surface. Each tool gets an accurate root README, release history and issue context. There is no shared code to maintain twice. The cost is two repository configurations and release workflows, which is modest for a pair of independent Python packages.
- **One repo, two packages:** technically viable, with separate package versions, tags and CI. A monorepo does not inherently couple releases or enlarge the installed quota wheel. It does, however, require package-scoped release plumbing and a migration or duplicate-home decision for the public quota repo. With no shared implementation, those costs buy mainly a common landing page.
- **Fold into the quota repo:** avoids moving the quota URL but turns a narrowly named, easily audited project into the home of a much larger four-harness analytics tool. That is the weakest fit for both the ledger's audience and the quota tool's trust positioning.

Evidence: consolidation report "3.4", particularly "Why two packages, not one" and its discoverability counter-argument; quota `README.md`, opening pitch, "Where the numbers come from", and "Design notes". The current trust story is stronger than the older report describes: documented local sources by default, no credential unless explicitly opted in, and a stdlib core. Keep that story easy to verify.

For one-person maintenance, two simple repos are preferable to introducing a multi-package release system without shared code. Add reciprocal links and the same short "fleet economics: usage accounting plus quota headroom" description. Put each package's own repo and documentation in its registry metadata. This gives agents a direct, stable citation and a focused install recipe without needing a new umbrella repo. Repository layout alone does not establish discoverability or future training-data inclusion.

## 3. Name The Ledger `agent-usage-ledger` (B)

This is the clearest cold-read name: it says whose usage is recorded and that the tool maintains an accounting history. It fits all four harnesses and does not imply that a user needs an orchestrated fleet. Its extra length is worthwhile in a registry, where the name may be seen without the family pitch.

Candidate ranking:

1. `agent-usage-ledger`: most explicit description of the actual function; harness-neutral.
2. `agent-fleet-ledger`: identifies the domain but not what is being recorded; suggests fleet-level accounting only.
3. `ai-fleet-ledger`: signals AI but is less precise about coding agents and usage.
4. `fleet-ledger`: shortest, but easily mistaken for vehicle-fleet accounting or another general ledger product.
5. `fleet-economics`: good umbrella phrase, weak package identity; implies a broader economics offering rather than a concrete usage reader.

Evidence: consolidation report "2.1" describes the CLI/MCP aggregation surface, and "3.4" records all five candidates as free on the stated date. `next-steps.md`, "Decisions these force", confirms that `opencode-usage` must be replaced. Availability is accepted from those inputs, not independently rechecked.

Names alone cannot disambiguate every use of "agent" or "ledger". Use a registry summary such as: "Local coding-agent usage ledger for OpenCode, Claude Code, Cursor and Codex; MCP and CLI with API-equivalent pricing." Do not present priced subscription activity as an actual subscription bill. This name ranking is a semantic judgment, not measured discovery evidence.

## 4. Do Not Rename `claude-quota-mcp` For Family Symmetry (C)

Its present name gives a stranger agent three useful facts: the primary provider, the purpose, and the integration protocol. `fleet-quota` loses those clues and suggests broader fleet-wide coverage. The existing tool also supports Codex, but that is a reason to make its provider support visible in the description, not to rebrand it solely to match a sibling.

Evidence: quota `README.md`, opening pitch, "Install", "Codex too" and "Design notes"; `next-steps.md`, "Split of work", records the public v0.2.0 tag and name-specific publishing configuration. A rename would require changing commands, docs and publishing metadata just before the PyPI release, without demonstrated user benefit. Retain the distribution, repo and command names; use "fleet economics" in descriptive copy and cross-links.

Confidence: high on the release gates and preserving the public quota identity; medium on the comparative repo/name choice because no external discovery or user-testing evidence is provided. No project code, tests, network requests or images were used for this assessment.

VOTE LAYOUT=separate-repo
VOTE NAME=agent-usage-ledger
VOTE RENAME=no
CONFIDENCE=M