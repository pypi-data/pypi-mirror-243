import json
import sys

with open("/input/validation/validation-report.json", "r") as f:
    report = json.load(f)

if "report" in report and "outcome" in report["report"]:
    outcome = report["report"]["outcome"]
    if outcome == "PASSED":
        sys.exit(0)
    else:
        print("Validation failed", file=sys.stderr)
        sys.exit(1)
else:
    print("Cannot parse outcome of validation report", file=sys.stderr)
    sys.exit(1)
