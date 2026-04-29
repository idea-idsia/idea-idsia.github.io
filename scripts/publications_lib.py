"""
Shared library for IDeA publication fetching.

Used by both the non-interactive CLI (fetch_publications.py)
and the interactive TUI (fetch_publications_tui.py).
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any

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
    "article": "journal",
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

# Minimum word-Jaccard score to treat two titles as the same work.
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

    A published work always beats a preprint; between equals the newer one wins.
    """
    c_preprint = _work_type(challenger) == "preprint"
    i_preprint = _work_type(incumbent) == "preprint"
    if c_preprint != i_preprint:
        return i_preprint
    return (challenger.get("publication_date") or "") > (
        incumbent.get("publication_date") or ""
    )


def _add_work(
    seen: dict[str, tuple[str | None, dict, list[dict]]], work: dict, doi: str | None
) -> None:
    """Insert work into seen, deduplicating against similar-titled entries."""
    title = work.get("title") or ""
    key = _title_key(title)

    if key in seen:
        doi_, main, alts = seen[key]
        if _is_better(work, main):
            seen[key] = (doi, work, [main] + alts)
        else:
            seen[key] = (doi_, main, alts + [work])
        return

    for ex_key, (_, ex_work, ex_alts) in seen.items():
        if (
            _title_jaccard(title, ex_work.get("title") or "")
            >= TITLE_SIMILARITY_THRESHOLD
        ):
            doi_, main, alts = seen[ex_key]
            if _is_better(work, main):
                seen[ex_key] = (doi, work, [main] + alts)
            else:
                seen[ex_key] = (doi_, main, alts + [work])
            return

    if key:
        seen[key] = (doi, work, [])


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_run": None, "known_orcids": []}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def get_people_orcids() -> dict[str, str]:
    """Return {orcid: display_name} for all people with ORCIDs."""
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


def get_existing_publications() -> tuple[set[str], set[str], list[str]]:
    """Return (normalised DOIs, title keys, raw titles) already on disk."""
    dois: set[str] = set()
    title_keys: set[str] = set()
    titles: list[str] = []
    for md in PUBLICATIONS_DIR.glob("*.md"):
        text = md.read_text()
        m = re.search(r"^doi:\s*['\"]?(.+?)['\"]?\s*$", text, re.MULTILINE)
        if m and (doi := m.group(1).strip()):
            dois.add(_normalise_doi(doi))
        m = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", text, re.MULTILINE)
        if m:
            title_keys.add(_title_key(m.group(1)))
            titles.append(m.group(1))
    return dois, title_keys, titles


def _openalex_get(path: str, params: dict | None = None) -> dict:
    params = {**(params or {}), "mailto": POLITE_EMAIL}
    resp = httpx.get(f"{OPENALEX_BASE}{path}", params=params, timeout=30)
    resp.raise_for_status()
    time.sleep(0.1)  # stay in the polite pool
    return resp.json()


def fetch_author_id(orcid: str) -> str | None:
    """Return the OpenAlex author ID for an ORCID, or None if not found."""
    data = _openalex_get("/authors", {"filter": f"orcid:{orcid}"})
    results = data.get("results", [])
    return results[0]["id"] if results else None


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


# ---------------------------------------------------------------------------
# Core filter
# ---------------------------------------------------------------------------


def filter_new_works(
    seen: dict[str, tuple[str | None, dict, list[dict]]],
    existing_dois: set[str],
    existing_title_keys: set[str],
    existing_titles: list[str],
) -> list[tuple[dict, list[dict]]]:
    """Return (main_work, alternatives) groups not already on disk."""
    new_groups: list[tuple[dict, list[dict]]] = []
    for title_key, (doi, work, alts) in seen.items():
        if doi and doi in existing_dois:
            continue
        if title_key in existing_title_keys:
            continue
        title = (work.get("title") or "").strip()
        if any(
            _title_jaccard(title, ex) >= TITLE_SIMILARITY_THRESHOLD
            for ex in existing_titles
        ):
            continue
        new_groups.append((work, alts))
    return new_groups
