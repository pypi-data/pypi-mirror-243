from __future__ import annotations

__all__ = ["human_file_size", "sanitize_path"]

from pathlib import Path
from urllib.parse import unquote, urlparse

from flamme.utils.format import human_byte


def human_file_size(path: Path | str, decimal: int = 2) -> str:
    r"""Gets a human-readable representation of a file size.

    Args:
    ----
        path (``pathlib.Path`` or str): Specifies the file.
        decimal (int, optional): Specifies the number of decimal
            digits. Default: ``2``

    Returns:
    -------
        str: The file size in a human-readable format.

    Example usage:

    .. code-block:: pycon

        >>> from flamme.utils.path import human_file_size
        >>> human_file_size("README.md")
        '...B'
    """
    return human_byte(size=sanitize_path(path).stat().st_size, decimal=decimal)


def sanitize_path(path: Path | str) -> Path:
    r"""Sanitizes a given path.

    Args:
    ----
        path (``pathlib.Path`` or str): Specifies the path to
            sanitize.

    Returns:
    -------
        ``pathlib.Path``: The sanitized path.

    Example usage:

    .. code-block:: pycon

        >>> from pathlib import Path
        >>> from flamme.utils.path import sanitize_path
        >>> sanitize_path("something")
        PosixPath('.../something')
        >>> sanitize_path("")
        PosixPath('...')
        >>> sanitize_path(Path("something"))
        PosixPath('.../something')
        >>> sanitize_path(Path("something/./../"))
        PosixPath('...')
    """
    if isinstance(path, str):
        # Use urlparse to parse file URI: https://stackoverflow.com/a/15048213
        path = Path(unquote(urlparse(path).path))
    return path.expanduser().resolve()
