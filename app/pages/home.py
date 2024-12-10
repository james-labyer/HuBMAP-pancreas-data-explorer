import logging

import dash_ag_grid as dag
import pandas as pd
from dash import html, register_page

register_page(__name__, path="/", title="HuBMAP Pancreas Data Explorer")
app_logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
app_logger.handlers = gunicorn_logger.handlers
app_logger.setLevel(gunicorn_logger.level)

blocks = pd.read_csv("assets/block-data.csv")

app_logger.debug(f"Data columns imported for home page grid:\n{blocks.columns}")


def make_grid(pancreas="P1"):
    p = blocks.loc[blocks["Pancreas"] == pancreas]
    prows = p.to_dict("records")
    pheight = len(prows) * 41.25 + 49 + 15

    return dag.AgGrid(
        id=f"{pancreas}-df",
        rowData=prows,
        columnDefs=columns,
        className="ag-theme-alpine block-grid",
        columnSize="sizeToFit",
        style={"height": pheight},
    )


columns = [
    {"field": "Order"},
    {"field": "Block ID"},
    {"field": "Anatomical region"},
    {"field": "Optical clearing", "cellRenderer": "dsLink"},
    {"field": "GeoMx", "cellRenderer": "dsLink"},
    {"field": "Proteomics", "cellRenderer": "dsLink"},
]

layout = html.Div(
    [
        html.Section([html.Header(html.H2("Pancreas 1 Datasets")), make_grid("P1")]),
        html.Section(
            [
                html.Header(html.H2("Pancreas 2 Datasets"), className="middle-section"),
                make_grid("P2"),
            ]
        ),
    ]
)
