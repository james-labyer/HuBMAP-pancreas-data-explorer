import dash_bootstrap_components as dbc
import logging
from dash import html, dcc, callback, Input, Output, get_app, register_page
from dash_slicer import VolumeSlicer
from bioio import BioImage
import bioio_czi

slices_img = BioImage(
    "assets/optical-clearing-czi/P1-19A/P1_19A2 INS tile scan_Stitch.czi",
    reader=bioio_czi.Reader,
)
vols = slices_img.data[0]
txt2 = register_page(
    __name__,
    path="/p1-19a-optical-clearing/p1-19a-optical-clearing-10",
    title="P1-19A optical clearing #10",
)
vol0 = vols[0]
slicer0 = VolumeSlicer(get_app(), vol0)
slicer0.graph.config["scrollZoom"] = False
logging.debug(
    f"Added slicer0 with {slicer0.nslices} slices to P1-19A-optical-clearing-10"
)
layout = [
    html.Section(
        id="P1-19A-optical-clearing-10",
        children=[
            html.Header(html.H2("View P1-19A optical clearing #10")),
            html.P("P1_19A2 INS tile scan_Stitch.czi"),
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
                        id="btn-download-P1-19A-optical-clearing-10",
                        className="download-button",
                    ),
                    dcc.Download(id="download-P1-19A-optical-clearing-10"),
                ]
            ),
        ],
    ),
]


@callback(
    Output("download-P1-19A-optical-clearing-10", "data"),
    Input("btn-download-P1-19A-optical-clearing-10", "n_clicks"),
    prevent_initial_call=True,
)
def download_file(n_clicks):
    logging.info("Sending P1_19A2 INS tile scan_Stitch.czi")
    return dcc.send_file(
        "assets/optical-clearing-czi/P1-19A/P1_19A2 INS tile scan_Stitch.czi"
    )
