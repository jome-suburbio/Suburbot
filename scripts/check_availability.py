from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from suburbot.availability_service import check_availability
from suburbot.config import load_env_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Consulta disponibilidad en Google Sheets.")
    parser.add_argument("--check-in", required=True, help="Fecha de llegada en formato YYYY-MM-DD")
    parser.add_argument("--check-out", required=True, help="Fecha de salida en formato YYYY-MM-DD")
    args = parser.parse_args()

    load_env_file()

    try:
        result = check_availability(args.check_in, args.check_out)
    except Exception as exc:
        print(f"[availability] {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
