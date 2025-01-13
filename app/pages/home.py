import logging

import dash_ag_grid as dag
import pandas as pd
from dash import html, register_page

register_page(__name__, path="/")

app_logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
app_logger.handlers = gunicorn_logger.handlers
app_logger.setLevel(gunicorn_logger.level)

blocks = pd.read_csv("../config/blocks.csv")
organs = blocks["Organ ID"].unique()

app_logger.debug(f"Data columns imported for home page grid:\n{blocks.columns}")

columns = [
    {"field": "Order"},
    {"field": "Tissue Block"},
    {"field": "Anatomical region"},
    {"field": "Images", "cellRenderer": "dsLink"},
    {"field": "Reports", "cellRenderer": "dsLink"},
    {"field": "Proteomics", "cellRenderer": "dsLink"},
]


def make_grid(organ="P1"):
    o = blocks.loc[blocks["Organ ID"] == organ]
    orows = o.to_dict("records")
    oheight = len(orows) * 41.25 + 49 + 15

    return dag.AgGrid(
        id=f"{organ}-df",
        rowData=orows,
        columnDefs=columns,
        className="ag-theme-alpine block-grid",
        columnSize="sizeToFit",
        style={"height": oheight},
    )


def layout():
    sections = []
    for organ in organs:
        organ_data = blocks.loc[blocks["Organ ID"] == organ]
        # assumes they have set the organ description consistently
        organ_desc = organ_data.at[organ_data.index[0], "Organ Description"]
        if len(sections) == 0:
            section = html.Section(
                [html.Header(html.H2(f"{organ_desc} Datasets")), make_grid(organ)]
            )
        else:
            section = section = html.Section(
                [
                    html.Header(
                        html.H2(f"{organ_desc} Datasets"), className="middle-section"
                    ),
                    make_grid(organ),
                ]
            )
        sections.append(section)
    return html.Div(sections)
