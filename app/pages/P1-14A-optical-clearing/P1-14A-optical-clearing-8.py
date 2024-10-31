from dash import html, callback, Input, Output, get_app, register_page
import dash_bootstrap_components as dbc
from dash_slicer import VolumeSlicer
from bioio import BioImage
import bioio_czi
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
            "href": "/layout2",
            "external_link": True,
        },
        {"label": "P1-14A optical clearing #8", "active": True},
    ],
)
colors = ["#{:02x}{:02x}{:02x}".format(0, i, 0) for i in range(0, 256, 1)]
slices_img = BioImage("assets/optical-clearing-czi/P1_14A1_KRT green stack.czi", reader=bioio_czi.Reader)
vol = slices_img.data[0][0]
slicer1 = VolumeSlicer(get_app(), vol)
slicer1.graph.config["scrollZoom"] = False
layout = [
    breadcrumb,
    html.Section(
        id="P1-14A-optical-clearing-8",
        className="slicer-card",
        children=[
            html.Header(html.H2("View P1-14A optical clearing #8")),
            html.Header(html.P("P1_14A1_KRT green stack.czi")),
            html.Div(
                children=[
                    slicer1.graph,
                    slicer1.slider,
                    *slicer1.stores,
                ],
            ),
        ],
    ),
]
@callback(
    Output(slicer1.overlay_data.id, "data"),
    Input("P1-14A-optical-clearing-8", "children"),
    Input(slicer1.slider, "value"),
)
def apply_levels(level, children):
    return slicer1.create_overlay_data(vol, colors)
