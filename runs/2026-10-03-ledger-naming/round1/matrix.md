# Agreement matrix - round 1, ledger layout and naming

Built from the five independent lane answers in this folder plus `index.json`. No facilitator position is
included on this run (the facilitator had none). Lane text is quoted sparingly; everything else is
normalised paraphrase. Source question set: `task-r1.md` (questions A-D, vote keys LAYOUT / NAME / RENAME).

---

## 1. Lanes

| Lane | Model family | Delivered | Bytes | Confidence stated |
|---|---|---|---|---|
| oc-gpt-astra | gpt (gpt-6-astra) | yes | 10,469 | `CONFIDENCE=M`; split self-assessment: H on release independence + no migration, M on name and discoverability |
| oc-gpt-sol | gpt (gpt-6.1-sol) | yes | 7,900 | `CONFIDENCE=M`; split: H on release gates + keeping the public quota identity, M on the comparative repo/name choice |
| cc-claude-fable | claude (fable) | yes | 9,895 | `CONFIDENCE=H`; per-question A:H, B:M, C:H, D:H |
| cc-claude-opus | claude (opus) | yes | 13,435 | `CONFIDENCE=M`; per-question A:M-H, B:M, C:H, D:M-H, overall explicitly capped at the weakest (the name) |
| cc-claude-sonnet | claude (sonnet) | yes | 7,130 | `CONFIDENCE=M`; no per-question breakdown given |

Bytes are the delivered payload sizes recorded in `index.json`; the on-disk `.md` files are 120-134 bytes
larger because each carries a collection header line. No lane is pending - all five say delivered, and all
five files end with a complete four-line vote block.

Methodology note worth one line: fable and opus apply opposite aggregation rules to the same per-question
spread (both rate the name M), fable reporting H overall and opus deliberately reporting the weakest
sub-answer. The headline confidence spread is therefore partly an artefact of aggregation, not of
disagreement about certainty.

---

## 2. Allocation - vote keys

Picks normalised to the option names defined in `task-r1.md`.

| Lane | LAYOUT | NAME | RENAME |
|---|---|---|---|
| oc-gpt-astra | separate-repo | agent-usage-ledger | no |
| oc-gpt-sol | separate-repo | agent-usage-ledger | no |
| cc-claude-fable | separate-repo | fleet-ledger | no |
| cc-claude-opus | separate-repo | agent-usage-ledger | no |
| cc-claude-sonnet | separate-repo | fleet-ledger | no |

### Tally

| Key | Option | Count | Lanes |
|---|---|---|---|
| LAYOUT | separate-repo | **5** | all |
| LAYOUT | one-repo-two-packages | 0 | - |
| LAYOUT | fold-into-quota-repo | 0 | - |
| NAME | agent-usage-ledger | **3** | astra, sol, opus |
| NAME | fleet-ledger | **2** | fable, sonnet |
| NAME | agent-fleet-ledger | 0 (2 as explicit runner-up: fable, opus) | - |
| NAME | fleet-economics | 0 (4 actively reject: astra, sol, opus, sonnet) | - |
| NAME | ai-fleet-ledger | 0 | - |
| RENAME | no | **5** | all |
| RENAME | yes | 0 | - |

No lane used `other:<name>`. All five candidates were taken as free on PyPI from the input docs; nobody
re-verified availability, and two lanes say to re-check before publishing.

### Bundling and gating noted by lanes

- **Decide now, apply after the merge** - opus is the most explicit: choose the name now because it is
  consumed at one point (`pyproject.toml`, which does not exist yet), but do the rename, package-directory
  move and `pyproject` in one pass *after* the lineage merge, or the three-way merge has to be resolved
  across a renamed tree. sol frames the same gate as "choosing the name now avoids packaging twice";
  sonnet calls the name choice reversible prep correctly ordered before `pyproject`.
- **LAYOUT and NAME are coupled through `fleet-economics`** - four lanes tie the separate-repo vote to
  reserving `fleet-economics` for an umbrella (thin repo, docs page, or just cross-links plus a shared
  GitHub topic) rather than spending it as a package name. This is a bundle: voting separate-repo is what
  frees the thesis name, and the umbrella is what replaces the monorepo's one surviving benefit.
- **Conditional NAME vote** - fable's `fleet-ledger` is explicitly conditional: switch to
  `agent-fleet-ledger` if the "fleet economics" framing is dropped before publish, or if a registry check
  at publish time shows `fleet-*` crowded by vehicle-fleet or cluster-tooling packages.
