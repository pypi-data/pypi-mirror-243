from __future__ import annotations

__all__ = ["ContinuousDistributionSection"]

from collections.abc import Sequence

import plotly
import plotly.express as px
from jinja2 import Template
from pandas import Series

from flamme.section.base import BaseSection
from flamme.section.utils import (
    GO_TO_TOP,
    render_html_toc,
    tags2id,
    tags2title,
    valid_h_tag,
)
from flamme.utils.range import find_range


class ContinuousDistributionSection(BaseSection):
    r"""Implements a section that analyzes a continuous distribution of
    values.

    Args:
    ----
        series (``pandas.Series``): Specifies the series/column to
            analyze.
        column (str): Specifies the column name.
        nbins (int or None, optional): Specifies the number of bins in
            the histogram. Default: ``None``
        log_y (bool, optional): If ``True``, it represents the bars
            with a log scale. Default: ``False``
        xmin (float or str or None, optional): Specifies the minimum
            value of the range or its associated quantile.
            ``q0.1`` means the 10% quantile. ``0`` is the minimum
            value and ``1`` is the maximum value. Default: ``None``
        xmax (float or str or None, optional): Specifies the maximum
            value of the range or its associated quantile.
            ``q0.9`` means the 90% quantile. ``0`` is the minimum
            value and ``1`` is the maximum value. Default: ``None``
    """

    def __init__(
        self,
        series: Series,
        column: str,
        nbins: int | None = None,
        log_y: bool = False,
        xmin: float | str | None = None,
        xmax: float | str | None = None,
    ) -> None:
        self._series = series
        self._column = column
        self._nbins = nbins
        self._log_y = log_y
        self._xmin = xmin
        self._xmax = xmax

    @property
    def column(self) -> str:
        return self._column

    @property
    def log_y(self) -> bool:
        return self._log_y

    @property
    def nbins(self) -> int | None:
        return self._nbins

    @property
    def series(self) -> Series:
        return self._series

    @property
    def xmin(self) -> float | str | None:
        return self._xmin

    @property
    def xmax(self) -> float | str | None:
        return self._xmax

    def get_statistics(self) -> dict:
        stats = {
            "count": int(self._series.shape[0]),
            "num_nulls": int(self._series.isnull().sum()),
            "nunique": self._series.nunique(dropna=False),
        }
        stats["num_non_nulls"] = stats["count"] - stats["num_nulls"]
        if stats["num_non_nulls"] > 0:
            stats |= (
                self._series.dropna()
                .agg(
                    {
                        "mean": "mean",
                        "median": "median",
                        "min": "min",
                        "max": "max",
                        "std": "std",
                        "q01": lambda x: x.quantile(0.01),
                        "q05": lambda x: x.quantile(0.05),
                        "q10": lambda x: x.quantile(0.1),
                        "q25": lambda x: x.quantile(0.25),
                        "q75": lambda x: x.quantile(0.75),
                        "q90": lambda x: x.quantile(0.9),
                        "q95": lambda x: x.quantile(0.95),
                        "q99": lambda x: x.quantile(0.99),
                    }
                )
                .to_dict()
            )
        else:
            stats |= {
                "mean": float("nan"),
                "median": float("nan"),
                "min": float("nan"),
                "max": float("nan"),
                "std": float("nan"),
                "q01": float("nan"),
                "q05": float("nan"),
                "q10": float("nan"),
                "q25": float("nan"),
                "q75": float("nan"),
                "q90": float("nan"),
                "q95": float("nan"),
                "q99": float("nan"),
            }
        return stats

    def render_html_body(self, number: str = "", tags: Sequence[str] = (), depth: int = 0) -> str:
        stats = self.get_statistics()
        null_values_pct = (
            f"{100 * stats['num_nulls'] / stats['count']:.2f}" if stats["count"] > 0 else "N/A"
        )
        return Template(self._create_template()).render(
            {
                "go_to_top": GO_TO_TOP,
                "id": tags2id(tags),
                "depth": valid_h_tag(depth + 1),
                "title": tags2title(tags),
                "section": number,
                "column": self._column,
                "table": create_stats_table(stats=stats, column=self._column),
                "total_values": f"{stats['count']:,}",
                "unique_values": f"{stats['nunique']:,}",
                "null_values": f"{stats['num_nulls']:,}",
                "null_values_pct": null_values_pct,
                "figure": create_histogram_figure(
                    series=self._series,
                    column=self._column,
                    nbins=self._nbins,
                    log_y=self._log_y,
                    xmin=self._xmin,
                    xmax=self._xmax,
                ),
            }
        )

    def render_html_toc(
        self, number: str = "", tags: Sequence[str] = (), depth: int = 0, max_depth: int = 1
    ) -> str:
        return render_html_toc(number=number, tags=tags, depth=depth, max_depth=max_depth)

    def _create_template(self) -> str:
        return """
<h{{depth}} id="{{id}}">{{section}} {{title}} </h{{depth}}>

{{go_to_top}}

<p style="margin-top: 1rem;">
This section analyzes the discrete distribution of values for column {{column}}.

<ul>
  <li> total values: {{total_values}} </li>
  <li> number of unique values: {{unique_values}} </li>
  <li> number of null values: {{null_values}} / {{total_values}} ({{null_values_pct}}%) </li>
</ul>

{{figure}}
{{table}}
<p style="margin-top: 1rem;">
"""


