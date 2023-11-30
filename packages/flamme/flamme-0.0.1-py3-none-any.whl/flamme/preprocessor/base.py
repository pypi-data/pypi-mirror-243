from __future__ import annotations

__all__ = ["BasePreprocessor", "is_preprocessor_config", "setup_preprocessor"]

import logging
from abc import ABC

from objectory import AbstractFactory
from objectory.utils import is_object_config
from pandas import DataFrame

logger = logging.getLogger(__name__)


class BasePreprocessor(ABC, metaclass=AbstractFactory):
    r"""Defines the base class to preprocess a DataFrame.

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

    def preprocess(self, df: DataFrame) -> DataFrame:
        r"""Preprocesses the data in the DataFrame.

        Args:
        ----
            df (``pandas.DataFrame``): Specifies the DataFrame
                to preprocess.

        Returns:
        -------
            ``pandas.DataFrame``: The preprocessed DataFrame.

        Example usage:

        .. code-block:: pycon

            >>> import pandas as pd
            >>> from flamme.preprocessor import ToNumericPreprocessor
            >>> preprocessor = ToNumericPreprocessor(columns=["col1", "col3"])
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


def is_preprocessor_config(config: dict) -> bool:
    r"""Indicates if the input configuration is a configuration for a
    ``BasePreprocessor``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
    ----
        config (dict): Specifies the configuration to check.

    Returns:
    -------
        bool: ``True`` if the input configuration is a configuration
            for a ``BasePreprocessor`` object.

    Example usage:

    .. code-block:: pycon

        >>> from flamme.preprocessor import is_preprocessor_config
        >>> is_preprocessor_config(
        ...     {
        ...         "_target_": "flamme.preprocessor.ToNumericPreprocessor",
        ...         "columns": ["col1", "col3"],
        ...     }
        ... )
        True
    """
    return is_object_config(config, BasePreprocessor)


def setup_preprocessor(
    preprocessor: BasePreprocessor | dict,
) -> BasePreprocessor:
    r"""Sets up an preprocessor.

    The preprocessor is instantiated from its configuration
    by using the ``BasePreprocessor`` factory function.

    Args:
    ----
        preprocessor (``BasePreprocessor`` or dict): Specifies an
            preprocessor or its configuration.

    Returns:
    -------
        ``BasePreprocessor``: An instantiated preprocessor.

    Example usage:

    .. code-block:: pycon

        >>> from flamme.preprocessor import setup_preprocessor
        >>> preprocessor = setup_preprocessor(
        ...     {
        ...         "_target_": "flamme.preprocessor.ToNumericPreprocessor",
        ...         "columns": ["col1", "col3"],
        ...     }
        ... )
        >>> preprocessor
        ToNumericPreprocessor(columns=('col1', 'col3'))
    """
    if isinstance(preprocessor, dict):
        logger.info("Initializing an preprocessor from its configuration... ")
        preprocessor = BasePreprocessor.factory(**preprocessor)
    if not isinstance(preprocessor, BasePreprocessor):
        logger.warning(f"preprocessor is not a `BasePreprocessor` (received: {type(preprocessor)})")
    return preprocessor
