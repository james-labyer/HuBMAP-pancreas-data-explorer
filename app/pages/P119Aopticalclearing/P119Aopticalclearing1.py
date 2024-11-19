import dash_bootstrap_components as dbc
import logging
from dash import html, dcc, callback, Input, Output, register_page
from PIL import Image

txt2 = register_page(
    __name__,
    path="/p1-19a-optical-clearing/p1-19a-optical-clearing-1",
    title="P1-19A optical clearing #1",
)
layout = [
    html.Section(
        id="P1-19A-optical-clearing-1",
        children=[
            html.Header(html.H2("View P1-19A optical clearing #1")),
            html.P("P1_19A AF_CD31.avi"),
            html.Div(
                [
                    dbc.Card(
                        [
                            html.Div(
                                id="P1-19A-optical-clearing-1-slider-output",
                                className="custom-slicer-div",
                            ),
                            dbc.CardBody(
                                dcc.Slider(
                                    1,
                                    60,
                                    1,
                                    value=1,
                                    id="P1-19A-optical-clearing-1-slider",
                                ),
                            ),
                        ],
                        class_name="slicer-card",
                    ),
                ]
            ),
            html.Div(
                children=[
                    html.H2("Download file", className="download-header"),
                    dbc.Button(
                        "Download",
                        id="btn-download-P1-19A-optical-clearing-1",
                        className="download-button",
                    ),
                    dcc.Download(id="download-P1-19A-optical-clearing-1"),
                ]
            ),
        ],
    ),
]


@callback(
    Output("P1-19A-optical-clearing-1-slider-output", "children"),
    Input("P1-19A-optical-clearing-1-slider", "value"),
)
def update_pic(value):
    val = value - 1
    val_str = f"{val:04}"
    pic = Image.open(
        f"assets/optical-clearing-czi/P1-19A//P1_19A AF_CD31/P1_19A AF_CD31{val_str}.png"
    )
    return html.Img(src=pic, className="custom-slicer-img")


@callback(
    Output("download-P1-19A-optical-clearing-1", "data"),
    Input("btn-download-P1-19A-optical-clearing-1", "n_clicks"),
    prevent_initial_call=True,
)
def download_file(n_clicks):
    logging.info("Sending P1_19A AF_CD31.avi")
    return dcc.send_file("assets/optical-clearing-czi/P1-19A/P1_19A AF_CD31.avi")
