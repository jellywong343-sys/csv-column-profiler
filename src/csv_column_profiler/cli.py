from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean

DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S")


def detect_dialect(path: Path, encoding: str) -> csv.Dialect:
    sample = path.read_text(encoding=encoding)[:8192]
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        return csv.excel


def value_type(value: str) -> str:
    value = value.strip()
    if not value:
        return "empty"
    lowered = value.lower()
    if lowered in {"true", "false", "yes", "no"}:
        return "boolean"
    try:
        int(value)
        return "integer"
    except ValueError:
        pass
    try:
        float(value)
        return "number"
    except ValueError:
        pass
    for fmt in DATE_FORMATS:
        try:
            datetime.strptime(value, fmt)
            return "date"
        except ValueError:
            continue
    return "text"


def inferred_type(counts: Counter[str]) -> str:
    nonempty = {key: value for key, value in counts.items() if key != "empty"}
    if not nonempty:
        return "empty"
    if set(nonempty) <= {"integer"}:
        return "integer"
    if set(nonempty) <= {"integer", "number"}:
        return "number"
    if set(nonempty) <= {"boolean"}:
        return "boolean"
    if set(nonempty) <= {"date"}:
        return "date"
    if len(nonempty) == 1:
        return next(iter(nonempty))
    return "mixed"


def profile_csv(path: Path, top: int = 5, encoding: str = "utf-8-sig") -> dict:
    dialect = detect_dialect(path, encoding)
    with path.open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle, dialect=dialect)
        if not reader.fieldnames:
            raise ValueError("CSV has no header")
        fields = [name.strip() for name in reader.fieldnames]
        values = {field: [] for field in fields}
        rows = 0
        for raw in reader:
            rows += 1
            for original, field in zip(reader.fieldnames, fields):
                values[field].append((raw.get(original) or "").strip())
    columns = {}
    for field in fields:
        items = values[field]
        type_counts = Counter(value_type(item) for item in items)
        nonempty = [item for item in items if item != ""]
        numeric = [float(item) for item in nonempty if value_type(item) in {"integer", "number"}]
        lengths = [len(item) for item in nonempty]
        column = {
            "inferred_type": inferred_type(type_counts),
            "type_counts": dict(type_counts),
            "missing": len(items) - len(nonempty),
            "missing_percent": round((len(items) - len(nonempty)) * 100 / rows, 2) if rows else 0.0,
            "unique": len(set(nonempty)),
            "unique_percent": round(len(set(nonempty)) * 100 / len(nonempty), 2) if nonempty else 0.0,
            "top_values": Counter(nonempty).most_common(top),
            "min_length": min(lengths) if lengths else None,
            "max_length": max(lengths) if lengths else None,
        }
        if numeric and len(numeric) == len(nonempty):
            column["numeric"] = {"min": min(numeric), "max": max(numeric), "mean": mean(numeric)}
        columns[field] = column
    return {"file": str(path.resolve()), "rows": rows, "columns": columns}


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile CSV columns and data quality.")
    parser.add_argument("file")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--encoding", default="utf-8-sig")
    parser.add_argument("--json", dest="json_path")
    args = parser.parse_args()
    report = profile_csv(Path(args.file), args.top, args.encoding)
    print(f"Rows: {report['rows']}  Columns: {len(report['columns'])}")
    for name, column in report["columns"].items():
        print(f"\n{name}: {column['inferred_type']}")
        print(f"  Missing: {column['missing']} ({column['missing_percent']}%)")
        print(f"  Unique: {column['unique']} ({column['unique_percent']}%)")
        if "numeric" in column:
            number = column["numeric"]
            print(f"  Range: {number['min']} .. {number['max']}; mean={number['mean']:.2f}")
        print("  Top: " + ", ".join(f"{value!r} ({count})" for value, count in column["top_values"]))
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nJSON report written to {args.json_path}")

if __name__ == "__main__": main()
