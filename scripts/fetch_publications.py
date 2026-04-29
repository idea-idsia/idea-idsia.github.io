# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.28",
#   "pyyaml>=6.0",
# ]
# ///
"""
Non-interactive CLI: fetch publications from OpenAlex for IDeA team members.

- Reads ORCIDs from _data/people/*.yml
- Tracks state in scripts/fetch_state.json (committed to repo)
- New authors → fetch all their works; existing authors → fetch since last run
- Writes new publications to _publications/<slug>.md

For an interactive experience use fetch_publications_tui.py instead.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from publications_lib import (
    _add_work,
    _normalise_doi,
    fetch_author_id,
    fetch_works,
    filter_new_works,
    get_existing_publications,
    get_people_orcids,
    load_state,
    save_state,
    work_to_frontmatter,
    write_publication,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch publications from OpenAlex.")
    parser.add_argument(
        "--force", action="store_true", help="Fetch all regardless of last-run date."
    )
    parser.add_argument(
        "--orcid", metavar="ORCID", nargs="+", help="Only process these ORCID(s)."
    )
    parser.add_argument(
        "--no-save-state", action="store_true", help="Do not update fetch_state.json."
    )
    args = parser.parse_args()

    state = load_state()
    known_orcids: list[str] = state.get("known_orcids", [])
    last_run: str | None = None if args.force else state.get("last_run")

    people = get_people_orcids()
    if not people:
        print("No ORCIDs found in _data/people/. Add 'orcid:' fields to member YAMLs.")
        return

    if args.orcid:
        requested = {
            re.search(r"(\d{4}-\d{4}-\d{4}-\d{3}[\dX])", o).group(1)  # type: ignore[union-attr]
            for o in args.orcid
        }
        people = {orcid: name for orcid, name in people.items() if orcid in requested}
        unknown = requested - people.keys()
        if unknown:
            print(f"[warn] ORCIDs not found in _data/people/: {', '.join(unknown)}")
        if not people:
            print("No matching ORCIDs found.")
            return

    print(
        f"Found {len(people)} author(s) with ORCIDs."
        + (" (forced full fetch)" if args.force else "")
    )

    existing_dois, existing_title_keys, existing_titles = get_existing_publications()
    seen: dict[str, tuple[str | None, dict, list[dict]]] = {}

    for orcid, name in people.items():
        is_new = orcid not in known_orcids
        from_date = None if (is_new or args.force) else last_run
        tag = (
            "all publications"
            if from_date is None
            else f"publications since {last_run}"
        )
        print(f"\n  {name} ({orcid}) — fetching {tag}")

        author_id = fetch_author_id(orcid)
        if not author_id:
            print(f"  [warn] No OpenAlex record found for ORCID {orcid}")
            continue

        works = fetch_works(author_id, from_date)
        print(f"    {len(works)} work(s) returned by OpenAlex")

        for work in works:
            doi = _normalise_doi(work.get("doi") or "") or None
            _add_work(seen, work, doi)

    new_groups = filter_new_works(
        seen, existing_dois, existing_title_keys, existing_titles
    )
    print(f"\n{len(new_groups)} new publication(s) to write.")

    written = 0
    for work, _alts in new_groups:
        fm = work_to_frontmatter(work)
        if fm:
            path = write_publication(fm)
            print(f"  + {path.name}")
            written += 1

    print(f"\nDone. Wrote {written} file(s).")

    if not args.force and not args.orcid and not args.no_save_state:
        state["last_run"] = datetime.now(timezone.utc).date().isoformat()
        state["known_orcids"] = list(set(known_orcids) | people.keys())
        save_state(state)
        print("State saved.")


if __name__ == "__main__":
    main()
