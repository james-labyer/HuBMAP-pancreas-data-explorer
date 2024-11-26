import pandas as pd
from dash import html, register_page
import dash_ag_grid as dag
import logging

register_page(
    __name__,
    path="/optical-clearing/P1/P1-19A",
    title="P1-19A Optical Clearing Files",
)

data = pd.read_csv("assets/P1_19A_Optical_Clearing_imgs.csv")

logging.debug(f"Data columns imported for p1-19a-optical-clearing:\n{data.columns}")

columns = [
    {
        "field": "Preview",
        "cellRenderer": "previewImg",
        "flex": 2,
        "cellClass": "center-aligned-cell",
        "headerClass": "center-aligned-header ag-header-cell-label",
    },
    {"field": "Name", "flex": 3},
    {"field": "Link", "cellRenderer": "dsLink", "flex": 1},
]

grid = dag.AgGrid(
    id="P1-19A-oc-grid",
    rowData=data.to_dict("records"),
    columnDefs=columns,
    className="ag-theme-alpine block-grid large",
    style={"height": 700},
)

layout = html.Div(
    html.Section(
        children=[
            html.Header(html.H2("P1-19A Optical Clearing Files")),
            grid,
        ],
    )
)
