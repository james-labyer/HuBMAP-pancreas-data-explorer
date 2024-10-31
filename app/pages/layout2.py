import pandas as pd
from dash import html, register_page
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

register_page(__name__, title="Test Dataset Page 2")

data = pd.read_csv("assets/P1_14A_Optical_Clearing_imgs.csv")

columns = [
    {"field": "Preview", "cellRenderer": "previewImg"},
    {"field": "Name"},
    {"field": "Link", "cellRenderer": "dsLink"},
]

grid = dag.AgGrid(
    id="layout2-grid",
    rowData=data.to_dict("records"),
    columnDefs=columns,
    className="ag-theme-alpine block-grid large",
    columnSize="autoSize",
    style={"height": 700, "width": 765},
)

layout = html.Div(
    children=[
        html.Main(
            children=[
                dbc.Container(
                    class_name="main-div",
                    children=[html.Header(html.H2("Dataset Test 2")), grid],
                ),
            ],
        ),
    ]
)
