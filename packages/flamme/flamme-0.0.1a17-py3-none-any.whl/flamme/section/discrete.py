from __future__ import annotations

__all__ = ["DiscreteDistributionSection"]

from collections import Counter
from collections.abc import Sequence

import plotly
import plotly.express as px
from jinja2 import Template
from pandas import DataFrame

from flamme.section.base import BaseSection
from flamme.section.utils import (
    GO_TO_TOP,
    render_html_toc,
    tags2id,
    tags2title,
    valid_h_tag,
)


class DiscreteDistributionSection(BaseSection):
    r"""Implements a section that analyzes a discrete distribution of
    values.

    Args:
    ----
        counter (``Counter``): Specifies the counter that represents
            the discrete distribution.
        null_values (int): Specifies the number of null values.
        column (str, optional): Specifies the column name.
            Default: ``'N/A'``
        max_rows (int, optional): Specifies the maximum number of rows
            to show in the table. Default: ``20``
    """

    def __init__(
        self, counter: Counter, null_values: int = 0, column: str = "N/A", max_rows: int = 20
    ) -> None:
        self._counter = counter
        self._null_values = null_values
        self._column = column
        self._max_rows = int(max_rows)

        self._total = sum(self._counter.values())

    def get_statistics(self) -> dict:
        most_common = [(value, count) for value, count in self._counter.most_common() if count > 0]
        return {
            "most_common": most_common,
            "nunique": len(most_common),
            "total": self._total,
        }

    def render_html_body(self, number: str = "", tags: Sequence[str] = (), depth: int = 0) -> str:
        stats = self.get_statistics()
        null_values_pct = (
            f"{100 * self._null_values / stats['total']:.2f}" if stats["total"] > 0 else "N/A"
        )
        return Template(self._create_template()).render(
            {
                "go_to_top": GO_TO_TOP,
                "id": tags2id(tags),
                "depth": valid_h_tag(depth + 1),
                "title": tags2title(tags),
                "section": number,
                "column": self._column,
                "total_values": f"{stats['total']:,}",
                "unique_values": f"{stats['nunique']:,}",
                "null_values": f"{self._null_values:,}",
                "null_values_pct": null_values_pct,
                "figure": self._create_figure(),
                "table": self._create_table(),
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

    def _create_figure(self) -> str:
        if self._total == 0:
            return ""
        most_common = [(value, count) for value, count in self._counter.most_common() if count > 0]
        df = DataFrame(
            {
                "value": [str(value) for value, _ in most_common],
                "count": [count for _, count in most_common],
            }
        )
        fig = px.bar(
            df,
            x="value",
            y="count",
            title="Number of occurrences per value",
            labels={"value": "value", "count": "number of occurrences"},
            text_auto=True,
            template="seaborn",
            log_y=(most_common[0][1] / most_common[-1][1]) >= 20,
        )
        return Template(
            r"""
<p style="margin-top: 1rem;">
<b>Distribution of values in column {{column}}</b>

<p>The values in the figure below are sorted by decreasing order of number of occurrences.

{{figure}}
"""
        ).render({"figure": plotly.io.to_html(fig, full_html=False), "column": self._column})

    def _create_table(self) -> str:
        if self._total == 0:
            return ""

        most_common = self._counter.most_common(self._max_rows)
        rows_head = "\n".join(
            [create_table_row(column=col, count=count) for col, count in most_common]
        )
        lest_common = self._counter.most_common()[-self._max_rows :][::-1]
        rows_tail = "\n".join(
            [create_table_row(column=col, count=count) for col, count in lest_common]
        )
        return Template(
            """
<details>
    <summary>Show head and tail values</summary>

    <div class="row">
      <div class="col">
        <p style="margin-top: 1rem;">
        <b>Head: {{max_values}} most common values in column {{column}}</b>
        <table class="table table-hover table-responsive w-auto" >
            <thead class="thead table-group-divider">
                <tr>
                    <th>column</th>
                    <th>count</th>
                </tr>
            </thead>
            <tbody class="tbody table-group-divider">
                {{rows_head}}
                <tr class="table-group-divider"></tr>
            </tbody>
        </table>
      </div>
      <div class="col">
        <p style="margin-top: 1rem;">
        <b>Tail: {{max_values}} least common values in column {{column}}</b>
        <table class="table table-hover table-responsive w-auto" >
            <thead class="thead table-group-divider">
                <tr>
                    <th>column</th>
                    <th>count</th>
                </tr>
            </thead>
            <tbody class="tbody table-group-divider">
                {{rows_tail}}
                <tr class="table-group-divider"></tr>
            </tbody>
        </table>
      </div>
    </div>
</details>
"""
        ).render(
            {
                "max_values": len(most_common),
                "rows_head": rows_head,
                "rows_tail": rows_tail,
                "column": self._column,
            }
        )


def create_table_row(column: str, count: int) -> str:
    r"""Creates the HTML code of a new table row.

    Args:
    ----
        column (str): Specifies the column name.
        count (int): Specifies the count for the column.

    Returns:
    -------
        str: The HTML code of a row.
    """
    return Template("""<tr><th>{{column}}</th><td {{num_style}}>{{count}}</td></tr>""").render(
        {"num_style": 'style="text-align: right;"', "column": column, "count": f"{count:,}"}
    )
