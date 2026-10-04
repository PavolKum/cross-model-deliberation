# Run record: ledger repository layout and package name (2026-10-03)

The first run of the harness. Five lanes, two rounds, twelve minutes, zero relaunches. Start with `decision.md`.

- `task-r1.md`: the round-one task body as the lanes received it. The three input documents it lists were local planning files and are not part of this repository; the lanes' answers quote the relevant parts.
- `round1/`: every lane's independent answer, `index.json` (task id, model, delivery, size), and `matrix.md` (the agreement matrix written by a separate subagent from the five answers).
- `round2/`: every lane's position note and vote block after reading the matrix and all peers, plus `votes.json` as parsed by the harness.
- `decision.md`: both tallies, what moved between rounds and why, dissent and residuals on record, harness defects found.

The round-two task body was rendered from `templates/task-r2.md`. Lane prompts, `run.json` and logs are not included because they carry bus session tokens.
