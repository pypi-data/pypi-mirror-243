from __future__ import annotations

__all__ = [
    "BaseIngestor",
    "CsvIngestor",
    "Ingestor",
    "ParquetIngestor",
    "PreprocessorIngestor",
    "is_ingestor_config",
    "setup_ingestor",
]

from flamme.ingestor.base import BaseIngestor, is_ingestor_config, setup_ingestor
from flamme.ingestor.csv import CsvIngestor
from flamme.ingestor.parquet import ParquetIngestor
from flamme.ingestor.preprocessor import PreprocessorIngestor
from flamme.ingestor.vanilla import Ingestor
