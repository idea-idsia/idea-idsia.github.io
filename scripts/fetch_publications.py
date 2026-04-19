# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.28",
#   "pyyaml>=6.0",
# ]
# ///
"""
Fetch publications from OpenAlex for IDeA team members.

- Reads ORCIDs from _data/people/*.yml
- Tracks state in scripts/fetch_state.json (committed to repo)
- New authors → fetch all their works; existing authors → fetch since last run
- Deduplicates by title (exact then fuzzy Jaccard), preferring published over preprint
- Writes new publications to _publications/<slug>.md
"""

from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import argparse

import httpx
import yaml

# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
PEOPLE_DIR = REPO_ROOT / "_data" / "people"
PUBLICATIONS_DIR = REPO_ROOT / "_publications"
STATE_FILE = Path(__file__).parent / "fetch_state.json"

OPENALEX_BASE = "https://api.openalex.org"
POLITE_EMAIL = os.environ.get("OPENALEX_EMAIL", "idea@idsia.ch")

WORK_TYPE_MAP: dict[str, str] = {
    "article": "journal",  # refined via type_crossref below
    "preprint": "preprint",
    "book-chapter": "book-chapter",
    "book": "book",
    "dissertation": "thesis",
    "review": "journal",
    "report": "report",
    "journal-article": "journal",
    "proceedings-article": "conference",
}

_REPOSITORY_SOURCE_TYPES = {"repository", "ebook platform"}

_STOPWORDS = {
    "a",
    "an",
    "the",
    "of",
    "in",
    "on",
    "for",
    "and",
    "with",
    "to",
    "is",
    "are",
    "via",
}

# Minimum word-Jaccard score (ignoring stopwords) to treat two titles as the same work.
TITLE_SIMILARITY_THRESHOLD = 0.85


def _normalise_doi(doi: str) -> str:
    return doi.replace("https://doi.org/", "").strip().lower()


def _title_key(title: str) -> str:
    return re.sub(r"\W+", "", title.lower())


def _title_words(title: str) -> frozenset[str]:
    return frozenset(re.findall(r"[a-z0-9]+", title.lower())) - _STOPWORDS


def _title_jaccard(t1: str, t2: str) -> float:
    w1, w2 = _title_words(t1), _title_words(t2)
    if not w1 or not w2:
        return 1.0 if _title_key(t1) == _title_key(t2) else 0.0
    return len(w1 & w2) / len(w1 | w2)


def _work_type(work: dict) -> str:
    crossref_type = work.get("type_crossref") or ""
    openalex_type = work.get("type") or ""
    return WORK_TYPE_MAP.get(crossref_type) or WORK_TYPE_MAP.get(openalex_type, "other")


def _is_better(challenger: dict, incumbent: dict) -> bool:
    """Return True if challenger should replace incumbent for the same title slot.

    A published work always beats a preprint. Between two works of equal
    finality, the more recently published one wins.
    """
    c_preprint = _work_type(challenger) == "preprint"
    i_preprint = _work_type(incumbent) == "preprint"
    if c_preprint != i_preprint:
        return i_preprint  # challenger wins when the incumbent is the preprint
    return (challenger.get("publication_date") or "") > (
        incumbent.get("publication_date") or ""
    )


def _add_work(
    seen: dict[str, tuple[str | None, dict]], work: dict, doi: str | None
) -> None:
    """Insert work into seen, deduplicating against similar-titled entries."""
    title = work.get("title") or ""
    key = _title_key(title)

    # Fast path: exact normalised title match
    if key in seen:
        if _is_better(work, seen[key][1]):
            seen[key] = (doi, work)
        return

    # Slower path: fuzzy match against existing titles
    for ex_key, (_, ex_work) in seen.items():
        if (
            _title_jaccard(title, ex_work.get("title") or "")
            >= TITLE_SIMILARITY_THRESHOLD
        ):
            if _is_better(work, ex_work):
                seen[ex_key] = (doi, work)
            return

    if key:
        seen[key] = (doi, work)


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_run": None, "known_orcids": []}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# People & existing-publication readers
# ---------------------------------------------------------------------------


