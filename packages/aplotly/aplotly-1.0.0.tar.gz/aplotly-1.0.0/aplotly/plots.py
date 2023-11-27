import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .style import configure_plotly


def plot_line(
    series: pd.Series,
    label: str,
    ylabel: str,
    xlabel: str,
    legend: bool = True,
    color_palette: str = "",
    group_title: str = "",
    plot_title: str = "",
) -> go.Figure:
    configure_plotly(subplots=1, color_palette=color_palette)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=series.index,
            y=series.values,
            mode="lines",
            name=label,
            legendgroup=1,
            legendgrouptitle_text=group_title,
            line=dict(width=2),
        )
    )
    fig.update_xaxes(title_text=xlabel)
    fig.update_yaxes(title_text=ylabel)
    fig.update_layout(showlegend=legend, title_text=plot_title)

    return fig


def plot_multiple_lines(
    series: list,
    ylabel: str,
    xlabel: str,
    labels: list = None,
    visible: list = None,
    legend: bool = True,
    color_palette: str = "",
    group_title: str = "",
    plot_title: str = "",
) -> go.Figure:
    if labels is None:
        labels = [None] * len(series)

    if visible is None:
        visible = [True] * len(series)

    configure_plotly(subplots=1, color_palette=color_palette)
    fig = go.Figure()
    for data, label, visibility in zip(series, labels, visible):
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data.values,
                mode="lines",
                name=label,
                legendgroup=1,
                legendgrouptitle_text=group_title,
                visible=visibility,
                line=dict(width=2),
            )
        )
    fig.update_xaxes(title_text=xlabel)
    fig.update_yaxes(title_text=ylabel)
    fig.update_layout(showlegend=legend, title_text=plot_title)

    return fig


def plot_performance(
    performance: pd.Series,
    drawdown: pd.Series,
    performance_label: str,
    drawdown_label: str,
    performance_ylabel: str = "PnL (%)",
    drawdown_ylabel: str = "Drawdown (%)",
    xlabel: str = "Date",
    legend: bool = True,
    color_palette: str = "",
    performance_group_title: str = "Performance",
    drawdown_group_title: str = "Drawdown",
    plot_title: str = "",
) -> go.Figure:
    configure_plotly(subplots=2, color_palette=color_palette)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.7, 0.3])
    fig.add_trace(
        go.Scatter(
            x=performance.index,
            y=performance,
            mode="lines",
            name=performance_label,
            legendgroup=1,
            legendgrouptitle_text=performance_group_title,
            line=dict(width=2),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=drawdown.index,
            y=drawdown,
            mode="lines",
            name=drawdown_label,
            legendgroup=2,
            legendgrouptitle_text=drawdown_group_title,
            line=dict(width=2),
        ),
        row=2,
        col=1,
    )

    fig.update_yaxes(title_text=performance_ylabel, row=1, col=1)
    fig.update_yaxes(title_text=drawdown_ylabel, row=2, col=1)
    fig.update_xaxes(title_text=xlabel, row=2, col=1)
    fig.update_layout(showlegend=legend, title_text=plot_title)

    return fig


def plot_multiple_performance(
    performance: list,
    drawdown: list,
    labels: list = None,
    performance_ylabel: str = "PnL (%)",
    drawdown_ylabel: str = "Drawdown (%)",
    xlabel: str = "Date",
    legend: bool = True,
    color_palette: str = "",
    performance_group_title: str = "Performance",
    drawdown_group_title: str = "Drawdown",
    plot_title: str = "",
) -> go.Figure:
    if len(performance) != len(drawdown):
        raise ValueError("performance and drawdown must have the same length")
    
    if labels is None:
        labels = [None] * len(performance)

    configure_plotly(subplots=2, color_palette=color_palette)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.7, 0.3])
    for _performance, _drawdown, label in zip(performance, drawdown, labels):
        fig.add_trace(
            go.Scatter(
                x=_performance.index,
                y=_performance,
                mode="lines",
                name=label,
                legendgroup=1,
                legendgrouptitle_text=performance_group_title,
                line=dict(width=2),
            ),
            row=1,
            col=1,
        )

        fig.for_each_trace(lambda trace: trace.update(line=dict(color=trace.marker.color)))

        fig.add_trace(
            go.Scatter(
                x=_drawdown.index,
                y=_drawdown,
                mode="lines",
                name=label,
                legendgroup=2,
                legendgrouptitle_text=drawdown_group_title,
                line=dict(width=2),
            ),
            row=2,
            col=1,
        )

    fig.update_yaxes(title_text=performance_ylabel, row=1, col=1)
    fig.update_yaxes(title_text=drawdown_ylabel, row=2, col=1)
    fig.update_xaxes(title_text=xlabel, row=2, col=1)
    fig.update_layout(showlegend=legend, title_text=plot_title)

    return fig

def plot_bars(
    df: pd.DataFrame, 
    ylabel: str = "",
    xlabel: str = "",
    legend: bool = True,
    color_palette: str = "",
    group_title: str = "",
    plot_title: str = ""
    ) -> go.Figure:
    configure_plotly(subplots=1, color_palette=color_palette)
    # split the stack
    labels = df.variable.unique()
    values = {label: df[df.variable == label].value for label in labels}
    years = df.Year.unique()

    data = [
        go.Bar(name=label, x=years, y=values[label], legendgroup=1, legendgrouptitle_text=group_title)
        for label in labels
    ]
    fig = go.Figure(data=data)

    fig.update_yaxes(title_text=ylabel)
    fig.update_xaxes(title_text=xlabel)
    fig.update_layout(showlegend=legend, title_text=plot_title)

    return fig


def plot_returns_tree(
    returns: pd.DataFrame,
    exposure: pd.DataFrame,
    metric: str = "total_return",
    root_color: str = "black",
    color_path: list = ["red", "grey", "green"],
    color_bar: bool = False,
    plot_title: str = ""
):
    if metric not in ["max_return", "avg_return", "std_return", "total_return"]:
        raise ValueError("metric must be either 'max_return', 'avg_return', 'std_return' or 'total_return'")

    metrics = []
    for column in exposure.columns:
        _exposure = exposure[column]
        _exposure = _exposure[_exposure != 0]
        try:
            _metrics = {
                "name": column,
                "max_return": returns.loc[_exposure.index, column].max(),
                "avg_return": returns.loc[_exposure.index, column].mean(),
                "std_return": returns.loc[_exposure.index, column].std(),
                "total_return": (returns.loc[_exposure.index, column] + 1).cumprod().iloc[-1] - 1,
            }
            metrics.append(_metrics)
        except:
            continue

    metrics = pd.DataFrame(metrics)
    sizes = metrics[metric].abs()
    colors = metrics[metric]
    labels = metrics["name"]

    configure_plotly(1, "alpha_nine")
    fig = go.Figure(
        go.Treemap(
            labels=labels,
            parents=[""] * len(labels),
            values=sizes,
            customdata=colors,
            hovertemplate="<b>%{label}</b><br>%{customdata:.2%}",
            texttemplate="%{label}<br>%{customdata:.2%}",
            textposition="middle center",
            textfont=dict(size=18),
            marker=dict(
                colors=colors,
                colorscale=color_path,
                cmid=0,
                showscale=color_bar,
                line=dict(width=0),
            ),
            tiling=dict(
                packing="squarify",
                pad=1,
            ),
            root_color=root_color,
        )
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), title_text=plot_title)

    fig.data[0].customdata = colors.values
    fig.data[0].texttemplate = "%{label}<br>%{customdata:.2%}"

    return fig