"""Export per-package mutation scores from mutmut's cache to mutation_scores.json.
Run via `make mutation`. Floors (mutation_floors.json) are updated by hand, deliberately:
raising a floor is a claim that the package's tests got stronger."""

import collections
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    out = subprocess.run(
        [sys.executable, "-m", "mutmut", "results", "--all", "true"],
        capture_output=True, text=True, cwd=ROOT,
    ).stdout
    per_pkg = collections.defaultdict(lambda: collections.Counter())
    for line in out.splitlines():
        m = re.match(r"\s*([\w.]+)\.x[^:]*: (\w+)", line)
        if m:
            per_pkg[m.group(1).split(".")[0]][m.group(2)] += 1
    if not per_pkg:
        sys.exit("no mutmut results found — run `mutmut run` first")

    scores = {}
    for pkg, c in sorted(per_pkg.items()):
        total = sum(c.values())
        killed = c.get("killed", 0) + c.get("timeout", 0)
        scores[pkg] = {"mutants": total, "killed": killed,
                       "survived": c.get("survived", 0),
                       "other": total - killed - c.get("survived", 0),
                       "kill_rate": round(killed / total, 3) if total else None}
    overall = {"mutants": sum(s["mutants"] for s in scores.values()),
               "killed": sum(s["killed"] for s in scores.values()),
               "survived": sum(s["survived"] for s in scores.values())}
    overall["kill_rate"] = round(overall["killed"] / overall["mutants"], 3)
    out_file = ROOT / "instrument" / "mutation_scores.json"
    json.dump({"tool": "mutmut", "note": "timeouts counted as caught; 'other' = not-run/skipped",
               "overall": overall, "packages": scores}, out_file.open("w"), indent=2)
    print(f"overall: {overall} -> {out_file}")


if __name__ == "__main__":
    main()
