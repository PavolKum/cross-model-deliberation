Build an agreement matrix from independent adjudication answers. Read-only on everything except the one output file.

Inputs: the files {{round1_dir}}/*.md (one per lane: {{lanes}}; a file that says "not delivered yet" is pending) and index.json in the same folder. The question set the lanes answered is {{task_path}}. The facilitator's own position, if any, is on the bus; include it only if the task names an event id, as a column labelled "{{lead_agent}}-lead (not a lane)" and excluded from every count.

Write exactly one file: {{matrix_path}} containing:
1. A header table: lane, model family, delivered yes/no, bytes, confidence stated.
2. Allocation table: lane x each vote key ({{vote_keys}}) with each pick normalised to the option names the task defined (or other:<short>), then the tally per option, and a note where a lane bundles or gates two options.
3. Question matrix: for each question in the task, one row per lane with a 1-line normalised position, then a "majority / dissent" line per question.
4. "Unique findings": points raised by exactly one lane, attributed.
5. "Family effect" paragraph: do same-family lanes cluster? Be factual; note that lanes from the facilitator's own family are same-family.
6. A 6-line executive read: what the swarm agrees on, where it splits, and what it rejects from the facilitator's position.

Quote lane text sparingly (max one short phrase per cell). Keep the output free of client, portfolio or named-person specifics and do not include an employer's name even if a lane wrote it. Return to the caller only: the tallies per vote key, and the file path.
