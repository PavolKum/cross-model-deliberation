"""Recompute published naming votes; no agent execution or external dependencies."""

import json
from collections import Counter
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs" / "2026-10-03-ledger-naming"
KEYS = ("LAYOUT", "NAME", "RENAME")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def one_value(body, field, path):
    matches = re.findall(rf"^{re.escape(field)}\s*=\s*([^\s]+)\s*$", body, re.MULTILINE)
    if len(matches) != 1:
        raise ValueError(f"{path.name}: expected one {field}, found {len(matches)}")
    return matches[0]


def main():
    index = read_json(RUN / "round1/index.json")
    collected = read_json(RUN / "round2/votes.json")
    if set(index) != set(collected):
        raise ValueError("Round-one and round-two lane sets differ")

    rounds = {}
    for number, metadata in ((1, index), (2, collected)):
        folder = RUN / f"round{number}"
        answer_files = {p.stem for p in folder.glob("*.md") if p.name != "matrix.md"}
        if answer_files != set(index):
            raise ValueError(f"Round {number}: answer files do not match indexed lanes")
        lanes = {}
        for lane in sorted(index):
            if metadata[lane].get("delivered") is not True:
                raise ValueError(f"Round {number}: {lane} is not marked delivered")
            path = folder / f"{lane}.md"
            body = path.read_text(encoding="utf-8")
            votes = {key: one_value(body, f"VOTE {key}", path) for key in KEYS}
            confidence = one_value(body, "CONFIDENCE", path)
            if confidence not in {"H", "M", "L"}:
                raise ValueError(f"{path.name}: invalid confidence {confidence}")
            if number == 2:
                recorded = collected[lane]["votes"]
                for key in KEYS:
                    if votes[key] != recorded[key]:
                        raise ValueError(f"{lane}: {key} differs from collected vote")
                if confidence != recorded["confidence"]:
                    raise ValueError(f"{lane}: confidence differs from collected value")
            lanes[lane] = {"votes": votes, "confidence": confidence}
        rounds[number] = lanes

    changes = [
        {"lane": lane, "key": key,
         "before": rounds[1][lane]["votes"][key],
         "after": rounds[2][lane]["votes"][key]}
        for lane in sorted(index) for key in KEYS
        if rounds[1][lane]["votes"][key] != rounds[2][lane]["votes"][key]
    ]
    result = {
        "source": RUN.relative_to(ROOT).as_posix(),
        "evidence_class": "artifact-recomputed",
        "lanes": len(index),
        "vote_keys": list(KEYS),
        "rounds": {
            str(number): {
                "answer_files": len(lanes),
                "tallies": {key: dict(sorted(Counter(
                    item["votes"][key] for item in lanes.values()
                ).items())) for key in KEYS},
                "confidence": dict(sorted(Counter(
                    item["confidence"] for item in lanes.values()
                ).items())),
            } for number, lanes in rounds.items()
        },
        "vote_observations": sum(len(lanes) * len(KEYS) for lanes in rounds.values()),
        "paired_lane_key_comparisons": len(index) * len(KEYS),
        "changed_lanes": len({item["lane"] for item in changes}),
        "changed_lane_key_votes": len(changes),
        "changes": changes,
        "not_verified": ["execution timing", "relaunches", "independence",
                         "decision quality", "cost", "full execution replay"],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
