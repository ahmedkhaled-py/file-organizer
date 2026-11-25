#!/usr/bin/env python3
"""Organize files in a folder into subfolders by type (or by date).

Usage:
    python organize.py /path/to/folder [--by-date] [--dry-run]
"""
import argparse
import logging
import shutil
from datetime import datetime
from pathlib import Path

CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".xlsx", ".pptx", ".csv"},
    "audio": {".mp3", ".wav", ".flac", ".ogg"},
    "video": {".mp4", ".mkv", ".mov", ".avi"},
    "archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "code": {".py", ".js", ".html", ".css", ".json", ".sql"},
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("organize")


def category_for(path: Path) -> str:
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return "other"


def target_folder(path: Path, by_date: bool) -> str:
    if by_date:
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        return mtime.strftime("%Y-%m")
    return category_for(path)


def organize(folder: Path, by_date: bool = False, dry_run: bool = False) -> int:
    moved = 0
    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue
        dest_dir = folder / target_folder(item, by_date)
        dest = dest_dir / item.name
        if dest.exists():
            log.warning("skip %s (already exists at destination)", item.name)
            continue
        log.info("%s -> %s/", item.name, dest_dir.name)
        if not dry_run:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest))
        moved += 1
    return moved


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize a folder by file type or date.")
    parser.add_argument("folder", type=Path, help="Folder to organize")
    parser.add_argument("--by-date", action="store_true", help="Group by YYYY-MM instead of type")
    parser.add_argument("--dry-run", action="store_true", help="Show what would move, move nothing")
    args = parser.parse_args()

    if not args.folder.is_dir():
        parser.error(f"{args.folder} is not a directory")
    moved = organize(args.folder, args.by_date, args.dry_run)
    log.info("done: %d file(s) %s", moved, "would move" if args.dry_run else "moved")


if __name__ == "__main__":
    main()
