import os

import plotly.graph_objects as go

from .colors import select_palette


def save_figure(fig: go.Figure, file_path: str, figsize: tuple = (1000, 600)) -> None:
    if file_path == "":
        raise ValueError("file_path cannot be empty")
    elif "." not in file_path:
        raise ValueError("file_path must contain a file extension")
    elif file_path.split(".")[-1] not in ["html", "png", "svg"]:
        raise ValueError("file_path must end with either 'html', 'svg' or 'png'")

    file_format = file_path.split(".")[-1]

    if file_format == "html":
        save_html(fig, file_path)

    elif file_format == "png":
        save_png(fig, file_path, figsize)

    elif file_format == "svg":
        save_svg(fig, file_path, figsize)


def save_html(fig: go.Figure, file_path: str):
    if os.environ.get("COLOR_PALETTE") is not None:
        color_palette = os.environ.get("COLOR_PALETTE")
        chart_colors = select_palette(color_palette, "rgba")[1]
        html = fig.to_html().replace(
            "<body>", f"<body style='margin:0;padding:0;background-color:{chart_colors['background']}'>"
        )

    else:
        html = fig.to_html()

    with open(file_path, "w") as f:
        f.write(html)


def save_png(fig: go.Figure, file_path: str, figsize: tuple = (1000, 600)):
    fig.write_image(file_path, width=figsize[0], height=figsize[1], scale=2)


def save_svg(fig: go.Figure, file_path: str, figsize: tuple = (1000, 600)):
    fig.write_image(
        file_path,
        width=figsize[0],
        height=figsize[1],
    )
