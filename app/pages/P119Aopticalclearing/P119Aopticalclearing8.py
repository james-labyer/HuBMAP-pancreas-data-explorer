from dash import html, dcc, callback, Input, Output, get_app, register_page
import dash_bootstrap_components as dbc
from dash_slicer import VolumeSlicer
import logging
import numpy as np
import imageio.v3 as iio

im = iio.imread(
'assets/optical-clearing-czi/P1-19A/P1_19A2 CD31 red INS white stack_Maximum intensity projection.tif'
)
vols = []
vols.append(np.expand_dims(im[0], axis=0))
vols.append(np.expand_dims(im[1], axis=0))
txt2 =register_page(
    __name__,
    path="/p1-19a-optical-clearing/p1-19a-optical-clearing-8",
    title="P1-19A optical clearing #8",
)
colors = ["#{:02x}{:02x}{:02x}".format(i, 0, 0) for i in range(0, 256, 1)]
vol0 = vols[0]
slicer0 = VolumeSlicer(get_app(), vol0)
slicer0.graph.config["scrollZoom"] = False
logging.debug(
    f'Added slicer0 with {slicer0.nslices} slices to P1-19A-optical-clearing-8'
)
vol1 = vols[1]
slicer1 = VolumeSlicer(get_app(), vol1)
slicer1.graph.config["scrollZoom"] = False
logging.debug(
    f'Added slicer1 with {slicer1.nslices} slices to P1-19A-optical-clearing-8'
)
layout = [
    html.Section(
        id="P1-19A-optical-clearing-8",
        children=[
            html.Header(html.H2("View P1-19A optical clearing #8")),
            html.P("P1_19A2 CD31 red INS white stack_Maximum intensity projection.czi"),
            html.Div(
                [
                    html.Div(
                        children=[
                            slicer0.graph,
                            slicer0.slider,
                            *slicer0.stores,
                        ],
                        className="slicer",
                    ),
                    html.Div(
                        children=[
                            slicer1.graph,
                            slicer1.slider,
                            *slicer1.stores,
                        ],
                        className="slicer",
                    ),
                ]
            ),
            html.Div(
                children=[
                    html.H2("Download file"),
                    html.P(
                        "The easiest way to open this file is to use Fiji with the Bio-Formats plugin installed."
                    ),
                    dbc.Button(
                        "Download .czi",
                        id="btn-download-P1-19A-optical-clearing-8",
                        className="download-button",
                    ),
                    dcc.Download(id="download-P1-19A-optical-clearing-8"),
                ]
            ),
        ],
    ),
]
@callback(
    Output(slicer1.overlay_data.id, "data"),
    Input("P1-19A-optical-clearing-8", "children"),
    Input(slicer1.slider, "value"),
)
def apply_overlay(level, children):
    logging.info("Creating overlay on P1-19A-optical-clearing-8")
    return slicer1.create_overlay_data(vol1, colors)
@callback(
    Output("download-P1-19A-optical-clearing-8", "data"),
    Input("btn-download-P1-19A-optical-clearing-8", "n_clicks"),
    prevent_initial_call=True,
)
def download_czi(n_clicks):
    logging.info(
        "Sending P1_19A2 CD31 red INS white stack_Maximum intensity projection.czi"
    )
    return dcc.send_file(
        "assets/optical-clearing-czi/P1-19A/P1_19A2 CD31 red INS white stack_Maximum intensity projection.czi"
    )
