from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "examples/ecom/refund-task.json"
OUT = ROOT / "examples/ecom/output.commit.json"
sys.path.insert(0, str(ROOT))

from pvcore import Goal, run_pvcore  # noqa: E402


def main() -> None:
    data = json.loads(TASK.read_text(encoding="utf-8"))
    result = run_pvcore(Goal.from_dict(data["goal"]), data["witnesses"])
    OUT.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"pvcore_ecom_refund.output={OUT}")
    print(f"pvcore_ecom_refund.status={result.to_dict()['status']}")


if __name__ == "__main__":
    main()
