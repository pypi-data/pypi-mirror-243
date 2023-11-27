import json
import shutil
import sys

with open("/input/validation/validation-report.json", "r") as f:
    report = json.load(f)

if "report" in report and "outcome" in report["report"]:
    outcome = report["report"]["outcome"]
    if outcome == "PASSED":
        shutil.copyfile("/input/validation/dataset.csv", "/output/dataset.csv")
        shutil.copyfile("/input/validation/types", "/output/types")
        sys.exit(0)
    else:
        print("Validation failed", file=sys.stderr)
        sys.exit(1)
else:
    print("Cannot parse outcome of validation report", file=sys.stderr)
    sys.exit(1)
