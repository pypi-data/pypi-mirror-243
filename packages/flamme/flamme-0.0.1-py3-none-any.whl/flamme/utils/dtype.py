from __future__ import annotations

__all__ = ["column_types"]

from pandas import DataFrame


def column_types(df: DataFrame) -> dict[str, set]:
    r"""Computes the value types per column.

    Args:
    ----
        df (``pandas.DataFrame``): Specifies the DataFrame to analyze.

    Returns:
    -------
        dict: A dictionary with the value types for each column.

    Example usage:

    .. code-block:: pycon

        >>> import numpy as np
        >>> import pandas as pd
        >>> from flamme.utils.dtype import column_types
        >>> df = pd.DataFrame(
        ...     {
        ...         "int": np.array([np.nan, 1, 0, 1]),
        ...         "float": np.array([1.2, 4.2, np.nan, 2.2]),
        ...     }
        ... )
        >>> coltypes = column_types(df)
        >>> coltypes
        {'int': {<class 'float'>}, 'float': {<class 'float'>}}
    """
    types = {}
    for col in df:
        types[col] = {type(x) for x in df[col].tolist()}
    return types
