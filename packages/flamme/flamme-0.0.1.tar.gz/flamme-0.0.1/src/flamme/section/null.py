from __future__ import annotations

__all__ = ["NullValueSection", "TemporalNullValueSection"]

import math
from collections.abc import Sequence

import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
from jinja2 import Template
from pandas import DataFrame
from plotly.subplots import make_subplots

from flamme.section.base import BaseSection
from flamme.section.utils import (
    GO_TO_TOP,
    render_html_toc,
    tags2id,
    tags2title,
    valid_h_tag,
)


class NullValueSection(BaseSection):
    r"""Implements a section that analyzes the number of null values.

    Args:
    ----
        columns (``Sequence``): Specifies the column names.
        null_count (``numpy.ndarray``): Specifies the number of null
            values for each column.
        total_count (``numpy.ndarray``): Specifies the total number
            of values for each column.
    """

    def __init__(
        self, columns: Sequence[str], null_count: np.ndarray, total_count: np.ndarray
    ) -> None:
        self._columns = tuple(columns)
        self._null_count = null_count.flatten().astype(int)
        self._total_count = total_count.flatten().astype(int)

        if len(self._columns) != self._null_count.shape[0]:
            raise RuntimeError(
                f"columns ({len(self._columns):,}) and null_count ({self._null_count.shape[0]:,}) "
                "do not match"
            )
        if len(self._columns) != self._total_count.shape[0]:
            raise RuntimeError(
                f"columns ({len(self._columns):,}) and total_count "
                f"({self._total_count.shape[0]:,}) do not match"
            )

    def get_statistics(self) -> dict:
        return {
            "columns": self._columns,
            "null_count": tuple(self._null_count.tolist()),
            "total_count": tuple(self._total_count.tolist()),
        }

    def render_html_body(self, number: str = "", tags: Sequence[str] = (), depth: int = 0) -> str:
        return Template(self._create_template()).render(
            {
                "go_to_top": GO_TO_TOP,
                "id": tags2id(tags),
                "depth": valid_h_tag(depth + 1),
                "title": tags2title(tags),
                "section": number,
                "table_alpha": self._create_table(sort_by="column"),
                "table_sort": self._create_table(sort_by="null"),
                "bar_figure": self._create_bar_figure(),
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
This section analyzes the number/proportion of null values for each column.
The color indicates the proportion of missing values.
Dark blues indicates more missing values than light blues.

{{bar_figure}}

<div class="container-fluid">
    <div class="row align-items-start">
        <div class="col align-self-center">
            <p><b>Columns sorted by alphabetical order</b></p>

            {{table_alpha}}

        </div>
        <div class="col">
            <p><b>Columns sorted by ascending order of missing values</b></p>

            {{table_sort}}

        </div>
    </div>
</div>
"""

    def _create_bar_figure(self) -> str:
        df = self._get_dataframe().sort_values(by="null")
        fig = px.bar(
            df,
            x="column",
            y="null",
            title="number of null values per column",
            labels={"column": "column", "null": "number of null values"},
            text_auto=True,
            template="seaborn",
        )
        return plotly.io.to_html(fig, full_html=False)

    def _create_table(self, sort_by: str) -> str:
        df = self._get_dataframe().sort_values(by=sort_by)
        rows = "\n".join(
            [
                create_table_row(column=column, null_count=null_count, total_count=total_count)
                for column, null_count, total_count in zip(
                    df["column"].to_numpy(), df["null"].to_numpy(), df["total"].to_numpy()
                )
            ]
        )
        return Template(
            """
<table class="table table-hover table-responsive w-auto" >
    <thead class="thead table-group-divider">
        <tr>
            <th>column</th>
            <th>null pct</th>
            <th>null count</th>
            <th>total count</th>
        </tr>
    </thead>
    <tbody class="tbody table-group-divider">
        {{rows}}
        <tr class="table-group-divider"></tr>
    </tbody>
</table>
"""
        ).render({"rows": rows})

    def _get_dataframe(self) -> DataFrame:
        return DataFrame(
            {"column": self._columns, "null": self._null_count, "total": self._total_count}
        )


def create_table_row(column: str, null_count: int, total_count: int) -> str:
    r"""Creates the HTML code of a new table row.

    Args:
    ----
        column (str): Specifies the column name.
        null_count (int): Specifies the number of null values.
        total_count (int): Specifies the total number of rows.

    Returns:
    -------
        str: The HTML code of a row.
    """
    pct = null_count / total_count
    return Template(
        """<tr>
    <th style="background-color: rgba(0, 191, 255, {{null_pct}})">{{column}}</th>
    <td {{num_style}}>{{null_pct}}</td>
    <td {{num_style}}>{{null_count}}</td>
    <td {{num_style}}>{{total_count}}</td>
</tr>"""
    ).render(
        {
            "num_style": f'style="text-align: right; background-color: rgba(0, 191, 255, {pct})"',
            "column": column,
            "null_count": f"{null_count:,}",
            "null_pct": f"{pct:.4f}",
            "total_count": f"{total_count:,}",
        }
    )


class TemporalNullValueSection(BaseSection):
    r"""Implements a section to analyze the temporal distribution of null
    values.

    Args:
    ----
        df (``pandas.DataFrame``): Specifies the DataFrame to analyze.
        dt_column (str): Specifies the datetime column used to analyze
            the temporal distribution.
        period (str): Specifies the temporal period e.g. monthly or
            daily.
    """

    def __init__(self, df: DataFrame, dt_column: str, period: str) -> None:
        self._df = df
        self._dt_column = dt_column
        self._period = period

    def get_statistics(self) -> dict:
        return {}

    def render_html_body(self, number: str = "", tags: Sequence[str] = (), depth: int = 0) -> str:
        return Template(self._create_template()).render(
            {
                "go_to_top": GO_TO_TOP,
                "id": tags2id(tags),
                "depth": valid_h_tag(depth + 1),
                "title": tags2title(tags),
                "section": number,
                "column": self._dt_column,
                "figure": create_temporal_null_figure(
                    df=self._df, dt_column=self._dt_column, period=self._period
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
This section analyzes the monthly distribution of null values.
The column {{column}} is used to define the month of each row.

{{figure}}
"""


def create_temporal_null_figure(
    df: DataFrame,
    dt_column: str,
    period: str,
    ncols: int = 2,
    figsize: tuple[int, int] = (700, 300),
) -> str:
    r"""Creates a HTML representation of a figure with the temporal null
    value distribution.

    Args:
    ----
        df (``DataFrame``): Specifies the DataFrame to analyze.
        dt_column (str): Specifies the datetime column used to analyze
            the temporal distribution.
        period (str): Specifies the temporal period e.g. monthly or
            daily.
        ncols (int, optional): Specifies the number of columns.
            Default: ``2``
        figsize (``tuple``, optional): Specifies the individual figure
            size in pixels. The first dimension is the width and the
            second is the height.  Default: ``(700, 300)``

    Returns:
    -------
        str: The HTML representation of the figure.
    """
    if df.shape[0] == 0:
        return ""
    df = df.copy()
    columns = sorted([col for col in df.columns if col != dt_column])
    dt_col = "__datetime__"
    df[dt_col] = df[dt_column].dt.to_period(period)

    nrows = math.ceil(len(columns) / ncols)
    fig = make_subplots(
        rows=nrows,
        cols=ncols,
        subplot_titles=columns,
        specs=[[{"secondary_y": True} for _ in range(ncols)] for _ in range(nrows)],
    )

    for i, column in enumerate(columns):
        x, y = i // ncols, i % ncols
        null_col = f"__{column}_isnull__"
        df2 = df[[column, dt_col]].copy()
        df2.loc[:, null_col] = df2.loc[:, column].isnull()

        df_sum = df2.groupby(dt_col)[null_col].sum().sort_index()
        df_count = df2.groupby(dt_col)[null_col].count().sort_index()
        labels = [str(dt) for dt in df_sum.index]

        fig.add_trace(
            go.Bar(
                x=labels,
                y=df_count.to_numpy(),
                marker=dict(color="rgba(0, 191, 255, 0.9)"),
            ),
            row=x + 1,
            col=y + 1,
            secondary_y=False,
        )
        fig.add_trace(
            go.Bar(
                x=labels,
                y=df_sum.to_numpy(),
                marker=dict(color="rgba(255, 191, 0, 0.9)"),
            ),
            row=x + 1,
            col=y + 1,
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=labels,
                y=df_sum.to_numpy() / df_count.to_numpy(),
                marker=dict(color="rgba(0, 71, 171, 0.9)"),
            ),
            row=x + 1,
            col=y + 1,
            secondary_y=True,
        )

    fig.update_yaxes(
        title_text=(
            '<span style="color:RGB(255, 191, 0)">null</span>/'
            '<span style="color:RGB(0, 191, 255)">total</span>'
        ),
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text='<span style="color:RGB(0, 71, 171)">percentage</span>',
        secondary_y=True,
    )
    fig.update_layout(
        height=figsize[1] * nrows + 120,
        width=figsize[0] * ncols,
        showlegend=False,
        barmode="overlay",
    )
    return plotly.io.to_html(fig, full_html=False)
