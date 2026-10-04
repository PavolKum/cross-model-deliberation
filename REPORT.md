# Two-round cross-model review: two operational case studies

**Run date:** 3 October 2026. **Report revision:** 4 October 2026.

## Abstract

This report examines two uses of a human-facilitated, two-round multi-agent review process. Lanes were asked to answer independently, then inspect peer answers and a synthesized disagreement matrix before revising their votes. The later five-lane naming run has published final-answer artifacts: two lanes changed their naming preference, moving a 3–2 split to 5–0. The other two vote keys were unanimous before discussion. Its operator recorded 12 minutes from initialization to the final tally and zero relaunches. An earlier eight-lane run documents launch failures, a shared prepaid-balance failure, recovery and one dropped lane. These are operational observations, not a controlled evaluation of decision quality or efficiency.

## 1. Questions and evidence standard

The questions are: Where did the lanes disagree? What changed after peer review? Which execution failures required intervention? What can a reader verify from this release?

We distinguish three evidence classes:

| Class | Meaning | Examples |
|---|---|---|
| Artifact-recomputed | A reader can calculate the result from published final answers | Vote tallies, changed votes, answer-file counts |
| Operator-reported | Recorded in the contemporaneous decision or retrospective mechanics account, without public execution receipts | Elapsed time, relaunches, failure sequence, launcher behavior |
| Interpretation | A proposed explanation or design implication | Why votes moved, possible conformity, the case for isolated review inputs |

File presence demonstrates that an answer was published. It does not independently establish its delivery time, original execution path or adherence to the instructions. Lane explanations are evidence of their stated reasoning, not proof of the cause of a change.

## 2. Method and configurations

The process was:

1. Give each lane the task and request an independent first answer with explicit vote keys.
2. Collect answers and produce an agreement/disagreement matrix.
3. Expose the matrix and peer answers; allow bounded critique and a second vote.
4. Have the facilitator record the decision, reasons, dissent and process caveats.

Independence was requested in round one. No published access attestation establishes that peers were inaccessible. Round two deliberately permits influence through peer reasoning and the matrix. The facilitator controls the brief and synthesis; these are part of the intervention.

| Configuration | Earlier mechanics run | Later naming run |
|---|---|---|
| Task | Private resource-allocation decision; content omitted | Repository layout, package name and whether to rename a sibling tool |
| Initial lanes | 8 | 5 |
| Recorded model labels | GPT Astra/Sol; Gemini Pro/Flash; Grok; Claude Fable/Opus/Sonnet | GPT Astra/Sol; Claude Fable/Opus/Sonnet |
| Initial execution | GPT through OpenCode/OpenAI; other lanes through OpenRouter | GPT through OpenCode/OpenAI; Claude as Claude Code subagents |
| Vote keys | 4 | 3: LAYOUT, NAME, RENAME |
| Change between rounds | Brief corrected; two lanes rerouted; one dropped | Five final answers retained in both rounds |
| Published evidence | Operator mechanics narrative | Task, final answers, matrix, vote record, decision narrative |

Model labels are those recorded at the time, not a set of pinned, reproducible model snapshots. Both tasks were selected from the operator's own projects on the same day. They are not independent benchmark samples.

## 3. Naming run: results that can be recomputed

Source: [published naming run](runs/2026-10-03-ledger-naming/). Computation: [report_metrics.py](scripts/report_metrics.py).

| Vote key | Round one | Round two | Changed lane votes |
|---|---|---|---|
| LAYOUT | separate-repo: 5 | separate-repo: 5 | 0/5 |
| NAME | agent-usage-ledger: 3; fleet-ledger: 2 | agent-usage-ledger: 5 | 2/5 |
| RENAME | no: 5 | no: 5 | 0/5 |

There are five published final answers per round and three formal vote keys per answer: 30 vote observations across both rounds, with 15 paired lane-by-key comparisons. Two of those 15 comparisons changed. Two of five lanes changed at least one vote. Only one of three questions was initially disputed.

| Lane | NAME, round one | NAME, round two |
|---|---|---|
| oc-gpt-astra | agent-usage-ledger | agent-usage-ledger |
| oc-gpt-sol | agent-usage-ledger | agent-usage-ledger |
| cc-claude-fable | fleet-ledger | agent-usage-ledger |
| cc-claude-opus | agent-usage-ledger | agent-usage-ledger |
| cc-claude-sonnet | fleet-ledger | agent-usage-ledger |

Fable and Sonnet's final answers explain the switch in terms of existing naming conventions and the distinction between package names and command names. Both credit peer reasoning, including Opus's round-one namespace argument. These are inspectable reasons for reconsideration; they are not independently new evidence or proof that exposure to the majority had no effect. Opus recorded concessions on supporting arguments without changing a formal vote.

Reported headline confidence changed from one High/four Medium to five Medium. Confidence was self-assessed, and Fable changed its aggregation rule between rounds. This is not a calibrated measure of correctness or evidence that uncertainty decreased.

### Timing and intervention

The [decision record](runs/2026-10-03-ledger-naming/decision.md) gives initialization at 21:32, round-one delivery at 21:36, matrix completion at 21:40 and round-two delivery at 21:44. It reports 12 minutes and zero relaunches. These are **operator-reported** figures; the release has no raw timestamps or launch receipts with which to verify them. Zero relaunches does not mean zero human effort: briefing, launching subagents, synthesis and final judgment remained facilitated.

### Convergence is not a correctness result

