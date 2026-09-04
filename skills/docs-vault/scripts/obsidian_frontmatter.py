"""Add Obsidian-compatible YAML frontmatter to markdown files in a `docs/` vault.

Drop this into a repo's `scripts/` (or run in place) to make `docs/` (including
`docs/plans/`) double as an Obsidian vault — graph view, backlinks, tag search,
Properties panel — without changing a single byte of how it renders on GitHub,
mkdocs, or a GitHub wiki mirror.

Rules
-----
* Files that already have frontmatter are left byte-identical (reported as skipped).
* Body content is never touched — only a block is prepended.
* Excluded by default: ``docs/wiki/**`` (GitHub's wiki renderer prints frontmatter
  as raw text) and ``docs/knowledge/**`` (a graphify export — gitignored, a
  regenerable local cache, never vault content; see the ``graphify-vault`` skill).
* Idempotent: a second run makes zero changes; ``--check`` exits non-zero if any
  file would change (CI / pre-commit gate).

Usage
-----
    uv run python scripts/obsidian_frontmatter.py            # write
    uv run python scripts/obsidian_frontmatter.py --check    # CI gate
    uv run python scripts/obsidian_frontmatter.py --verbose  # list every outcome
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess  # noqa: S404 - fixed argv, no shell, resolved git path
import sys
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[1]

#: Directories scanned for markdown, relative to the repo root.
SCAN_ROOTS: tuple[str, ...] = ("docs",)

#: Directory prefixes excluded outright (POSIX, relative to the repo root).
EXCLUDED_DIRS: tuple[str, ...] = ("docs/wiki", "docs/knowledge")

#: Individual files excluded (POSIX, relative to the repo root).
EXCLUDED_FILES: frozenset[str] = frozenset({"CHANGELOG.md"})

FRONTMATTER_FENCE = "---"
HEADING_RE = re.compile(r"^#\s+(?P<text>.+?)\s*#*\s*$")
#: YAML plain scalars we refuse to emit unquoted (ambiguous or reserved).
UNSAFE_TITLE_RE = re.compile(r"^[\s>|&*!%@`\[\]{}#'\"-]|[:#]\s|[:]$|[\n\r\t]|\s$")
YAML_RESERVED = frozenset({"true", "false", "null", "yes", "no", "on", "off", "~", ""})


@dataclass(frozen=True)
class Result:
    """Outcome for a single markdown file."""

    path: str
    action: str  # "converted" | "skipped"
    reason: str


def iter_markdown_files(roots: Sequence[str]) -> Iterator[Path]:
    """Yield eligible markdown files under *roots*, sorted, exclusions applied."""
    for root in roots:
        base = REPO_ROOT / root
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            if is_excluded(path):
                continue
            yield path


def relative_posix(path: Path) -> str:
    """Return *path* relative to the repo root, as a POSIX string."""
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def is_excluded(path: Path) -> bool:
    """True when *path* must never be rewritten."""
    rel = relative_posix(path)
    if rel in EXCLUDED_FILES:
        return True
    return any(rel.startswith(f"{prefix}/") for prefix in EXCLUDED_DIRS)


def has_frontmatter(text: str) -> bool:
    """True when *text* already opens with a YAML frontmatter fence."""
    return text.startswith(f"{FRONTMATTER_FENCE}\n") or text.startswith(f"{FRONTMATTER_FENCE}\r\n")


def derive_title(text: str, path: Path) -> str:
    """First ``# `` heading, else the file stem title-cased."""
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            return match.group("text").strip()
    words = re.split(r"[-_\s]+", path.stem)
    return " ".join(word[:1].upper() + word[1:] for word in words if word)


def derive_tags(path: Path) -> list[str]:
    """Path segments (minus the filename) become tags: ``docs/internal/ui/x.md`` → 3 tags."""
    parts = Path(relative_posix(path)).parts[:-1]
    tags: list[str] = []
    for part in parts:
        tag = re.sub(r"[^a-z0-9_-]+", "-", part.lower()).strip("-")
        if tag and tag not in tags:
            tags.append(tag)
    return tags