- **Distribution name vs entry point unbundled** - opus notes the console script need not equal the
  distribution name, which removes the length objection to the 18-character pick (long dist name, short
  `usage-ledger` command). This partly dissolves the 3-2 split rather than resolving it.
- **RENAME is gated on evidence, not closed** - astra says revisit only if observed adoption shows the
  harness-specific name obstructs the audience; several lanes say fix the undersold second-harness support
  with a keyword and a README line instead.
- **Ledger publication gated behind release work** - all five separate "decide the layout/name" from "ship
  the ledger". astra lists four gates, sol three; both insist the gates, not this vote, are the blocker.

---

## 3. Question matrix

### A. Layout

| Lane | Normalised position |
|---|---|
| oc-gpt-astra | Separate repo; the monorepo's premise is stale now that the quota repo is public, so create only the repo that is still missing; fold-in is the "worst match for scope" |
| oc-gpt-sol | Separate repo; with no shared code a monorepo's plumbing buys "mainly a common landing page"; fold-in is weakest for both audiences |
| cc-claude-fable | Separate repo; the monorepo was free only at one moment and that moment passed; fold-in rejected outright as the wrong name for a four-harness ledger |
| cc-claude-opus | Separate repo (M-H); the report's four "why two packages" reasons are really arguments for two repos; fold-in is "the worst of the three" |
| cc-claude-sonnet | Separate repo; follow "the fact on the ground, not the stale recommendation"; the monorepo case reduces to one README of thesis framing |

**Majority / dissent:** 5-0 separate-repo; no dissent. All five independently identify the same stale
premise (the monorepo was justified as free *because* no public repo existed yet, and one now does) and all
five cite the consolidation report's own counter-argument, which predicted the standalone ship. Convergence
is on the reasoning, not just the verdict. Zero votes for fold-into-quota-repo, and three lanes rank it
worst of three rather than merely second.

### B. Name

| Lane | Normalised position |
|---|---|
| oc-gpt-astra | `agent-usage-ledger` - names subject, activity and recordkeeping role; extra word earns "useful discrimination"; `fleet-economics` is a weak package identity |
| oc-gpt-sol | `agent-usage-ledger` - "clearest cold-read name"; fits all four harnesses and does not imply the user runs an orchestrated fleet |
| cc-claude-fable | `fleet-ledger` - short at every site it is typed, and it carries the frame the probe exists to test; runner-up `agent-fleet-ledger` |
| cc-claude-opus | `agent-usage-ledger` - each word does distinct work and it echoes the shipped `usage_*` tool namespace; `fleet-ledger` is "weakest ... on exactly the criterion the question foregrounds" |
| cc-claude-sonnet | `fleet-ledger` - the converging answer already in the report, 12 vs 18 characters, "once the PyPI description does the explaining" the extra words add no clarity |

**Majority / dissent:** 3-2 for `agent-usage-ledger` (astra, sol, opus) over `fleet-ledger` (fable,
sonnet). The split is not about facts - all five accept the same availability list and the same
harness-neutrality requirement - but about whether a package name must self-explain in isolation or may
lean on its registry summary. Secondary agreement is wide: 4 of 5 reject `fleet-economics` as a package
name and want it kept for the umbrella, all 5 reject `ai-fleet-ledger` (low-signal prefix), and
`agent-fleet-ledger` is the stated runner-up on both sides of the split (fable, opus) - the obvious
compromise if the vote has to be broken.

### C. Rename the quota MCP

| Lane | Normalised position |
|---|---|
| oc-gpt-astra | No; preserve the published identity; the genuine counter (it already covers a second harness) is answered by description and keywords, "not a migration during the demand probe" |
| oc-gpt-sol | No; the current name gives a stranger three facts - provider, purpose, protocol - and `fleet-quota` loses all three |
| cc-claude-fable | No, strong; the name is load-bearing in the shipped artefact (three console scripts, an env-var family, a snapshot path, the publisher binding, a README honesty line) |
| cc-claude-opus | No (H); a PyPI project name cannot be renamed in place, and `fleet-quota` would imply fleet-wide quota management the tool does not do |
| cc-claude-sonnet | No; real wired surface (scripts, env vars, module name, live integration) to churn "for a cosmetic family match"; family branding belongs at the thesis level |

