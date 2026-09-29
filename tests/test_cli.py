import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from csv_column_profiler.cli import profile_csv, value_type

class CsvProfilerTests(unittest.TestCase):
    def test_value_types(self):
        self.assertEqual(value_type("42"), "integer")
        self.assertEqual(value_type("3.14"), "number")
        self.assertEqual(value_type("2026-09-28"), "date")
        self.assertEqual(value_type("true"), "boolean")

    def test_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "people.csv"
            path.write_text("name,age,city\nAlice,30,Shanghai\nBob,40,\nChen,20,Shanghai\n", encoding="utf-8")
            report = profile_csv(path, encoding="utf-8")
            self.assertEqual(report["rows"], 3)
            self.assertEqual(report["columns"]["age"]["inferred_type"], "integer")
            self.assertEqual(report["columns"]["age"]["numeric"]["mean"], 30)
            self.assertEqual(report["columns"]["city"]["missing"], 1)

if __name__ == "__main__": unittest.main()