def get_people_orcids() -> dict[str, str]:
    """Return {orcid_id: display_name} for all people with ORCIDs."""
    orcids: dict[str, str] = {}
    for yml_file in sorted(PEOPLE_DIR.glob("*.yml")):
        data = yaml.safe_load(yml_file.read_text())
        if not data:
            continue
        raw = str(data.get("orcid") or "")
        match = re.search(r"(\d{4}-\d{4}-\d{4}-\d{3}[\dX])", raw)
        if match:
            orcids[match.group(1)] = data.get("name", "Unknown")
    return orcids


def get_existing_dois() -> set[str]:
    """Return normalised DOIs already present in _publications/."""
    dois: set[str] = set()
    for md in PUBLICATIONS_DIR.glob("*.md"):
        m = re.search(r"^doi:\s*['\"]?(.+?)['\"]?\s*$", md.read_text(), re.MULTILINE)
        if m and (doi := m.group(1).strip()):
            dois.add(_normalise_doi(doi))
    return dois


def get_existing_title_keys() -> set[str]:
    """Return normalised title keys already present in _publications/."""
    keys: set[str] = set()
    for md in PUBLICATIONS_DIR.glob("*.md"):
        m = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", md.read_text(), re.MULTILINE)
        if m:
            keys.add(_title_key(m.group(1)))
    return keys


def _openalex_get(path: str, params: dict | None = None) -> dict:
    params = {**(params or {}), "mailto": POLITE_EMAIL}
    resp = httpx.get(f"{OPENALEX_BASE}{path}", params=params, timeout=30)
    resp.raise_for_status()
    time.sleep(0.1)  # stay in the polite pool
    return resp.json()


def fetch_author_id(orcid: str) -> str | None:
    data = _openalex_get("/authors", {"filter": f"orcid:{orcid}"})
    results = data.get("results", [])
    if not results:
        print(f"  [warn] No OpenAlex record found for ORCID {orcid}")
        return None
    return results[0]["id"]


def fetch_works(author_id: str, from_date: str | None = None) -> list[dict]:
    """Cursor-paginated fetch of all works for an author."""
    filter_parts = [f"authorships.author.id:{author_id}"]
    if from_date:
        filter_parts.append(f"from_publication_date:{from_date}")

    works: list[dict] = []
    cursor = "*"
    while cursor:
        data = _openalex_get(
            "/works",
            {
                "filter": ",".join(filter_parts),
                "per-page": 200,
                "cursor": cursor,
                "sort": "publication_date:desc",
            },
        )
        works.extend(data.get("results", []))
        cursor = data.get("meta", {}).get("next_cursor")
    return works


def _reconstruct_abstract(inv: dict[str, list[int]]) -> str:
    """OpenAlex stores abstracts as inverted index {word: [positions]}."""
    words: dict[int, str] = {}
    for word, positions in inv.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words[i] for i in sorted(words))


def _extract_arxiv(work: dict) -> str:
    for loc in work.get("locations", []):
        landing = loc.get("landing_page_url") or ""
        if "arxiv.org" in landing:
            m = re.search(r"arxiv\.org/abs/(\d{4}\.\d+\w*)", landing)
            if m:
                return m.group(1)
    return ""