The historical decision record says there was no cascade signature. The available evidence supports a narrower statement: the switching answers contain substantive reasons and self-reports about their influences. The claimed ordering of intermediate messages cannot be checked here, and would not exclude all influence paths even if verified. Round-one independence does not establish round-two independence. No naming-discovery experiment or downstream adoption outcome validates the final preference.

## 4. Earlier eight-lane run: reported operational outcomes

All results in this section come from the [operator's mechanics account](reports/2026-10-03-routing-adjudication-mechanics.md). Its underlying logs, receipts and task content are not included.

| Stage | Reported result | Denominator and qualification |
|---|---|---|
| Round-one first launch | 5/8 delivered | Three original lanes needed relaunch/recovery |
| Round-one eventual answers | 8/8 delivered | After operator intervention |
| Shared balance failure in round two | Three lanes affected | One prepaid account was a shared dependency |
| Round-two final answers | 7/7 retained lanes | 7/8 original lane slots; one dropped, two rerouted and rerun |
| Vote movement | 5/7 changed at least one vote | Retained lanes only; dropped lane's second-round preference is unknown |
| Final agreement | Unanimous on four keys among seven retained lanes | Does not establish agreement among the original eight |
| Timing | Approximately 50 minutes | Account says “across both rounds, plus recoveries”; exact boundary is unclear |

Reported failures included two nonjoining lanes launched with an unsupported variant option, one lane answering an older task, a generic lane identity, lost detached-child stdout and the shared prepaid-balance failure. Five of eight lanes reportedly identified the same factual error in the brief, which was corrected before round two. That input change is another possible explanation for vote movement.

One lane raised an information-cascade concern. The report also records a switch citing a primary document. Neither observation resolves whether the process improved the decision.

### Separate supervised-launcher attempt

The operator also launched an extra GPT Sol lane through a supervised read-only path on the same task. It is a separate attempt, outside the eight-lane and seven-lane denominators.

- First attempt: reported failure after 41 seconds, associated with the Windows `.cmd` launch path; the operator switched to the native executable.
- Second attempt: reported runtime of 407 seconds, exit code zero and answer production, followed by `attestation_failed` because ten workspace paths changed during execution. The account attributes those writes to the facilitator. The answer was withheld from submission to the bus and recovered separately.

This illustrates an operational distinction: **producing an answer, exiting successfully and having a result accepted are separate outcomes.** Without the receipts, hashes and logs, this release cannot independently verify the policy enforcement or attribution of those mutations. The case motivates evaluating isolated or narrowly attested inputs; it does not establish the supervisor's general reliability.

## 5. What these runs do and do not support

The naming run demonstrates an inspectable record of disagreement and revision. The mechanics account identifies concrete recovery work and a shared account dependency. Together they suggest useful design questions about input isolation, explicit task identity, output capture and acceptance checks.

They do **not** establish:

- A speedup from approximately 50 to 12 minutes. Tasks, lane counts, providers, routing, recovery and timing boundaries differ.
- Higher accuracy or better judgment than one strong model. There is no matched baseline, answer key or independent quality assessment.
- Lower cost. No comparable token totals, marginal cash costs, subscription allocations or human-effort measurements are published.
- That subscriptions are generally more reliable than prepaid access. One shared-balance incident motivated a local roster policy; it is not a provider reliability study.
- That open discussion necessarily causes conformity, or that requested blind first answers prevent it.
- That five lanes or two rounds are optimal. No alternative-size or alternative-protocol evaluation was conducted.

The historical records retain stronger language in places. This report qualifies those interpretations rather than treating them as measured results.

## 6. Reproduction and provenance limits

Run from the repository root with Python 3.11+:

```text
python scripts/report_metrics.py
python tests/test_swarm.py
```

The first command reads final answer vote blocks independently of the harness parser, requires exactly one value per key and confidence field, compares round-two values with the collector's JSON, and prints counts and changed votes. It uses only the Python standard library and does not launch agents or access the network. A mismatch fails the command.

The second command checks harness behavior without the bus or network. Passing it does not validate the historical executions.

The naming-run source inputs, rendered execution prompts, intermediate exchanges, launch logs and receipts are absent. The earlier run exposes only a narrative. The required coordination-bus implementation is not included. Consequently, readers can reproduce the published naming tallies, but cannot fully replay either original execution or evaluate every source-dependent argument.

The collector labels a text-length field `bytes` while computing Python `len(body)`, which counts characters. This report does not use those historical fields as byte, token, cost or quality measurements. They are preserved in the original records.

## 7. Next evaluation — proposed, not yet performed

Use a frozen, publishable input packet for each of several tasks with independently assessable outcomes. Compare a preselected single-model baseline with the same first-round lanes without peer discussion and with the two-round process. Repeat conditions, account for all launched lanes and preregister the scoring rules and treatment of failed runs. Evaluate outputs without revealing which condition produced them.

Record separately:

| Dimension | Measurement |
|---|---|
| Outcome quality | Correctness or a task-specific external rubric; preserved consequential errors and dissent |
| Time | Defined start/end events for end-to-end completion; setup and recovery time separately |
| Human effort | Active operator minutes and intervention count |
| Resources | Tokens where available; recorded cash spend separate from estimated or allocated costs |
| Reliability | First-attempt delivery, eventual delivery, accepted results and exclusions, all against original launch counts |
| Influence | Vote changes and source-grounded reasons; compare conditions with and without visible majority counts |

Publish sanitized event receipts, frozen input hashes, full configuration and final outputs. That would support a test of whether peer review adds value beyond parallel generation. The present repository establishes the observations and measurement gaps from which to design that test.
