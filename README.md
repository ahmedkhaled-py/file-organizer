# file-organizer

A small command-line tool that tidies a messy folder by moving files into
subfolders — by type (images, documents, audio...) or by month (`2026-11`).

## Features

- Sorts into categories based on extension, or into `YYYY-MM` buckets by modification date
- `--dry-run` mode shows every move before touching anything
- Skips files that would overwrite an existing file, with a warning
- Logs every action; no dependencies beyond the Python standard library

## Usage

```bash
python organize.py ~/Downloads --dry-run     # preview
python organize.py ~/Downloads               # organize by file type
python organize.py ~/Downloads --by-date     # organize by month
```

## Example

```
$ python organize.py ~/Downloads
INFO: report.pdf -> documents/
INFO: photo.png -> images/
INFO: done: 2 file(s) moved
```

Requires Python 3.8+.
