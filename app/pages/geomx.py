import logging

import dash_ag_grid as dag
import pandas as pd
from dash import html, register_page

app_logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
app_logger.handlers = gunicorn_logger.handlers
app_logger.setLevel(gunicorn_logger.level)


def title(pancreas="P1"):
    if not pancreas:
        return "Invalid report request"
    else:
        return f"Pancreas {pancreas[-1]} GeoMx reports"


register_page(
    __name__,
    path_template="/geomx/<pancreas>",
    path="/geomx/P1",
    title=title,
)

reports = pd.read_csv("assets/geomx-reports.csv")


def layout(pancreas="P1", **kwargs):
    app_logger.debug(f"Data columns imported for report link list:\n{reports.columns}")

    p_reports = reports.loc[reports["pancreas"] == pancreas]

    columns = [
        {"field": "name", "flex": 3},
        {"field": "link", "cellRenderer": "dsLink", "flex": 1},
    ]

    grid = dag.AgGrid(
        id="geo-reports-grid",
        rowData=p_reports.to_dict("records"),
        columnDefs=columns,
        className="ag-theme-alpine block-grid",
        columnSize="sizeToFit",
        style={"height": 230},
    )

    return html.Div(
        html.Section(
            children=[
                html.Header(html.H2(f"Pancreas {pancreas[-1]} GeoMx reports")),
                grid,
            ],
        )
    )
