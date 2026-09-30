# CSV Column Profiler

[绠€浣撲腑鏂嘳(README.zh-CN.md)

Inspect CSV columns for inferred data types, missing values, uniqueness, ranges, and frequent values.

## Features

- Infers integer, number, boolean, date, text, mixed, or empty columns.
- Reports missing and unique percentages.
- Calculates numeric minimum, maximum, and mean.
- Shows common values and text length ranges.
- Exports a machine-readable JSON report.
- Reads data only and never modifies the source file.

## Install

```bash
git clone https://github.com/jellywong343-sys/csv-column-profiler.git
cd csv-column-profiler
python -m pip install -e .
```

## Usage

```bash
csv-profile examples/people.csv
csv-profile data.csv --top 10 --json profile.json
csv-profile legacy.csv --encoding gb18030
```

Type inference is a practical summary, not a formal schema guarantee. Always review results before changing production data.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT


