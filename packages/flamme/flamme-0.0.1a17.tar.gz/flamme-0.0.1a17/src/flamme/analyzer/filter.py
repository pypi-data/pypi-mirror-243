from __future__ import annotations

__all__ = ["FilteredAnalyzer"]

from coola.utils import str_indent, str_mapping
from pandas import DataFrame

from flamme.analyzer.base import BaseAnalyzer
from flamme.section import BaseSection
from flamme.utils import setup_object


class FilteredAnalyzer(BaseAnalyzer):
    r"""Implements an analyzer to find all the value types in each
    column.

    Example usage:

    .. code-block:: pycon

        >>> import numpy as np
        >>> import pandas as pd
        >>> from flamme.analyzer import FilteredAnalyzer, NullValueAnalyzer
        >>> analyzer = FilteredAnalyzer(query="float >= 2.0", analyzer=NullValueAnalyzer())
        >>> analyzer
        FilteredAnalyzer(
          (query): float >= 2.0
          (analyzer): NullValueAnalyzer()
        )
        >>> df = pd.DataFrame(
        ...     {
        ...         "int": np.array([np.nan, 1, 0, 1]),
        ...         "float": np.array([1.2, 4.2, np.nan, 2.2]),
        ...         "str": np.array(["A", "B", None, np.nan]),
        ...     }
        ... )
        >>> section = analyzer.analyze(df)
    """

    def __init__(self, query: str, analyzer: BaseAnalyzer | dict) -> None:
        self._query = query
        self._analyzer = setup_object(analyzer)

    def __repr__(self) -> str:
        args = str_indent(str_mapping({"query": self._query, "analyzer": self._analyzer}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def analyze(self, df: DataFrame) -> BaseSection:
        df = df.query(self._query)
        return self._analyzer.analyze(df)