**Majority / dissent:** 5-0 no. The only shared criticism of the current name is that it undersells
support for a second harness; all five treat that as a description-and-keywords fix. Three lanes add the
accuracy argument that a fleet-flavoured name would overclaim - the tool reports one account's windows and
does not aggregate across a fleet.

### D. Moot or premature?

| Lane | Normalised position |
|---|---|
| oc-gpt-astra | Not moot; gate the ledger's *publication*, not this decision; lists four release gates and flags that some blockers in the older report are already superseded |
| oc-gpt-sol | Not moot; "publication gates matter more than the layout vote"; run the quota probe now and track the two tools' outcomes separately |
| cc-claude-fable | Not moot; the real gap is the measurement clock - two clocks, each starting at its own PyPI release, since the halves now ship weeks apart |
| cc-claude-opus | Not moot but the ledger half is premature; decide the name now, apply after the merge; the actual critical path is the owner-only pending-publisher web step |
| cc-claude-sonnet | Not premature to decide, premature to treat the ledger as shippable; the 30-day clock starts per-tool at actual PyPI publish, and the quota tool's has not started either |

**Majority / dissent:** 5-0 that nothing makes the decision moot and 5-0 that the ledger is not ready to
ship (unpublishable history, no packaging metadata, unmerged lineages). One real disagreement hides inside
the agreement: **the 30-day probe has two proposed start dates.** fable and sonnet say the clock starts at
PyPI release, so the quota tool's clock has *not* started; opus reads the plan's "thirty days from publish"
against the GitHub publish date and says the probe's clock is already running on the quota tool alone. That
flips whether the window opened on 2026-10-03 or is still closed, and nobody reconciled it. 4 of 5 lanes
also warn against giving the ledger the remainder of the quota tool's window or recording an unshipped
ledger as a zero-demand result.

---

## 4. Unique findings

Raised by exactly one lane.

**cc-claude-sonnet**
- *Blast radius.* The ledger still needs a destructive history rewrite (orphan history or a filter tool).
  Running that inside a repo that also holds the already-public, already-tagged quota package means a
  mistake in the rewrite endangers a live artefact; a brand-new repo has "zero blast radius". Flagged by
  the lane itself as not present in either input doc. This is the only safety-shaped argument for
  separation in the whole round, and it is independent of every audience and trust argument the others use.

**cc-claude-opus**
- *A PyPI project name cannot be renamed in place* - you publish under a second name and the first lingers,
  which is a worse outcome than one honest name. This is the only irreversibility argument on question C.
- *Critical path is not this decision.* The highest-value next action in the inputs is the owner-only
  pending-publisher web step, "a five-minute web form, not a repo-layout decision" - and every layout
  option that moves the repo or workflow path invalidates its coordinates and delays it further.
- *Namespace hop.* The shipped MCP tools are all `usage_*` and the live server is registered as `usage`, so
  `agent-usage-ledger` lets an agent get from a tool name to the package name without a hop. The sharpest
  version of the registry-reading test, and the only one grounded in the tool surface rather than intuition.
- *Entry point unbundling* - ship the long distribution name with a short console script, which removes the
  length objection the other side of the split relies on.
- *Transient stem collision* - a third internal lineage already carries the `agent-usage` stem, so the
  preferred name sits next to a same-stemmed directory during the merge window.

**cc-claude-fable**
- *"Fleet" is literal, not marketing.* The ledger pools across machines as well as harnesses (pooled
  aggregates, a machine label), so the word describes the data shape. The only evidential defence of
  `fleet-ledger` offered on either side.
- *A name that drops the frame does not test the frame.* The probe exists to test the "fleet economics"
  positioning, so choosing a name without "fleet" quietly changes what the experiment measures.
- *Count-agnostic naming* - the ledger may ship with five harness readers rather than four, so avoid
  anything that hard-codes the count.
- *Shared GitHub topic* as the zero-cost substitute for the monorepo's single README, with an umbrella repo
  added later only if the probe returns a positive signal.
- *Only git installs are countable today*, because the PyPI step is pending and the `uvx` path does not
  resolve - a measurement consequence nobody else draws.

**oc-gpt-astra**
- *The report's trust description is stale too.* Other lanes flag only the repo-existence premise as
  superseded; astra also flags that the older report describes credential-based quota access while the
  current README makes local snapshots the default and the network endpoint explicit opt-in.
