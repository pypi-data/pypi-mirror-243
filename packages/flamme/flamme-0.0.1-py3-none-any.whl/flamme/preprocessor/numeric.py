from __future__ import annotations

__all__ = ["ToNumericPreprocessor"]

from collections.abc import Sequence

import pandas as pd
from pandas import DataFrame
from tqdm import tqdm

from flamme.preprocessor.base import BasePreprocessor


class ToNumericPreprocessor(BasePreprocessor):
    r"""Implements a preprocessor to convert some columns to numeric
    type.

    Args:
    ----
        columns (``Sequence``): Specifies the columns to convert.
        **kwargs: Specifies the keyword arguments for
            ``pandas.to_numeric``.

    Example usage:

    .. code-block:: pycon

        >>> import pandas as pd
        >>> from flamme.preprocessor import ToNumericPreprocessor
        >>> preprocessor = ToNumericPreprocessor(columns=["col1", "col3"])
        >>> preprocessor
        ToNumericPreprocessor(columns=('col1', 'col3'))
        >>> df = pd.DataFrame(
        ...     {
        ...         "col1": [1, 2, 3, 4, 5],
        ...         "col2": ["1", "2", "3", "4", "5"],
        ...         "col3": ["1", "2", "3", "4", "5"],
        ...         "col4": ["a", "b", "c", "d", "e"],
        ...     }
        ... )
        >>> df.dtypes
        col1     int64
        col2    object
        col3    object
        col4    object
        dtype: object
        >>> df = preprocessor.preprocess(df)
        >>> df.dtypes
        col1     int64
        col2    object
        col3     int64
        col4    object
        dtype: object
    """

    def __init__(self, columns: Sequence[str], **kwargs) -> None:
        self._columns = tuple(columns)
        self._kwargs = kwargs

    def __repr__(self) -> str:
        args = ", ".join([f"{key}={value}" for key, value in self._kwargs.items()])
        if args:
            args = ", " + args
        return f"{self.__class__.__qualname__}(columns={self._columns}{args})"

    def preprocess(self, df: DataFrame) -> DataFrame:
        for col in tqdm(self._columns, desc="Converting to numeric type"):
            df[col] = pd.to_numeric(df[col], **self._kwargs)
        return df
