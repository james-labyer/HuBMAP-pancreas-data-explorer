from dash import html, dcc, callback, Input, Output, get_app, register_page
import dash_bootstrap_components as dbc
from dash_slicer import VolumeSlicer
import numpy as np
import imageio.v3 as iio

im = iio.imread(
'assets/optical-clearing-czi/P1_14A2_CD31 red INS white stack high res 2x.tif'
)
temp0 = []
temp1 = []
for i in range(14):
    temp0.append(im[i][0])
    temp1.append(im[i][1])
vols = []
vols.append(np.array(temp0))
vols.append(np.array(temp1))
txt2 =register_page(
    __name__,
    path="/P1-14A-optical-clearing/P1-14A-optical-clearing-10",
    title="P1-14A optical clearing #10",
)
breadcrumb = dbc.Breadcrumb(
    items=[
        {"label": "Home", "href": "/", "external_link": False},
       {
            "label": "P1-14A optical clearing",
            "href": "/p1-14a-optical-clearing-files",
            "external_link": True,
        },
        {"label": "P1-14A optical clearing #10", "active": True},
    ],
)
colors = ["#{:02x}{:02x}{:02x}".format(i, 0, 0) for i in range(0, 256, 1)]
vol0 = vols[0]
slicer0 = VolumeSlicer(get_app(), vol0)
slicer0.graph.config["scrollZoom"] = False
vol1 = vols[1]
slicer1 = VolumeSlicer(get_app(), vol1)
slicer1.graph.config["scrollZoom"] = False
layout = [
    breadcrumb,
    html.Section(
        id="P1-14A-optical-clearing-10",
        className="slicer-card",
        children=[
            html.Header(html.H2("View P1-14A optical clearing #10")),
            html.P("P1_14A2_CD31 red INS white stack high res 2x.czi"),
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
                    dcc.Loading(
                        [
                            html.Div(
                                children=[
                                    slicer1.graph,
                                    slicer1.slider,
                                    *slicer1.stores,
                                ],
                                className="slicer",
                            ),
                        ],
                        style={
                            "visibility": "visible",
                            "backgroundColor": "transparent",
                            "opacity": 0.5,
                        },
                        type="dot",
                        parent_className="loader-wrapper",
                    ),                ]
            ),
            html.Div(
                children=[
                    html.H2("Download file"),
                    html.P(
                        "The easiest way to open this file is to use Fiji with the Bio-Formats plugin installed."
                    ),
                    dbc.Button(
                        "Download .czi",
                        id="btn-download-P1-14A-optical-clearing-10",
                        className="download-button",
                    ),
                    dcc.Download(id="download-P1-14A-optical-clearing-10"),
                ]
            ),
        ],
    ),
]
@callback(
    Output(slicer1.overlay_data.id, "data"),
    Input("P1-14A-optical-clearing-10", "children"),
    Input(slicer1.slider, "value"),
)
def apply_levels(level, children):
    return slicer1.create_overlay_data(vol1, colors)
@callback(
    Output("download-P1-14A-optical-clearing-10", "data"),
    Input("btn-download-P1-14A-optical-clearing-10", "n_clicks"),
    prevent_initial_call=True,
)
def download_czi(n_clicks):
    return dcc.send_file(
        "assets/optical-clearing-czi/P1_14A2_CD31 red INS white stack high res 2x.czi"    )
