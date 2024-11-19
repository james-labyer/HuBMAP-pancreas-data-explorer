import dash_bootstrap_components as dbc
import logging
from dash import html, dcc, callback, Input, Output, get_app, register_page
from dash_slicer import VolumeSlicer
import numpy as np
import imageio.v3 as iio

im = iio.imread(
'assets/optical-clearing-czi/P1-7A/P1_7A2_KRT CD31 INS tile 2_Stitch.tif'
)
vols = []
vols.append(np.expand_dims(im[0], axis=0))
vols.append(np.expand_dims(im[1], axis=0))
vols.append(np.expand_dims(im[2], axis=0))
txt2 =register_page(
    __name__,
    path="/p1-7a-optical-clearing/p1-7a-optical-clearing-3",
    title="P1-7A optical clearing #3",
)
greens = ["#{:02x}{:02x}{:02x}".format(0, i, 0) for i in range(0, 256, 1)]
reds = ["#{:02x}{:02x}{:02x}".format(i, 0, 0) for i in range(0, 256, 1)]
vol0 = vols[0]
slicer0 = VolumeSlicer(get_app(), vol0)
slicer0.graph.config["scrollZoom"] = False
logging.debug(
    f'Added slicer0 with {slicer0.nslices} slices to P1-7A-optical-clearing-3'
)
vol1 = vols[1]
slicer1 = VolumeSlicer(get_app(), vol1)
slicer1.graph.config["scrollZoom"] = False
logging.debug(
    f'Added slicer1 with {slicer1.nslices} slices to P1-7A-optical-clearing-3'
)
vol2 = vols[2]
slicer2 = VolumeSlicer(get_app(), vol2)
slicer2.graph.config["scrollZoom"] = False
logging.debug(
    f'Added slicer2 with {slicer2.nslices} slices to P1-7A-optical-clearing-3'
)
layout = [
    html.Section(
        id="P1-7A-optical-clearing-3",
        children=[
            html.Header(html.H2("View P1-7A optical clearing #3")),
            html.P("P1_7A2_KRT CD31 INS tile 2_Stitch.czi"),
            html.Div(
                [
                    dbc.Card(
                        dbc.CardBody(
                             children=[
                                slicer0.graph,
                                slicer0.slider,
                                *slicer0.stores,
                            ],
                            className="slicer",
                        ),
                        class_name="slicer-card",
                    ),
                    dbc.Card(
                        dbc.CardBody(
                             children=[
                                slicer1.graph,
                                slicer1.slider,
                                *slicer1.stores,
                            ],
                            className="slicer",
                        ),
                        class_name="slicer-card",
                    ),
                    dbc.Card(
                        dbc.CardBody(
                             children=[
                                slicer2.graph,
                                slicer2.slider,
                                *slicer2.stores,
                            ],
                            className="slicer",
                        ),
                        class_name="slicer-card",
                    ),
                ]
            ),
            html.Div(
                children=[
                    html.H2("Download file", className="download-header"),
                    html.P(
                        "The easiest way to open this file is to use Fiji with the Bio-Formats plugin installed."
                    ),
                    dbc.Button(
                        "Download",
                        id="btn-download-P1-7A-optical-clearing-3",
                        className="download-button",
                    ),
                    dcc.Download(id="download-P1-7A-optical-clearing-3"),
                ]
            ),
        ],
    ),
]
@callback(
    Output(slicer0.overlay_data.id, "data"),
    Input("P1-7A-optical-clearing-3", "children"),
    Input(slicer0.slider, "value"),
)
def apply_overlay0(level, children):
    logging.info("Creating overlay on P1-7A-optical-clearing-3")
    return slicer0.create_overlay_data(vol0, greens)
@callback(
    Output(slicer2.overlay_data.id, "data"),
    Input("P1-7A-optical-clearing-3", "children"),
    Input(slicer2.slider, "value"),
)
def apply_overlay2(level, children):
    logging.info("Creating overlay on P1-7A-optical-clearing-3")
    return slicer2.create_overlay_data(vol2, reds)
@callback(
    Output("download-P1-7A-optical-clearing-3", "data"),
    Input("btn-download-P1-7A-optical-clearing-3", "n_clicks"),
    prevent_initial_call=True,
)
def download_file(n_clicks):
    logging.info(
        "Sending P1_7A2_KRT CD31 INS tile 2_Stitch.czi"
    )
    return dcc.send_file(
        "assets/optical-clearing-czi/P1-7A/P1_7A2_KRT CD31 INS tile 2_Stitch.czi"
    )
