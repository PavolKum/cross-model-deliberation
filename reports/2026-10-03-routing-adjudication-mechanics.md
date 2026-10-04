# The hand-driven eight-lane run (2026-10-03): mechanics and measurements

This is the run the harness was built from. The question was a private resource-allocation decision, so its content is not published; the mechanics, counts and failure modes are. Everything below comes from the bus event log, the lane logs and the launcher receipts of that day.

## Setup

| Item | Value |
|---|---|
| Lanes | 8: GPT 6 Astra (xhigh), GPT 6.1 Sol (xhigh), Gemini 3.1 Pro, Gemini 3.8 Flash, Grok 4.7, Claude Fable 5.1, Claude Opus 5.5, Claude Sonnet 5.5 |
| Routing | GPT lanes on the OpenAI endpoint via OpenCode; Claude and Gemini lanes via OpenRouter prepaid credits; Grok via OpenRouter |
| Facilitator | one Claude Code session, which also held a position of its own, recorded as a labelled column outside the counts |
| Rounds | round one blind and independent; round two with the agreement matrix and all eight answers visible, position notes exchanged on the bus, then a fixed vote block |
| Vote keys | four, each with a closed option list |
| Wall-clock | about 50 minutes across both rounds, plus recoveries |

## Round one: 8 of 8 delivered

- Delivered on first launch: 5 of 8, between 4 and 9 minutes each.
- Two lanes (Opus and Sonnet via OpenRouter) never joined. They had been launched with `--variant high`; relaunched without the flag they delivered in under three minutes.
- One lane (Gemini Pro) joined but answered an older, closed task. Redirected and relaunched.
- One lane joined under the harness's generic identity before correcting itself.
- Five of eight lanes independently flagged the same factual error in the facilitator's brief. The brief was corrected before round two.
- The facilitator's own pick lost 6 to 7 of 8 on the two main keys.

## Round two: 7 of 7 delivered

- Three lanes (Gemini Pro, Fable, Sonnet) stalled mid-run with "Insufficient credits" when the OpenRouter prepaid balance ran out. Every lane on the OpenAI endpoint delivered.
- The operator set the roster rule on the spot: subscription-backed lanes only. Fable and Sonnet re-ran as Claude Code subagents and delivered; Gemini Pro was dropped from the roster and its round-one answer kept in the matrix.
- 5 of 7 lanes changed at least one vote after reading peers. The two lanes that held were already the round-one majority.
- Final tally: unanimous on all four keys among the seven delivered lanes. The facilitator withdrew its position in writing.
- Process caveat raised by one lane (Sonnet): the near-unanimity looked partly like an information cascade, with later lanes citing and conceding to the two earliest answers rather than re-deriving. Partial counter-evidence: one of the switches cited a primary document rather than a peer. The decision was recorded as a strong majority with one acknowledged cascade risk, medium confidence.

## Heavyweight versus lightweight launch, measured side by side

Same task, same workspace, same bus; one extra GPT 6.1 Sol lane was launched through a supervised read-only launcher for comparison.

### Lightweight: raw `opencode run` plus bus commands in the prompt

| Measure | Result |
|---|---|
| Setup | about 10 minutes to write the launcher and the prompt template, reusable |
| Delivered on first launch | 5 of 8 |
| Failures | two silent exits (variant flag), one wrong-task answer, one generic identity |
| Logs | empty: stdout of detached `.cmd` children was lost; relaunches as foreground children logged normally |
| Enforcement | none beyond the prompt. "Read-only" is a request, not a boundary. No attestation of workspace state. |

### Heavyweight: supervisor plus read-only launcher

| Measure | Result |
|---|---|
| Setup | about 15 minutes: find the manifest format, write and validate it, pre-assign exactly one task |
| Attempt 1 | failed in 41 s: model exited before emitting readiness, stderr "The system cannot find the file specified". The launcher had resolved the npm `opencode.cmd` shim; the typed task packet travels as one argv string, so the `.cmd` transport is a second place the Windows 8 KB command-line limit bites. Fixed by passing the native `opencode.exe`. |
| Attempt 2 | model ran 407 s, exit 0, produced an 11.2 KB answer. Task bridge status `attestation_failed`: 10 workspace paths changed during the run, written by the facilitator lane. The result was not proposed to the bus; the launcher left cleanly and wrote its receipt. |
| Enforcement delivered | deny-by-default tool policy (read, glob, grep, list, lsp only), parent-owned join and leave, token redaction, before/after workspace hash, required completion marker, two-phase task commit |
| Answer quality | consistent with the lightweight majority; recovered from the launcher's stdout log and labelled as uncommitted |

### What this says

1. **The heavyweight path did exactly what it promises, and that is why it blocked.** Whole-workspace attestation is incompatible with a workspace where other lanes or the facilitator write during the run. Supervised lanes need a quiescent worktree per lane, or an attestation scope limited to the lane's declared inputs. The packet should be the attested object, not the repository.
2. **The lightweight path scales but lies about state.** Eight lanes in parallel with zero ceremony, but three of eight needed human-in-the-loop recovery, output was lost, and "read-only" was unenforced. Acceptable for an adjudication where nothing is written. Not acceptable for a review that gates a merge.
3. **Two Windows-specific traps, both now known:** `--variant` on OpenRouter-hosted Anthropic models kills the lane silently; the npm `.cmd` shim should never be the launcher's binary when the prompt is large.
4. **A swarm dies on prepaid credits, not on subscription quota.** Three lanes went down together when one balance hit zero; none of the subscription lanes did. That is the reason for the roster rule.
5. **Recommended hybrid:** lightweight dispatch for the fan-out, heavyweight launcher for each lane whose output gates something, each in a per-lane worktree containing only the frozen inputs, so attestation passes by construction and the receipt carries the hash of the exact inputs.

## What the harness in this repository changed as a result

Join check at two minutes with one relaunch without the variant; foreground children with stdout to a log file; the task id repeated in every prompt with "ignore any other task"; the lane name in every bus command; facilitator re-join before each round; the subscription-only roster as data. The first harnessed run (`runs/2026-10-03-ledger-naming/`) needed zero relaunches.