def work_to_frontmatter(work: dict) -> dict[str, Any] | None:
    title = (work.get("title") or "").strip()
    if not title:
        return None

    year = work.get("publication_year") or (work.get("publication_date") or "")[:4]
    if not year:
        return None

    authors = [
        a["author"]["display_name"]
        for a in work.get("authorships", [])
        if a.get("author", {}).get("display_name")
    ]

    # type_crossref distinguishes journal-article vs proceedings-article;
    # OpenAlex's own "article" type lumps both together.
    work_type = _work_type(work)
    if work_type == "other":
        for loc in work.get("locations", []):
            src_type = (loc.get("source") or {}).get("type", "")
            if src_type == "book series":
                work_type = "book-chapter"
                break
            if src_type == "conference":
                work_type = "conference"
                break

    # Prefer a non-repository source for venue (avoid institutional repos like Infoscience)
    venue = ""
    for loc in work.get("locations", []):
        src = loc.get("source") or {}
        if src.get("type") not in _REPOSITORY_SOURCE_TYPES and src.get("display_name"):
            venue = src["display_name"]
            break
    if not venue:
        primary = work.get("primary_location") or {}
        venue = (primary.get("source") or {}).get("display_name", "")

    doi = _normalise_doi(work.get("doi") or "")
    arxiv = _extract_arxiv(work)
    inv = work.get("abstract_inverted_index")
    abstract = _reconstruct_abstract(inv) if inv else ""
    best_oa = work.get("best_oa_location") or {}
    pdf = best_oa.get("pdf_url") or best_oa.get("landing_page_url") or ""
    tag_candidates = work.get("topics") or work.get("concepts") or []
    tags = [t["display_name"] for t in tag_candidates[:6] if t.get("display_name")]

    fm: dict[str, Any] = {
        "layout": "publication",
        "title": title,
        "authors": authors,
        "year": int(year),
        "type": work_type,
    }
    for field, value in [
        ("venue", venue),
        ("abstract", abstract),
        ("doi", doi),
        ("arxiv", arxiv),
        ("pdf", pdf),
    ]:
        if value:
            fm[field] = value
    if tags:
        fm["tags"] = tags

    return fm


def make_filename(fm: dict) -> str:
    year = fm.get("year", "0000")
    authors: list[str] = fm.get("authors", [])
    last_name = re.sub(
        r"[^a-z0-9]", "", (authors[0].split()[-1] if authors else "unknown").lower()
    )

    sig = [
        w.lower()
        for w in re.findall(r"[a-zA-Z0-9]+", fm.get("title", ""))
        if w.lower() not in _STOPWORDS
    ]
    slug_word = sig[0] if sig else "paper"

    base = f"{last_name}{year}{slug_word}"
    candidate = f"{base}.md"
    suffix = ord("a")
    while (PUBLICATIONS_DIR / candidate).exists():
        candidate = f"{base}{chr(suffix)}.md"
        suffix += 1
    return candidate


def write_publication(fm: dict) -> Path:
    path = PUBLICATIONS_DIR / make_filename(fm)
    path.write_text(
        f"---\n{yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)}---\n",
        encoding="utf-8",
    )
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch publications from OpenAlex.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Fetch all publications regardless of last-run date.",
    )
    parser.add_argument(
        "--orcid",
        metavar="ORCID",
        nargs="+",
        help="Only process these ORCID(s) instead of all people on file.",
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

    existing_dois = get_existing_dois()
    existing_title_keys = get_existing_title_keys()

    # Collect all works across authors into a single title-keyed dict,
    # deduplicating on the fly. Title is the dedup key because the same
    # paper can appear as a preprint and a journal article with different DOIs.
    seen: dict[str, tuple[str | None, dict]] = {}

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
            continue

        works = fetch_works(author_id, from_date)
        print(f"    {len(works)} work(s) returned by OpenAlex")

        for work in works:
            doi = _normalise_doi(work.get("doi") or "") or None
            _add_work(seen, work, doi)

    # Keep only works not already on disk (checked by both DOI and title).
    new_works = [
        work
        for title_key, (doi, work) in seen.items()
        if (doi is None or doi not in existing_dois)
        and title_key not in existing_title_keys
    ]

    print(f"\n{len(new_works)} new publication(s) to write.")

    written = 0
    for work in new_works:
        fm = work_to_frontmatter(work)
        if fm:
            path = write_publication(fm)
            print(f"  + {path.name}")
            written += 1

    print(f"\nDone. Wrote {written} file(s).")

    # Only advance state when running normally (not a targeted/forced re-fetch).
    if not args.force and not args.orcid:
        state["last_run"] = datetime.now(timezone.utc).date().isoformat()
        state["known_orcids"] = list(set(known_orcids) | people.keys())
        save_state(state)
        print("State saved.")


if __name__ == "__main__":
    main()
