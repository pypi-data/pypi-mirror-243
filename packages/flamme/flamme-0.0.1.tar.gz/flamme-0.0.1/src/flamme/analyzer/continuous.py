from __future__ import annotations

__all__ = ["ContinuousDistributionAnalyzer", "TemporalContinuousDistributionAnalyzer"]

import logging

from pandas import DataFrame

from flamme.analyzer.base import BaseAnalyzer
from flamme.section import (
    ContinuousDistributionSection,
    EmptySection,
    TemporalContinuousDistributionSection,
)

logger = logging.getLogger(__name__)


class ContinuousDistributionAnalyzer(BaseAnalyzer):
    r"""Implements an analyzer to show the temporal distribution of
    continuous values.

    Args:
    ----
        column (str): Specifies the column to analyze.
        nbins (int or None, optional): Specifies the number of bins in
            the histogram. Default: ``None``
        log_y (bool, optional): If ``True``, it represents the bars
            with a log scale. Default: ``False``
        xmin (float or str or None, optional): Specifies the minimum
            value of the range or its associated quantile.
            ``q0.1`` means the 10% quantile. ``0`` is the minimum
            value and ``1`` is the maximum value. Default: ``q0``
        xmax (float or str or None, optional): Specifies the maximum
            value of the range or its associated quantile.
            ``q0.9`` means the 90% quantile. ``0`` is the minimum
            value and ``1`` is the maximum value. Default: ``q1``

    Example usage:

    .. code-block:: pycon

        >>> import numpy as np
        >>> import pandas as pd
        >>> from flamme.analyzer import ContinuousDistributionAnalyzer
        >>> analyzer = ContinuousDistributionAnalyzer(column="float")
        >>> analyzer
        ContinuousDistributionAnalyzer(column=float, nbins=None, log_y=False, xmin=q0, xmax=q1)
        >>> df = pd.DataFrame(
        ...     {
        ...         "int": np.array([np.nan, 1, 0, 1]),
        ...         "float": np.array([1.2, 4.2, np.nan, 2.2]),
        ...         "str": np.array(["A", "B", None, np.nan]),
        ...     }
        ... )
        >>> section = analyzer.analyze(df)
    """

    def __init__(
        self,
        column: str,
        nbins: int | None = None,
        log_y: bool = False,
        xmin: float | str | None = "q0",
        xmax: float | str | None = "q1",
    ) -> None:
        self._column = column
        self._nbins = nbins
        self._log_y = log_y
        self._xmin = xmin
        self._xmax = xmax

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(column={self._column}, nbins={self._nbins}, "
            f"log_y={self._log_y}, xmin={self._xmin}, xmax={self._xmax})"
        )

    def analyze(self, df: DataFrame) -> ContinuousDistributionSection | EmptySection:
        if self._column not in df:
            logger.info(
                "Skipping temporal continuous distribution analysis because the column "
                f"({self._column}) is not in the DataFrame: {sorted(df.columns)}"
            )
            return EmptySection()
        return ContinuousDistributionSection(
            column=self._column,
            series=df[self._column],
            nbins=self._nbins,
            log_y=self._log_y,
            xmin=self._xmin,
            xmax=self._xmax,
        )


class TemporalContinuousDistributionAnalyzer(BaseAnalyzer):
    r"""Implements an analyzer to show the temporal distribution of
    continuous values.

    Args:
    ----
        column (str): Specifies the column to analyze.
        dt_column (str): Specifies the datetime column used to analyze
            the temporal distribution.
        period (str): Specifies the temporal period e.g. monthly or
            daily.
        log_y (bool, optional): If ``True``, it represents the bars
            with a log scale. Default: ``False``

    Example usage:

    .. code-block:: pycon

        >>> import numpy as np
        >>> import pandas as pd
        >>> from flamme.analyzer import TemporalNullValueAnalyzer
        >>> analyzer = TemporalContinuousDistributionAnalyzer(
        ...     column="float", dt_column="datetime", period="M"
        ... )
        >>> analyzer
        TemporalContinuousDistributionAnalyzer(column=float, dt_column=datetime, period=M, log_y=False)
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

    def __init__(self, column: str, dt_column: str, period: str, log_y: bool = False) -> None:
        self._column = column
        self._dt_column = dt_column
        self._period = period
        self._log_y = log_y

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(column={self._column}, "
            f"dt_column={self._dt_column}, period={self._period}, log_y={self._log_y})"
        )

    def analyze(self, df: DataFrame) -> TemporalContinuousDistributionSection | EmptySection:
        if self._column not in df:
            logger.info(
                "Skipping temporal continuous distribution analysis because the column "
                f"({self._column}) is not in the DataFrame: {sorted(df.columns)}"
            )
            return EmptySection()
        if self._dt_column not in df:
            logger.info(
                "Skipping temporal continuous distribution analysis because the datetime column "
                f"({self._dt_column}) is not in the DataFrame: {sorted(df.columns)}"
            )
            return EmptySection()
        return TemporalContinuousDistributionSection(
            column=self._column,
            df=df,
            dt_column=self._dt_column,
            period=self._period,
            log_y=self._log_y,
        )