def create_histogram_figure(
    series: Series,
    column: str,
    nbins: int | None = None,
    log_y: bool = False,
    xmin: float | str | None = None,
    xmax: float | str | None = None,
) -> str:
    r"""Creates the HTML code of a figure.

    Args:
    ----
        row (``pandas.Series``): Specifies the series of data.
        column (str): Specifies the column name.
        nbins (int or None, optional): Specifies the number of bins in
            the histogram. Default: ``None``
        log_y (bool, optional): If ``True``, it represents the bars
            with a log scale. Default: ``False``

    Returns:
    -------
        str: The HTML code of the figure.
    """
    array = series.to_numpy()
    xmin, xmax = find_range(array, xmin=xmin, xmax=xmax)
    fig = px.histogram(
        array,
        marginal="box",
        nbins=nbins,
        title=f"Distribution of values for column {column}",
        labels={"x": "value", "y": "count"},
        log_y=log_y,
        range_x=[xmin, xmax],
    )
    fig.update_layout(showlegend=False)

    return plotly.io.to_html(fig, full_html=False)


def create_stats_table(stats: dict, column: str) -> str:
    r"""Creates the HTML code of the table with statistics.

    Args:
    ----
        stats (dict): Specifies a dictionary with the statistics.
        column (str): Specifies the column name.

    Returns:
    -------
        str: The HTML code of the table.
    """
    return Template(
        """
<details>
    <summary>Statistics</summary>

    <p>The following table shows some statistics about the distribution for column {{column}}.

    <table class="table table-hover table-responsive w-auto" >
        <thead class="thead table-group-divider">
            <tr><th>stat</th><th>value</th></tr>
        </thead>
        <tbody class="tbody table-group-divider">
            <tr><th>count</th><td {{num_style}}>{{count}}</td></tr>
            <tr><th>mean</th><td {{num_style}}>{{mean}}</td></tr>
            <tr><th>std</th><td {{num_style}}>{{std}}</td></tr>
            <tr><th>min</th><td {{num_style}}>{{min}}</td></tr>
            <tr><th>quantile 1%</th><td {{num_style}}>{{q01}}</td></tr>
            <tr><th>quantile 5%</th><td {{num_style}}>{{q05}}</td></tr>
            <tr><th>quantile 10%</th><td {{num_style}}>{{q10}}</td></tr>
            <tr><th>quantile 25%</th><td {{num_style}}>{{q25}}</td></tr>
            <tr><th>median</th><td {{num_style}}>{{median}}</td></tr>
            <tr><th>quantile 75%</th><td {{num_style}}>{{q75}}</td></tr>
            <tr><th>quantile 90%</th><td {{num_style}}>{{q90}}</td></tr>
            <tr><th>quantile 95%</th><td {{num_style}}>{{q95}}</td></tr>
            <tr><th>quantile 99%</th><td {{num_style}}>{{q99}}</td></tr>
            <tr><th>max</th><td {{num_style}}>{{max}}</td></tr>
            <tr class="table-group-divider"></tr>
        </tbody>
    </table>
</details>
"""
    ).render(
        {
            "column": column,
            "num_style": 'style="text-align: right;"',
            "count": f"{stats['count']:,}",
            "mean": f"{stats['mean']:,.4f}",
            "median": f"{stats['median']:,.4f}",
            "min": f"{stats['min']:,.4f}",
            "max": f"{stats['max']:,.4f}",
            "std": f"{stats['std']:,.4f}",
            "q01": f"{stats['q01']:,.4f}",
            "q05": f"{stats['q05']:,.4f}",
            "q10": f"{stats['q10']:,.4f}",
            "q25": f"{stats['q25']:,.4f}",
            "q75": f"{stats['q75']:,.4f}",
            "q90": f"{stats['q90']:,.4f}",
            "q95": f"{stats['q95']:,.4f}",
            "q99": f"{stats['q99']:,.4f}",
        }
    )
