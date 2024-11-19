import dash_bootstrap_components as dbc
import logging
from dash import html, dcc, callback, Input, Output, register_page
from PIL import Image

txt2 = register_page(
    __name__,
    path="/p1-19a-optical-clearing/p1-19a-optical-clearing-11",
    title="P1-19A optical clearing #11",
)
layout = [
    html.Section(
        id="P1-19A-optical-clearing-11",
        children=[
            html.Header(html.H2("View P1-19A optical clearing #11")),
            html.P("P1_19A2__z_stack__no_tiling__not_isotropic_dx_dy_dz_sampling.avi"),
            html.Div(
                [
                    dbc.Card(
                        [
                            html.Div(
                                id="P1-19A-optical-clearing-11-slider-output",
                                className="custom-slicer-div",
                            ),
                            dbc.CardBody(
                                dcc.Slider(
                                    1,
                                    60,
                                    1,
                                    value=1,
                                    id="P1-19A-optical-clearing-11-slider",
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
                        id="btn-download-P1-19A-optical-clearing-11",
                        className="download-button",
                    ),
                    dcc.Download(id="download-P1-19A-optical-clearing-11"),
                ]
            ),
        ],
    ),
]


@callback(
    Output("P1-19A-optical-clearing-11-slider-output", "children"),
    Input("P1-19A-optical-clearing-11-slider", "value"),
)
def update_pic(value):
    val = value - 1
    val_str = f"{val:04}"
    pic = Image.open(
        f"assets/optical-clearing-czi/P1-19A//P1_19A2__z_stack__no_tiling__not_isotropic_dx_dy_dz_sampling/P1_19A2__z_stack__no_tiling__not_isotropic_dx_dy_dz_sampling{val_str}.png"
    )
    return html.Img(src=pic, className="custom-slicer-img")


@callback(
    Output("download-P1-19A-optical-clearing-11", "data"),
    Input("btn-download-P1-19A-optical-clearing-11", "n_clicks"),
    prevent_initial_call=True,
)
def download_file(n_clicks):
    logging.info(
        "Sending P1_19A2__z_stack__no_tiling__not_isotropic_dx_dy_dz_sampling.avi"
    )
    return dcc.send_file(
        "assets/optical-clearing-czi/P1-19A/P1_19A2__z_stack__no_tiling__not_isotropic_dx_dy_dz_sampling.avi"
    )
