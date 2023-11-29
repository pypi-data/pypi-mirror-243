from __future__ import annotations

__all__ = ["DiscreteDistributionAnalyzer", "TemporalDiscreteDistributionAnalyzer"]

import logging
from collections import Counter

from pandas import DataFrame

from flamme.analyzer.base import BaseAnalyzer
from flamme.section import (
    DiscreteDistributionSection,
    EmptySection,
    TemporalDiscreteDistributionSection,
)

logger = logging.getLogger(__name__)


class DiscreteDistributionAnalyzer(BaseAnalyzer):
    r"""Implements a discrete distribution analyzer.

    Args:
    ----
        column (str): Specifies the column to analyze.
        dropna (bool, optional): If ``True``, the NaN values are not
            included in the analysis. Default: ``False``
        max_rows (int, optional): Specifies the maximum number of rows
            to show in the table. Default: ``20``
    """

    def __init__(self, column: str, dropna: bool = False, max_rows: int = 20) -> None:
        self._column = column
        self._dropna = bool(dropna)
        self._max_rows = max_rows

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(column={self._column}, "
            f"dropna={self._dropna}, max_rows={self._max_rows})"
        )

    def analyze(self, df: DataFrame) -> DiscreteDistributionSection | EmptySection:
        if self._column not in df:
            logger.info(
                f"Skipping discrete distribution analysis of column {self._column} "
                f"because it is not in the DataFrame: {sorted(df.columns)}"
            )
            return EmptySection()
        return DiscreteDistributionSection(
            counter=Counter(df[self._column].value_counts(dropna=self._dropna).to_dict()),
            null_values=df[self._column].isnull().sum(),
            column=self._column,
            max_rows=self._max_rows,
        )


class TemporalDiscreteDistributionAnalyzer(BaseAnalyzer):
    r"""Implements an analyzer to show the temporal distribution of
    discrete values.

    Args:
    ----
        column (str): Specifies the column to analyze.
        dt_column (str): Specifies the datetime column used to analyze
            the temporal distribution.
        period (str): Specifies the temporal period e.g. monthly or
            daily.

    Example usage:

    .. code-block:: pycon

        >>> import numpy as np
        >>> import pandas as pd
        >>> from flamme.analyzer import TemporalNullValueAnalyzer
        >>> analyzer = TemporalDiscreteDistributionAnalyzer(
        ...     column="float", dt_column="datetime", period="M"
        ... )
        >>> analyzer
        TemporalDiscreteDistributionAnalyzer(column=float, dt_column=datetime, period=M)
        >>> df = pd.DataFrame(
        ...     {
        ...         "int": np.array([np.nan, 1, 0, 1]),
        ...         "float": np.array([1.2, 4.2, np.nan, 2.2]),
        ...         "str": np.array(["A", "B", None, np.nan]),
        ...         "datetime": pd.to_datetime(
        ...             ["2020-01-03", "2020-02-03", "2020-03-03", "2020-04-03"]
        ...         ),
        ...     }
        ... )
        >>> section = analyzer.analyze(df)
    """

    def __init__(self, column: str, dt_column: str, period: str) -> None:
        self._column = column
        self._dt_column = dt_column
        self._period = period

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(column={self._column}, "
            f"dt_column={self._dt_column}, period={self._period})"
        )

    def analyze(self, df: DataFrame) -> TemporalDiscreteDistributionSection | EmptySection:
        if self._column not in df:
            logger.info(
                "Skipping temporal discrete distribution analysis because the column "
                f"({self._column}) is not in the DataFrame: {sorted(df.columns)}"
            )
            return EmptySection()
        if self._dt_column not in df:
            logger.info(
                "Skipping temporal discrete distribution analysis because the datetime column "
                f"({self._dt_column}) is not in the DataFrame: {sorted(df.columns)}"
            )
            return EmptySection()
        return TemporalDiscreteDistributionSection(
            column=self._column,
            df=df,
            dt_column=self._dt_column,
            period=self._period,
        )
