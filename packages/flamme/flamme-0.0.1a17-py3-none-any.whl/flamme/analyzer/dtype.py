from __future__ import annotations

__all__ = ["ColumnTypeAnalyzer"]

from pandas import DataFrame

from flamme.analyzer.base import BaseAnalyzer
from flamme.section import ColumnTypeSection
from flamme.utils.dtype import column_types


class ColumnTypeAnalyzer(BaseAnalyzer):
    r"""Implements an analyzer to find all the value types in each
    column.

    Example usage:

    .. code-block:: pycon

        >>> import numpy as np
        >>> import pandas as pd
        >>> from flamme.analyzer import ColumnTypeAnalyzer
        >>> analyzer = ColumnTypeAnalyzer()
        >>> analyzer
        ColumnTypeAnalyzer()
        >>> df = pd.DataFrame(
        ...     {
        ...         "int": np.array([np.nan, 1, 0, 1]),
        ...         "float": np.array([1.2, 4.2, np.nan, 2.2]),
        ...         "str": np.array(["A", "B", None, np.nan]),
        ...     }
        ... )
        >>> section = analyzer.analyze(df)
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def analyze(self, df: DataFrame) -> ColumnTypeSection:
        return ColumnTypeSection(dtypes=df.dtypes.to_dict(), types=column_types(df))