def git_last_commit_date(path: Path) -> str | None:
    """Committer date of the newest commit touching *path* (``YYYY-MM-DD``)."""
    git = shutil.which("git")
    if git is None:
        return None
    completed = subprocess.run(  # noqa: S603 - fixed argv, no shell, absolute git path
        [git, "log", "-1", "--format=%cs", "--", relative_posix(path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    stamp = completed.stdout.strip()
    return stamp or None


def derive_updated(path: Path) -> str:
    """Last git commit date, falling back to the file's mtime (new/untracked files)."""
    stamp = git_last_commit_date(path)
    if stamp:
        return stamp
    # Local time, to match git's `%cs` (committer-local date) rather than drift a day in UTC.
    mtime = datetime.fromtimestamp(path.stat().st_mtime).astimezone()
    return mtime.date().isoformat()


def yaml_scalar(value: str) -> str:
    """Emit *value* as a YAML scalar, quoting only when a plain scalar is unsafe."""
    if value.lower() in YAML_RESERVED or UNSAFE_TITLE_RE.search(value):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    try:
        float(value)
    except ValueError:
        return value
    return f'"{value}"'


def build_frontmatter(title: str, tags: Sequence[str], updated: str) -> str:
    """Render the frontmatter block, trailing newline included."""
    tag_list = ", ".join(tags)
    return (
        f"{FRONTMATTER_FENCE}\n"
        f"title: {yaml_scalar(title)}\n"
        f"tags: [{tag_list}]\n"
        f"updated: {updated}\n"
        f"{FRONTMATTER_FENCE}\n\n"
    )


def read_text(path: Path) -> str:
    """Read *path* preserving its original line endings."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    """Write *text* verbatim — no newline translation."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def process_file(path: Path, *, check_only: bool) -> Result:
    """Prepend frontmatter to *path* unless it already has some."""
    rel = relative_posix(path)
    text = read_text(path)
    if has_frontmatter(text):
        return Result(rel, "skipped", "already has frontmatter")
    if not text.strip():
        return Result(rel, "skipped", "empty file")

    block = build_frontmatter(derive_title(text, path), derive_tags(path), derive_updated(path))
    if not check_only:
        write_text(path, block + text)
    return Result(rel, "converted", "frontmatter added")


def summarize(results: Sequence[Result], *, verbose: bool, check_only: bool) -> None:
    """Print a per-file listing (verbose) plus grouped counts."""
    label = "would-add" if check_only else "converted"
    converted = [r for r in results if r.action == "converted"]
    skipped = [r for r in results if r.action == "skipped"]
    if verbose:
        for result in results:
            action = label if result.action == "converted" else result.action
            print(f"  {action:<9} {result.path} ({result.reason})")
    reasons: dict[str, int] = {}
    for result in skipped:
        reasons[result.reason] = reasons.get(result.reason, 0) + 1
    print(f"scanned: {len(results)}  {label}: {len(converted)}  skipped: {len(skipped)}")
    for reason, count in sorted(reasons.items()):
        print(f"  skipped — {reason}: {count}")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report only; exit 1 if any file would change (no writes)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="list every scanned file and its outcome",
    )
    parser.add_argument(
        "--root",
        action="append",
        dest="roots",
        metavar="DIR",
        help=f"directory to scan, repeatable (default: {', '.join(SCAN_ROOTS)})",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point: returns a process exit code."""
    args = parse_args(argv)
    roots: Sequence[str] = tuple(args.roots) if args.roots else SCAN_ROOTS
    results = [process_file(path, check_only=args.check) for path in iter_markdown_files(roots)]
    summarize(results, verbose=args.verbose, check_only=args.check)

    pending = [r for r in results if r.action == "converted"]
    if args.check and pending:
        print(f"\n{len(pending)} file(s) missing frontmatter — run without --check to fix:")
        for result in pending:
            print(f"  {result.path}")
        return 1
    if args.check:
        print("\nAll files carry frontmatter. Nothing to do.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
