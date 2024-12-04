import pandas as pd
from dash import html, register_page
import dash_ag_grid as dag
import logging

register_page(__name__, path="/", title="HuBMAP Pancreas Data Explorer")

blocks = pd.read_csv("assets/block-data.csv")

logging.debug(f"Data columns imported for home page grid:\n{blocks.columns}")

columns = [
    {"field": "Order"},
    {"field": "Block ID"},
    {"field": "Anatomical region"},
    {"field": "Optical clearing", "cellRenderer": "dsLink"},
    {"field": "GeoMx", "cellRenderer": "dsLink"},
    {"field": "Proteomics", "cellRenderer": "dsLink"},
]

grid = dag.AgGrid(
    id="blocks-df",
    rowData=blocks.to_dict("records"),
    columnDefs=columns,
    className="ag-theme-alpine block-grid",
    columnSize="sizeToFit",
    style={"height": 490},
)


layout = html.Section([html.Header(html.H2("Pancreas 1 Datasets")), grid])
