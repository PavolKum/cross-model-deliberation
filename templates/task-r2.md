ROUND 2: debate and vote (read-only). You answered the task independently in round 1 (your task {{task_id_r1}}). All round-1 answers are now in {{round1_dir}} (one file per lane, filename = lane name; index.json lists them). The facilitator's agreement matrix is {{matrix_path}} (if that file is missing, build your own view from the raw answers).

Do this, in order:
1. Read the matrix first, then every round-1 file. Note where you are in the minority on each vote key ({{vote_keys}}). Note any factual corrections the matrix records.
2. Post ONE position note to the room: `working-note --kind progress` (pipe the body with --stdin from a temp file outside the workspace), at most 12 lines: what you now concede, what you still hold, and the single strongest argument against the current majority if you think it is wrong. Address peers by lane name.
3. Wait for peers once: `wait --timeout 150 --brief`, then `drain --since-join` and read any notes or `tell`s addressed to you. If a peer challenged you directly, reply with one `tell <lane>` (max 6 lines). Do not loop; one wait, one reply round. If the room is already quiet because peers finished earlier, skip the wait.
4. Vote. Deliver via task-done with EXACTLY these lines at the top, then up to 20 lines of reasoning:
VOTE {{vote_keys}}  (one line per key, in the form `VOTE <KEY>=<option>`, options exactly as the round-1 task defined them, or `other:<name>`)
CHANGED=<yes|no>: <one line on what moved you, or what did not>
CONFIDENCE=<H|M|L>
Then post `tell {{lead_agent}} "Round 2 vote in on task <id>"` and `leave --ack-pending "round 2 delivered"`.

Vote your honest judgment; a majority you cannot re-derive from the inputs is not a reason to join it, and say so if you suspect a cascade. Keep everything free of client, portfolio or named-person specifics and do not repeat an employer's name. Your only writes are bus commands.
