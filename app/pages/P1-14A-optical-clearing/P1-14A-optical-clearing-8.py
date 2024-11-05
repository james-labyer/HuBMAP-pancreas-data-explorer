from dash import html, dcc, callback, Input, Output, get_app, register_page
import dash_bootstrap_components as dbc
from dash_slicer import VolumeSlicer
from bioio import BioImage
import bioio_czi

slices_img = BioImage("assets/optical-clearing-czi/P1_14A1_KRT green stack.czi", reader=bioio_czi.Reader)
vols = slices_img.data[0]
txt2 =register_page(
    __name__,
    path="/P1-14A-optical-clearing/P1-14A-optical-clearing-8",
    title="P1-14A optical clearing #8",
)
breadcrumb = dbc.Breadcrumb(
    items=[
        {"label": "Home", "href": "/", "external_link": False},
       {
            "label": "P1-14A optical clearing",
            "href": "/p1-14a-optical-clearing-files",
            "external_link": True,
        },
        {"label": "P1-14A optical clearing #8", "active": True},
    ],
)
colors = ["#{:02x}{:02x}{:02x}".format(0, i, 0) for i in range(0, 256, 1)]
vol0 = vols[0]
slicer0 = VolumeSlicer(get_app(), vol0)
slicer0.graph.config["scrollZoom"] = False
layout = [
    breadcrumb,
    html.Section(
        id="P1-14A-optical-clearing-8",
        className="slicer-card",
        children=[
            html.Header(html.H2("View P1-14A optical clearing #8")),
            html.P("P1_14A1_KRT green stack.czi"),
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
                        id="btn-download-P1-14A-optical-clearing-8",
                        className="download-button",
                    ),
                    dcc.Download(id="download-P1-14A-optical-clearing-8"),
                ]
            ),
        ],
    ),
]
@callback(
    Output(slicer0.overlay_data.id, "data"),
    Input("P1-14A-optical-clearing-8", "children"),
    Input(slicer0.slider, "value"),
)
def apply_levels(level, children):
    return slicer0.create_overlay_data(vol0, colors)
@callback(
    Output("download-P1-14A-optical-clearing-8", "data"),
    Input("btn-download-P1-14A-optical-clearing-8", "n_clicks"),
    prevent_initial_call=True,
)
def download_czi(n_clicks):
    return dcc.send_file(
        "assets/optical-clearing-czi/P1_14A1_KRT green stack.czi"    )
