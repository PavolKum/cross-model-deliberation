# Two-round cross-model deliberation

**An observational technical report on vote movement, delivery failures and human intervention in multi-agent deliberation.**

Two runs on 3 October 2026 requested independent first answers, then used an agreement matrix, peer critique and revised votes, followed by a human-directed decision. This repository publishes the findings, available evidence and supporting harness.

**[Read the technical report](REPORT.md)**

## Observed outcomes

| Outcome | Result | Evidence available here |
|---|---|---|
| Naming run: final answers | 5 lanes in each of 2 rounds | Ten published answer files |
| Naming preference | 3–2 split became 5–0 | Recomputed from answer vote blocks |
| Vote movement | 2/5 lanes; 2/15 lane-by-question votes changed | Recomputed across rounds; both changes concerned the name |
| Other naming-run questions | Repository layout and sibling rename were already unanimous | Recomputed from answer vote blocks |
| Naming-run elapsed time and relaunches | 12 minutes; 0 relaunches | Operator-reported; execution receipts are not published |
| Earlier eight-lane run | 5/8 first-launch deliveries; 7/8 original lane slots delivered in round two after recovery and one exclusion | Operator-reported mechanics account |

**These runs document vote movement and failures, not decision quality.** See the report for the evaluation limits.

## Inspect and reproduce

- [Technical report](REPORT.md): method, results, denominators, limitations and the next evaluation.
- [Naming-run evidence](runs/2026-10-03-ledger-naming/): task, final answers, matrix, collected votes and operator decision record.
- [Earlier mechanics account](reports/2026-10-03-routing-adjudication-mechanics.md): historical operator narrative, including the supervised-launcher attempt. See the technical report for qualifications to its original conclusions.
- [Harness instructions](docs/harness.md): requirements and operation; **the required local coordination bus is not included**, so this is not a turnkey installation.

Recompute the naming-run counts locally, with Python 3.11+ and no network or external packages:

```text
python scripts/report_metrics.py
```

The script reads the ten answer files, checks their vote blocks against the collected round-two record and prints JSON. It does not validate timings or replay the agents. Harness checks run separately:

```text
python tests/test_swarm.py
```

## Scope

The evidence release contains final answers, not full execution transcripts. Original source inputs, intermediate bus exchanges, rendered prompts, launch receipts and raw logs are not included. Live run configuration, prompts and logs can contain session tokens and remain excluded.

The historical records are preserved as written; [REPORT.md](REPORT.md) is the current synthesis. Code and documentation are under the [MIT license](LICENSE).
