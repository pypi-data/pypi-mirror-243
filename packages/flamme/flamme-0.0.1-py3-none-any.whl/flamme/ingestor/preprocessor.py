from __future__ import annotations

__all__ = ["PreprocessorIngestor"]

import logging

from coola.utils import str_indent, str_mapping
from pandas import DataFrame

from flamme.ingestor.base import BaseIngestor, setup_ingestor
from flamme.preprocessor.base import BasePreprocessor, setup_preprocessor

logger = logging.getLogger(__name__)


class PreprocessorIngestor(BaseIngestor):
    r"""Implements an ingestor that also preprocess the DataFrame.

    Args:
    ----
        path (``pathlib.Path`` or str): Specifies the path to the
            CSV file to ingest.
        **kwargs: Additional keyword arguments for
            ``pandas.read_csv``.

    Example usage:

    .. code-block:: pycon

        >>> from flamme.ingestor import PreprocessorIngestor, ParquetIngestor
        >>> from flamme.preprocessor import ToNumericPreprocessor
        >>> ingestor = PreprocessorIngestor(
        ...     ingestor=ParquetIngestor(path="/path/to/df.csv"),
        ...     preprocessor=ToNumericPreprocessor(columns=["col1", "col3"]),
        ... )
        >>> ingestor
        PreprocessorIngestor(
          (ingestor): ParquetIngestor(path=/path/to/df.csv)
          (preprocessor): ToNumericPreprocessor(columns=('col1', 'col3'))
        )
        >>> df = ingestor.ingest()  # doctest: +SKIP
    """

    def __init__(
        self, ingestor: BaseIngestor | dict, preprocessor: BasePreprocessor | dict
    ) -> None:
        self._ingestor = setup_ingestor(ingestor)
        self._preprocessor = setup_preprocessor(preprocessor)

    def __repr__(self) -> str:
        args = str_indent(
            str_mapping({"ingestor": self._ingestor, "preprocessor": self._preprocessor})
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def ingest(self) -> DataFrame:
        df = self._ingestor.ingest()
        return self._preprocessor.preprocess(df)
