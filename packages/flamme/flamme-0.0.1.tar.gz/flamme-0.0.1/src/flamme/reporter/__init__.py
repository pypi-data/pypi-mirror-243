from __future__ import annotations

__all__ = ["BaseReporter", "Reporter", "is_reporter_config", "setup_reporter"]

from flamme.reporter.base import BaseReporter, is_reporter_config, setup_reporter
from flamme.reporter.vanilla import Reporter
