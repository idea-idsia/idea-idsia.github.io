# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.28",
#   "pyyaml>=6.0",
#   "textual>=0.80",
# ]
# ///
"""
Interactive TUI for fetching IDeA publications from OpenAlex.

Flow:
  1. All authors are pre-selected — deselect any you want to skip.
  2. Press F to fetch.  The right panel fills with new publications.
  3. Deselect any papers you don't want, then press W to write them to disk.
  4. When duplicates are found, use ↳ rows and press P to promote an alt.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from publications_lib import (
    _add_work,
    _is_better,
    _normalise_doi,
    _work_type,
    _REPOSITORY_SOURCE_TYPES,
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

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Label, RichLog, SelectionList
from textual.widgets.selection_list import Selection


_TYPE_STYLE: dict[str, str] = {
    "journal": "bold green",
    "conference": "bold cyan",
    "preprint": "bold yellow",
    "book-chapter": "bold blue",
    "book": "bold blue",
    "thesis": "bold magenta",
    "report": "dim",
    "other": "dim",
}


def _pub_venue(work_item: dict) -> str:
    for loc in work_item.get("locations", []):
        src = loc.get("source") or {}
        if src.get("type") not in _REPOSITORY_SOURCE_TYPES and src.get("display_name"):
            return src["display_name"]
    primary = work_item.get("primary_location") or {}
    return (primary.get("source") or {}).get("display_name", "")


def _pub_label(work_item: dict, *, prefix: str = "") -> str:
    title = (work_item.get("title") or "Untitled").strip()
    year = work_item.get("publication_year") or ""
    wtype = _work_type(work_item)
    style = _TYPE_STYLE.get(wtype, "dim")
    venue = _pub_venue(work_item)
    venue_part = f"  [dim]{venue[:28]}[/dim]" if venue else ""
    avail = 52 - len(prefix)
    short = (title[:avail] + "…") if len(title) > avail else title
    return f"{prefix}{short}  [{style}]{wtype}[/{style}]  [dim]{year}[/dim]{venue_part}"


def _compare_line(main: dict, alt: dict) -> str:
    """One-line comparison shown in the log when an alt row is focused."""

    def _fmt(w: dict) -> str:
        wtype = _work_type(w)
        style = _TYPE_STYLE.get(wtype, "dim")
        venue = _pub_venue(w) or "no venue"
        year = w.get("publication_year") or "?"
        cit = w.get("cited_by_count")
        cit_part = f" · {cit} cit" if cit else ""
        doi = _normalise_doi(w.get("doi") or "")
        doi_part = " · DOI ✓" if doi else " · no DOI"
        return (
            f"[{style}]{wtype}[/{style}] · [dim]{venue[:30]}[/dim]"
            f" · {year}{cit_part}{doi_part}"
        )

    m_preprint = _work_type(main) == "preprint"
    a_preprint = _work_type(alt) == "preprint"
    alt_should_win = _is_better(alt, main)
    if m_preprint != a_preprint:
        reason = (
            "[bold yellow]alt is published — consider promoting (P)[/bold yellow]"
            if alt_should_win
            else "main is published · alt is preprint"
        )
    else:
        m_date = main.get("publication_date") or ""
        a_date = alt.get("publication_date") or ""
        if alt_should_win:
            reason = f"[bold yellow]alt is newer ({a_date} vs {m_date}) — consider promoting (P)[/bold yellow]"
        elif m_date != a_date:
            reason = f"main is newer ({m_date} vs {a_date})"
        else:
            reason = "same date"

    return (
        f"[dim]↕[/dim] main: {_fmt(main)}  "
        f"[dim]|[/dim]  alt: {_fmt(alt)}  "
        f"[dim]reason: {reason}[/dim]"
    )


@dataclass
class _PubItem:
    group_idx: int
    is_alt: bool
    alt_idx: int  # index within group's alts list; ignored when is_alt=False
    work: dict


class PublicationFetcherApp(App[None]):
    TITLE = "IDeA Publication Fetcher"
    SUB_TITLE = "OpenAlex → Jekyll"

    CSS = """
    Screen {
        layout: vertical;
    }

    #panels {
        height: 1fr;
    }

    #left {
        width: 36;
        border: tall $primary-darken-2;
        padding: 0 1;
    }

    #right {
        width: 1fr;
        border: tall $primary-darken-2;
        padding: 0 1;
    }

    .panel-title {
        text-style: bold;
        color: $accent;
        margin: 1 0 0 0;
        height: 1;
    }

    SelectionList {
        height: 1fr;
        border: none;
        background: transparent;
    }

    #log {
        height: 9;
        border: tall $accent-darken-2;
        padding: 0 1;
        margin-top: 0;
    }
    """

    BINDINGS = [
        Binding("f", "fetch", "Fetch"),
        Binding("w", "write", "Write selected"),
        Binding("p", "promote", "Promote alt"),
        Binding("a", "select_all_pubs", "All pubs"),
        Binding("n", "deselect_all_pubs", "No pubs"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, force: bool = False, no_save_state: bool = False) -> None:
        super().__init__()
        self._force = force
        self._no_save_state = no_save_state
        self._state = load_state()
        self._people = get_people_orcids()
        self._existing_dois, self._existing_title_keys, self._existing_titles = (
            get_existing_publications()
        )
        self._new_groups: list[tuple[dict, list[dict]]] = []
        self._list_items: list[_PubItem] = []
        self._fetching = False

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="panels"):
            with Vertical(id="left"):
                yield Label("AUTHORS", classes="panel-title")
                yield SelectionList(
                    *[
                        Selection(name, orcid, True)
                        for orcid, name in self._people.items()
                    ],
                    id="author-list",
                )
            with Vertical(id="right"):
                yield Label("NEW PUBLICATIONS", id="pub-label", classes="panel-title")
                yield SelectionList(id="pub-list")
        yield RichLog(id="log", highlight=True, markup=True, max_lines=500)
        yield Footer()

    def on_mount(self) -> None:
        log = self.query_one("#log", RichLog)
        last_run = self._state.get("last_run")
        log.write(
            f"[bold]{len(self._people)}[/bold] author(s) loaded.  "
            "Press [bold cyan]F[/bold cyan] to fetch."
        )
        if last_run and not self._force:
            log.write(f"Last run: [dim]{last_run}[/dim] — incremental fetch.")
        else:
            log.write("No prior run — will fetch all publications.")

    def on_selection_list_option_highlighted(
        self, event: SelectionList.OptionHighlighted
    ) -> None:
        if event.selection_list.id != "pub-list" or not self._list_items:
            return
        idx = event.option_index
        if idx >= len(self._list_items):
            return
        item = self._list_items[idx]
        if not item.is_alt:
            return
        main, alts = self._new_groups[item.group_idx]
        alt = alts[item.alt_idx]
        self.query_one("#log", RichLog).write(_compare_line(main, alt))

    @work(thread=True)
    def _do_fetch(self, selected_orcids: list[str]) -> None:
        def log(msg: str) -> None:
            self.call_from_thread(self.query_one("#log", RichLog).write, msg)

        known_orcids: list[str] = self._state.get("known_orcids", [])
        last_run: str | None = None if self._force else self._state.get("last_run")
        seen: dict[str, tuple[str | None, dict, list[dict]]] = {}

        log("[bold yellow]⟳ Fetching…[/bold yellow]")

        for orcid in selected_orcids:
            name = self._people.get(orcid, orcid)
            from_date = None if (orcid not in known_orcids or self._force) else last_run
            scope = "all" if from_date is None else f"since {from_date}"
            log(f"  [cyan]{name}[/cyan] [dim]({orcid})[/dim] — {scope}")

            author_id = fetch_author_id(orcid)
            if not author_id:
                log("    [red]✗ no OpenAlex record[/red]")
                continue

            works = fetch_works(author_id, from_date)
            log(f"    [green]✓[/green] {len(works)} work(s)")

            for w in works:
                doi = _normalise_doi(w.get("doi") or "") or None
                _add_work(seen, w, doi)

        new_groups = filter_new_works(
            seen, self._existing_dois, self._existing_title_keys, self._existing_titles
        )
        self._new_groups = new_groups

        self.call_from_thread(self._populate_pub_list, new_groups)
        n_with_alts = sum(1 for _, alts in new_groups if alts)
        if new_groups:
            alt_note = (
                f"  [dim]({n_with_alts} with alternatives — press P to promote)[/dim]"
                if n_with_alts
                else ""
            )
            log(
                f"[bold green]{len(new_groups)} new publication(s) found.[/bold green]"
                f"{alt_note}  Press [bold cyan]W[/bold cyan] to write."
            )
        else:
            log("[dim]No new publications found.[/dim]")
        self._fetching = False

    def _populate_pub_list(
        self,
        new_groups: list[tuple[dict, list[dict]]],
        deselected_groups: set[int] | None = None,
    ) -> None:
        pub_list = self.query_one("#pub-list", SelectionList)
        pub_label = self.query_one("#pub-label", Label)
        pub_list.clear_options()
        deselected_groups = deselected_groups or set()

        n_alts_total = sum(len(alts) for _, alts in new_groups)
        suffix = f"  [dim]({n_alts_total} alt(s) shown)[/dim]" if n_alts_total else ""
        pub_label.update(
            f"NEW PUBLICATIONS  [dim]({len(new_groups)} found)[/dim]{suffix}"
        )

        self._list_items = []
        for g_idx, (main, alts) in enumerate(new_groups):
            alt_badge = (
                f"  [dim]+{len(alts)} alt{'s' if len(alts) > 1 else ''}[/dim]"
                if alts
                else ""
            )
            main_label = _pub_label(main) + alt_badge
            checked = g_idx not in deselected_groups
            pub_list.add_option(Selection(main_label, len(self._list_items), checked))
            self._list_items.append(_PubItem(g_idx, False, 0, main))

            for a_idx, alt in enumerate(alts):
                alt_label = _pub_label(alt, prefix="  ↳ ")
                pub_list.add_option(Selection(alt_label, len(self._list_items), False))
                self._list_items.append(_PubItem(g_idx, True, a_idx, alt))

    def action_fetch(self) -> None:
        if self._fetching:
            return
        selected = list(self.query_one("#author-list", SelectionList).selected)
        if not selected:
            self.query_one("#log", RichLog).write("[red]No authors selected.[/red]")
            return
        self._fetching = True
        self._do_fetch(selected)

    def action_promote(self) -> None:
        pub_list = self.query_one("#pub-list", SelectionList)
        highlighted = pub_list.highlighted
        if highlighted is None or highlighted >= len(self._list_items):
            return
        item = self._list_items[highlighted]
        log = self.query_one("#log", RichLog)
        if not item.is_alt:
            log.write("[yellow]Already the main entry — navigate to a ↳ alt row.[/yellow]")
            return

        # Remember which mains were deselected so we can restore selection after repopulate
        deselected: set[int] = set()
        for val in set(range(len(self._list_items))) - set(pub_list.selected):
            it = self._list_items[val]
            if not it.is_alt:
                deselected.add(it.group_idx)

        g_idx = item.group_idx
        main, alts = self._new_groups[g_idx]
        a_idx = item.alt_idx
        new_main = alts[a_idx]
        new_alts = [main] + alts[:a_idx] + alts[a_idx + 1:]
        self._new_groups[g_idx] = (new_main, new_alts)

        self._populate_pub_list(self._new_groups, deselected)
        log.write(
            f"[green]↑ Promoted:[/green] {(new_main.get('title') or '')[:70]}"
        )

    def action_write(self) -> None:
        pub_list = self.query_one("#pub-list", SelectionList)
        selected_values = list(pub_list.selected)
        if not selected_values:
            self.query_one("#log", RichLog).write(
                "[yellow]Nothing selected to write.[/yellow]"
            )
            return

        log = self.query_one("#log", RichLog)
        written = 0
        for val in selected_values:
            item = self._list_items[val]
            if item.is_alt:
                continue  # only write mains; use P to promote an alt first
            main, _ = self._new_groups[item.group_idx]
            fm = work_to_frontmatter(main)
            if fm:
                path = write_publication(fm)
                log.write(f"  [green]+[/green] {path.name}")
                written += 1
        log.write(f"[bold green]Wrote {written} file(s).[/bold green]")

        if not self._no_save_state and not self._force:
            all_orcids = set(self._people.keys())
            selected_orcids = set(
                self.query_one("#author-list", SelectionList).selected
            )
            if selected_orcids >= all_orcids:
                self._state["last_run"] = datetime.now(timezone.utc).date().isoformat()
                known = set(self._state.get("known_orcids", []))
                self._state["known_orcids"] = list(known | selected_orcids)
                save_state(self._state)
                log.write("[dim]State saved.[/dim]")

    def action_select_all_pubs(self) -> None:
        pub_list = self.query_one("#pub-list", SelectionList)
        # Select only main entries
        for i, item in enumerate(self._list_items):
            if not item.is_alt:
                pub_list.select(i)

    def action_deselect_all_pubs(self) -> None:
        self.query_one("#pub-list", SelectionList).deselect_all()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Interactive TUI for fetching publications."
    )
    parser.add_argument(
        "--force", action="store_true", help="Fetch all regardless of last-run date."
    )
    parser.add_argument(
        "--no-save-state", action="store_true", help="Do not update fetch_state.json."
    )
    args = parser.parse_args()
    PublicationFetcherApp(force=args.force, no_save_state=args.no_save_state).run()


if __name__ == "__main__":
    main()
