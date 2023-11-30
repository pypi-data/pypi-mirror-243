from __future__ import annotations

__all__ = ["valid_h_tag", "tags2id", "tags2title", "render_html_toc"]

from collections.abc import Sequence

GO_TO_TOP = '<a href="#">Go to top</a>'


def tags2id(tags: Sequence[str]) -> str:
    r"""Converts a sequence of tags to a string that can be used as ID in
    a HTML file.

    Args:
    ----
        tags (``Sequence``): Specifies the sequence of tags.

    Returns:
    -------
        str: The generated ID from the tags.
    """
    return "-".join(tags).replace(" ", "-").lower()


def tags2title(tags: Sequence[str]) -> str:
    r"""Converts a sequence of tags to a string that can be used as
    title.

    Args:
    ----
        tags (``Sequence``): Specifies the sequence of tags.

    Returns:
    -------
        str: The generated title from the tags.
    """
    return " | ".join(tags[::-1])


def valid_h_tag(index: int) -> int:
    r"""Computes a valid number of a h HTML tag.

    Args:
    ----
        index (int): Specifies the original value.

    Returns:
    -------
        int: A valid value.
    """
    return max(1, min(6, index))


def render_html_toc(
    number: str = "", tags: Sequence[str] = (), depth: int = 0, max_depth: int = 1
) -> str:
    r"""Renders the HTML table of content (TOC) associated to the
    section.

    Args:
    ----
        number (str, optional): Specifies the section number
            associated to the section. Default: ""
        tags (``Sequence``, optional): Specifies the tags
            associated to the section. Default: ``()``
        depth (int, optional): Specifies the depth in the report.
            Default: ``0``

    Returns:
    -------
        str: The HTML table of content associated to the section.
    """
    if depth >= max_depth:
        return ""
    tag = tags[-1] if tags else ""
    return f'<li><a href="#{tags2id(tags)}">{number} {tag}</a></li>'
