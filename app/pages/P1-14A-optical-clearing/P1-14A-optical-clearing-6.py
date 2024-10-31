from dash import html, callback, Input, Output, get_app, register_page
import dash_bootstrap_components as dbc
from dash_slicer import VolumeSlicer
from bioio import BioImage
import bioio_czi
txt2 =register_page(
    __name__,
    path="/P1-14A-optical-clearing/P1-14A-optical-clearing-6",
    title="P1-14A optical clearing #6",
)
breadcrumb = dbc.Breadcrumb(
    items=[
        {"label": "Home", "href": "/", "external_link": False},
       {
            "label": "P1-14A optical clearing",
            "href": "/layout2",
            "external_link": True,
        },
        {"label": "P1-14A optical clearing #6", "active": True},
    ],
)
slices_img = BioImage("assets/optical-clearing-czi/P1_14A1_KRT green INS white stack_Maximum intensity projection.czi", reader=bioio_czi.Reader)
vol = slices_img.data[0][0]
slicer1 = VolumeSlicer(get_app(), vol)
slicer1.graph.config["scrollZoom"] = False
vol2 = slices_img.data[0][1]
slicer2 = VolumeSlicer(get_app(), vol2)
slicer2.graph.config["scrollZoom"] = False
layout = [
    breadcrumb,
    html.Section(
        id="P1-14A-optical-clearing-6",
        className="slicer-card",
        children=[
            html.Header(html.H2("View P1-14A optical clearing #6")),
            html.Header(html.P("P1_14A1_KRT green INS white stack_Maximum intensity projection.czi")),
            html.Div(
                [
                    html.Div(
                        children=[
                            slicer1.graph,
                            slicer1.slider,
                            *slicer1.stores,
                        ],
                    ),
                    html.Div(
                        children=[
                            slicer2.graph,
                            slicer2.slider,
                            *slicer2.stores,
                        ],
                    ),
                ]
            ),
        ],
    ),
]