- *A fresh repo does not sanitise the files copied into its first commit* - review both the public tree and
  the built distributions before publishing, not just the history.
- *Cost-language discipline* - keep API-equivalent valuation distinct from actual subscription charges; the
  export schema already separates equivalent, cash and implied cost, so do not present computed prices as
  money spent.
- *Symmetric inference* - quota failure does not refute ledger demand any more than quota success proves it.

**oc-gpt-sol**
- *Use synthetic examples in the public tree and preserve the private archive separately*, rather than
  treating deletion from the tip commit as sanitisation.
- *Three-facts framing* of the existing quota name (provider, purpose, protocol) as the concrete cost of a
  family rename.

**Correction to one expected unique finding.** The PyPI pending-publisher binding is *not* a single-lane
item: opus, fable and sonnet all three state the trusted-publisher registration is keyed to the repository
name and workflow path (opus and fable also name the `pypi` environment), and astra and sol refer to it
more loosely as name-specific publishing configuration. What is unique to opus is the *consequence* drawn
from it - that a project name cannot be renamed in place, and that the binding makes the pending web step,
not the layout, the critical path.

---

## 5. Family effect

**No clustering on the only contested question - and the contested one splits the facilitator's own
family.** The facilitator is Claude, so the three Claude lanes are same-family with it. On LAYOUT and
RENAME there is nothing to measure: all five lanes agree 5-0, so no family signal can be extracted. On
NAME, the two GPT lanes agree with each other (`agent-usage-ledger`, both of them) while the three Claude
lanes split 2-1 (`fleet-ledger`, `fleet-ledger`, `agent-usage-ledger`). The one Claude lane that breaks
ranks lands on the GPT answer, so the 3-2 majority is cross-family and the only internally divided family
is the facilitator's. That is the opposite of the failure mode this check exists to catch.

Factual texture, stated without over-reading five data points. The two Claude lanes that pick
`fleet-ledger` are also the two lanes that take the consolidation report's own recommendation as a starting
point and ask whether events have overtaken it - which is consistent with their choosing the report's name;
the GPT lanes and the dissenting Claude lane each derive the name from first principles against the
question's four criteria and arrive at the same place independently. Style differences track the harness
more than the family: both GPT lanes volunteer an explicit epistemic footer (no code, tests, network or
images consulted; availability accepted from inputs rather than re-verified) and both hedge the name as a
semantic judgment with no measured discovery evidence; the Claude lanes instead cite line numbers and
quote the input docs directly, and two of them reconstruct a same-day timeline. Those are presentation
habits, not positions. The Claude lanes are longer on average (10,153 bytes vs 9,185) and produced both
the longest and the shortest answer in the round, so length does not separate the families either. With
n=5 and a 5-0 result on two of three keys, none of this supports a claim about family bias in either
direction; the useful observation is simply that the one split available did not fall along family lines.

---

## 6. Executive read

1. Unanimous and safe to act on: the ledger gets its own fresh repo (5-0), the public quota tool keeps its
   name (5-0), and the ledger is nowhere near shippable - unmerged lineages, an unpublishable history and
   no packaging metadata all sit upstream of this vote.
2. Every lane independently found the same stale premise: the monorepo was recommended *because* no public
   repo existed to preserve, one now does, so the option that was free has a price and nobody will pay it.
3. The split is the package name, 3-2 for `agent-usage-ledger` (both GPT lanes plus one Claude lane) over
   `fleet-ledger` (two Claude lanes) - a difference of naming philosophy, not of evidence.
4. Strongest case for `agent-usage-ledger`: it is the only candidate that resolves two heavily pre-owned
   words and it echoes the tool namespace the project already ships (`usage_*`), so a stranger agent reads
   it correctly cold and reaches the package from a tool name without a hop - and the length objection
   dissolves if the console script is shortened independently.
5. Strongest case for `fleet-ledger`: the probe exists to test the "fleet economics" framing, a name
   without "fleet" does not test it, "fleet" is literally true of the data (it pools across machines), and
   the name is short at every site it is typed - import, console script, MCP server name.
6. The tiebreaker nobody voted for is `agent-fleet-ledger`, named as runner-up by one lane on each side;
   and the unresolved item worth more than the name is the probe's clock, which has two proposed start
   dates (GitHub publish vs PyPI release) and so is either already running or not yet open.
