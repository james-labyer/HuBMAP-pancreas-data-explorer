import pandas as pd
from dash import html, register_page
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

register_page(
    __name__,
    path="/p1-14a-optical-clearing",
    title="P1-14A Optical Clearing Files",
)

data = pd.read_csv("assets/P1_14A_Optical_Clearing_imgs.csv")

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
    id="P1-14A-oc-grid",
    rowData=data.to_dict("records"),
    columnDefs=columns,
    className="ag-theme-alpine block-grid large",
    style={"height": 700, "width": 1050},
)

layout = html.Div(
    children=[
        html.Main(
            children=[
                dbc.Container(
                    class_name="main-div",
                    children=[
                        html.Header(html.H2("P1-14A Optical Clearing Files")),
                        grid,
                    ],
                ),
            ],
        ),
    ]
)
