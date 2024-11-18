from dash import html, dcc, callback, Input, Output, get_app, register_page
import dash_bootstrap_components as dbc
from dash_slicer import VolumeSlicer
import logging
from bioio import BioImage
import bioio_czi

slices_img = BioImage("assets/optical-clearing-czi/P1-14A/P1_14A1_KRT green INS white stack_Maximum intensity projection.czi", reader=bioio_czi.Reader)
vols = slices_img.data[0]
txt2 =register_page(
    __name__,
    path="/p1-14a-optical-clearing/p1-14a-optical-clearing-6",
    title="P1-14A optical clearing #6",
)
vol0 = vols[0]
slicer0 = VolumeSlicer(get_app(), vol0)
slicer0.graph.config["scrollZoom"] = False
logging.debug(
    f'Added slicer0 with {slicer0.nslices} slices to P1-14A-optical-clearing-6'
)
vol1 = vols[1]
slicer1 = VolumeSlicer(get_app(), vol1)
slicer1.graph.config["scrollZoom"] = False
logging.debug(
    f'Added slicer1 with {slicer1.nslices} slices to P1-14A-optical-clearing-6'
)
layout = [
    html.Section(
        id="P1-14A-optical-clearing-6",
        children=[
            html.Header(html.H2("View P1-14A optical clearing #6")),
            html.P("P1_14A1_KRT green INS white stack_Maximum intensity projection.czi"),
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
                        id="btn-download-P1-14A-optical-clearing-6",
                        className="download-button",
                    ),
                    dcc.Download(id="download-P1-14A-optical-clearing-6"),
                ]
            ),
        ],
    ),
]
@callback(
    Output("download-P1-14A-optical-clearing-6", "data"),
    Input("btn-download-P1-14A-optical-clearing-6", "n_clicks"),
    prevent_initial_call=True,
)
def download_czi(n_clicks):
    logging.info(
        "Sending P1_14A1_KRT green INS white stack_Maximum intensity projection.czi"
    )
    return dcc.send_file(
        "assets/optical-clearing-czi/P1-14A/P1_14A1_KRT green INS white stack_Maximum intensity projection.czi"
    )
