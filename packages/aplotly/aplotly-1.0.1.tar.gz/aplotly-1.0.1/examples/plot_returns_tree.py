import numpy as np
import pandas as pd
from aplotly.plots import plot_returns_tree


exposures = pd.DataFrame(
    np.random.uniform(-1, 1, (10, 3)),
    columns=["a", "b", "c"],
    index=np.arange(10)
)
exposures = exposures.div(exposures.sum(axis=1), axis=0)

returns = pd.DataFrame(
    np.random.uniform(-0.1, 0.1, (10, 3)),
    columns=["a", "b", "c"],
    index=np.arange(10)
)

fig = plot_returns_tree(
    returns,
    exposures,
    metric="total_return",
    root_color="black",
    color_path=["red", "grey", "green"],
    color_bar=False,
    plot_title="Returns Tree"
)
fig.show()
