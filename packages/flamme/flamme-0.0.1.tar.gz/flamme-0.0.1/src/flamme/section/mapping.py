from __future__ import annotations

__all__ = ["SectionDict"]

from collections.abc import Sequence

from coola.utils import str_indent

from flamme.section.base import BaseSection
from flamme.section.utils import (
    GO_TO_TOP,
    render_html_toc,
    tags2id,
    tags2title,
    valid_h_tag,
)


class SectionDict(BaseSection):
    r"""Implements a section to manage a dictionary of sections.

    Args:
    ----
        sections (dict): Specifies the dictionary of sections.
    """

    def __init__(self, sections: dict[str, BaseSection]) -> None:
        self._sections = sections

    def get_statistics(self) -> dict:
        return {name: section.get_statistics() for name, section in self._sections.items()}

    def render_html_body(self, number: str = "", tags: Sequence[str] = (), depth: int = 0) -> str:
        report = []
        if tags:
            report.append(
                f'<h{valid_h_tag(depth+1)} id="{tags2id(tags)}">{number} '
                f"{tags2title(tags)} </h{valid_h_tag(depth+1)}>"
            )
            report.append(GO_TO_TOP)
            report.append('<p style="margin-top: 1rem;">')
        for i, (name, section) in enumerate(self._sections.items()):
            report.append(
                section.render_html_body(
                    number=f"{number}{i + 1}.", tags=list(tags) + [name], depth=depth + 1
                )
            )
        return "\n".join(report)

    def render_html_toc(
        self, number: str = "", tags: Sequence[str] = (), depth: int = 0, max_depth: int = 1
    ) -> str:
        toc = []
        if tags:
            toc.append(render_html_toc(number=number, tags=tags, depth=depth, max_depth=max_depth))
        subtoc = []
        for i, (name, section) in enumerate(self._sections.items()):
            line = section.render_html_toc(
                number=f"{section}{i+1}.",
                tags=list(tags) + [name],
                depth=depth + 1,
                max_depth=max_depth,
            )
            if line:
                subtoc.append(f"  {str_indent(line)}")
        if subtoc:
            toc.extend(["<ul>", "\n".join(subtoc), "</ul>"])
        return "\n".join(toc)
