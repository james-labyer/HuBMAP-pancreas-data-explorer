import pandas as pd
from dash import html, register_page
import dash_ag_grid as dag
import logging


def title(block=None, pancreas=None):
    return f"{block} optical clearing"


register_page(
    __name__,
    path_template="/optical-clearing-files/<block>",
    path="/optical-clearing-files/P1-19A",
    title=title,
)

thumbnails = pd.read_csv("assets/optical-clearing-czi/oc-thumbnails.csv")


def layout(block=None, **kwargs):
    block_thumbnails = thumbnails.loc[thumbnails["Block"] == block]

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
        id="oc-files-grid",
        rowData=block_thumbnails.to_dict("records"),
        columnDefs=columns,
        className="ag-theme-alpine block-grid large",
        style={"height": 700},
    )

    return html.Div(
        html.Section(
            children=[
                html.Header(html.H2(f"{block} Optical Clearing Files")),
                grid,
            ],
        )
    )
