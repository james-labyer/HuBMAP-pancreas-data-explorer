import logging
import math

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html, register_page

register_page(__name__, title="Block P1-20C Proteomics")
app_logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
app_logger.handlers = gunicorn_logger.handlers
app_logger.setLevel(gunicorn_logger.level)

"""
Constants and Datasets
"""

D_PROTEIN = "INS"
D_SCHEME = "haline"
D_LAYER = "All"
LAYERS = ["All", "Layer 1", "Layer 2", "Layer 3", "Layer 4"]
X_AXIS = [221, 271, 321, 371, 421, 471, 521, 571, 621, 671]
Y_AXIS = [248, 301, 354, 407, 460, 513]
Z_AXIS = [0, 35, 70, 105, 140]
C_SCHEMES = [
    "bluered",
    "deep",
    "delta",
    "greys",
    "haline",
    "ice",
    "inferno",
    "jet",
    "magma",
    "plasma",
    "spectral",
    "thermal",
    "viridis",
    "ylgnbu",
    "ylorrd",
]

cubes_df1 = pd.read_csv("assets/rectangles_output.csv")
points_df = pd.read_csv("assets/HuBMAP_ili_data10-11-24.csv")
protein_df = pd.read_csv("assets/protein_labels.csv")
proteins = protein_df.columns.tolist()

"""
Helper Functions
"""


def select_layer(zlayer, df):
    if zlayer == "All":
        return df
    elif zlayer == "Layer 1":
        return df[df["Z Center"] < 35]
    elif zlayer == "Layer 2":
        return df[(df["Z Center"] >= 35) & (df["Z Center"] < 70)]
    elif zlayer == "Layer 3":
        return df[(df["Z Center"] >= 70) & (df["Z Center"] < 105)]
    elif zlayer == "Layer 4":
        return df[df["Z Center"] >= 105]


def get_colors(df, protein):
    colors = [
        df[df["Y Center"] < 301].loc[:, protein].to_list(),
        df[(df["Y Center"] >= 301) & (df["Y Center"] < 354)].loc[:, protein].to_list(),
        df[(df["Y Center"] >= 354) & (df["Y Center"] < 407)].loc[:, protein].to_list(),
        df[(df["Y Center"] >= 407) & (df["Y Center"] < 460)].loc[:, protein].to_list(),
        df[df["Y Center"] >= 460].loc[:, protein].to_list(),
    ]
    return colors


def make_sphere(x, y, z, radius, resolution=5):
    """Calculate the coordinates to plot a sphere with center at (x, y, z). Returns three Numpy ndarrays."""
    u, v = np.mgrid[0 : 2 * np.pi : resolution * 2j, 0 : np.pi : resolution * 1j]
    X = radius * np.cos(u) * np.sin(v) + x
    Y = radius * np.sin(u) * np.sin(v) + y
    Z = radius * np.cos(v) + z
    return (X, Y, Z)


def set_layout(fig):
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                nticks=10,
                range=[X_AXIS[0], X_AXIS[-1]],
            ),
            yaxis=dict(
                nticks=6,
                range=[Y_AXIS[0], Y_AXIS[-1]],
            ),
            zaxis=dict(
                nticks=5,
                range=[Z_AXIS[0], Z_AXIS[-1]],
            ),
            aspectmode="manual",
            aspectratio=dict(x=0.9, y=0.5, z=0.4),
            camera=dict(eye=dict(x=0.7, y=0.7, z=0.7)),
        ),
    )


"""
Layout and Figure Creation Functions
"""


def make_cube_fig(
    opacity=0.4, caps=True, colorscheme=D_SCHEME, protein=D_PROTEIN, layer="All"
):
    """Create figure for cube view of proteomics data"""
    df3 = select_layer(layer, cubes_df1)

    X = df3.loc[:, "X Center"]
    Y = df3.loc[:, "Y Center"]
    Z = df3.loc[:, "Z Center"]
    values = df3.loc[:, protein]

    fig1 = go.Figure(
        data=go.Volume(
            x=X,
            y=Y,
            z=Z,
            value=values,
            isomin=math.floor(protein_df.loc[0, protein]),
            isomax=math.ceil(protein_df.loc[1, protein]),
            opacity=opacity,
            surface_count=180,
            slices_z=dict(show=True, locations=[0.4]),
            caps=dict(x_show=caps, y_show=caps, z_show=caps, x_fill=1),
            colorscale=colorscheme,
            name="Cube View",
        )
    )

    set_layout(fig1)
    app_logger.debug("Added cube view to proteomics page")
    return fig1


def make_point_fig(opacity=0.1, colorscheme=D_SCHEME, protein=D_PROTEIN, layer="All"):
    """Create figure for point view of proteomics data"""
    df4 = select_layer(layer, points_df)
    X = df4.loc[:, "X Center"]
    Y = df4.loc[:, "Y Center"]
    Z = df4.loc[:, "Z Center"]
    values = df4.loc[:, protein]

    fig2 = go.Figure(
        data=go.Volume(
            x=X,
            y=Y,
            z=Z,
            value=values,
            isomin=math.floor(protein_df.loc[0, protein]),
            isomax=math.ceil(protein_df.loc[1, protein]),
            opacity=opacity,
            colorscale=colorscheme,
            surface_count=21,
            name="Point View",
        )
    )
    set_layout(fig2)
    app_logger.debug("Added point view to proteomics page")
    return fig2


def make_layer_fig(colorscheme=D_SCHEME, protein=D_PROTEIN, layer=D_LAYER):
    """Create figure for layer view of proteomics data"""
    x = [246, 296, 346, 396, 446, 496, 546, 596, 646]
    y = [274.5, 327.5, 380.5, 433.5, 486.5]

    zlayers = {
        "Layer 1": [[17.5 for i in x] for j in y],
        "Layer 2": [[52.5 for i in x] for j in y],
        "Layer 3": [[87.5 for i in x] for j in y],
        "Layer 4": [[122.5 for i in x] for j in y],
    }

    cmin = math.floor(protein_df.loc[0, protein])
    cmax = math.ceil(protein_df.loc[1, protein])

    data = []

    if layer == "All":
        for k in range(4):
            this_layer = select_layer(LAYERS[k + 1], points_df)
            color_set = get_colors(this_layer, protein)
            if k == 0:
                data.append(
                    go.Surface(
                        x=x,
                        y=y,
                        z=zlayers[LAYERS[k + 1]],
                        colorscale=colorscheme,
                        surfacecolor=color_set,
                        name=LAYERS[k + 1],
                        cmin=cmin,
                        cmax=cmax,
                    ),
                )
            else:
                data.append(
                    go.Surface(
                        x=x,
                        y=y,
                        z=zlayers[LAYERS[k + 1]],
                        colorscale=colorscheme,
                        surfacecolor=color_set,
                        name=LAYERS[k + 1],
                        cmin=cmin,
                        cmax=cmax,
                        showscale=False,
                    ),
                )
    else:
        this_layer = select_layer(layer, points_df)
        color_set = get_colors(this_layer, protein)
        data.append(
            go.Surface(
                x=x,
                y=y,
                z=zlayers[layer],
                colorscale=colorscheme,
                surfacecolor=color_set,
                name=layer,
                cmin=cmin,
                cmax=cmax,
            ),
        )

    fig = go.Figure(data=data)
    set_layout(fig)
    app_logger.debug("Added layer view to proteomics page")
    return fig


def make_sphere_fig(opacity=1, colorscheme=D_SCHEME, protein=D_PROTEIN, layer=D_LAYER):
    """Create figure for sphere view of proteomics data"""
    res = 5
    data = []
    cmin = math.floor(protein_df.loc[0, protein])
    cmax = math.ceil(protein_df.loc[1, protein])

    layer_df = select_layer(layer, points_df)

    scalebar = False
    for k in layer_df.index:
        s_color = layer_df.loc[k, protein]
        if not np.isnan(s_color):
            (X, Y, Z) = make_sphere(
                x=layer_df.loc[k, "X Center"],
                y=layer_df.loc[k, "Y Center"],
                z=layer_df.loc[k, "Z Center"],
                radius=14,
                resolution=res,
            )
            c = [[s_color.item() for i in range(res)] for j in range(res * 2)]
            if not scalebar:
                data.append(
                    go.Surface(
                        x=X,
                        y=Y,
                        z=Z,
                        surfacecolor=c,
                        colorscale=colorscheme,
                        cmin=cmin,
                        cmax=cmax,
                        opacity=opacity,
                        name=f"val:\n{s_color.item()}",
                    )
                )
                scalebar = True
            else:
                data.append(
                    go.Surface(
                        x=X,
                        y=Y,
                        z=Z,
                        surfacecolor=c,
                        colorscale=colorscheme,
                        cmin=cmin,
                        cmax=cmax,
                        showscale=False,
                        opacity=opacity,
                        name=f"val:\n{s_color.item()}",
                    )
                )

    fig4 = go.Figure(data=data)
    set_layout(fig4)
    app_logger.debug("Added sphere view to proteomics page")
    return fig4


def make_opacity_slider(id, opacity):
    return [
        html.P("Adjust the opacity of the model:"),
        dcc.Slider(
            0,
            1,
            0.2,
            value=opacity,
            id=id,
        ),
    ]


"""
Layout Components
"""

filters = dbc.Card(
    dbc.CardBody(
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P("Select a protein:", className="card-text"),
                        dcc.Dropdown(
                            proteins,
                            D_PROTEIN,
                            id="proteinsdd",
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.P("Choose a color scheme:", className="card-text"),
                        dcc.Dropdown(
                            C_SCHEMES,
                            D_SCHEME,
                            id="cschemedd",
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.P("Choose a layer:", className="card-text"),
                        dcc.Dropdown(
                            LAYERS,
                            D_LAYER,
                            id="layersdd",
                        ),
                    ]
                ),
            ],
            justify="center",
        ),
    ),
    color="light",
    class_name="proteomics-filter",
)

proteomics_fig = dbc.Row(
    dbc.Col(
        dcc.Loading(
            dcc.Graph(
                figure=make_cube_fig(),
                className="dcc-graph",
                id="proteomics-graph",
            ),
            style={
                "visibility": "visible",
                "backgroundColor": "transparent",
                "opacity": 0.7,
            },
            type="dot",
            parent_className="loader-wrapper",
        ),
    )
)

tab_content = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Cube View", tab_id="cube-tab"),
                    dbc.Tab(label="Point View", tab_id="point-tab"),
                    dbc.Tab(label="Layer View", tab_id="layer-tab"),
                    dbc.Tab(label="Sphere View", tab_id="sphere-tab"),
                ],
                id="tabs",
                active_tab="cube-tab",
            )
        ),
        dbc.CardBody(
            [
                proteomics_fig,
                html.Div(id="extra-filters"),
            ]
        ),
    ]
)

cube_controls = dbc.Card(
    dbc.CardBody(
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.P("Add or remove end caps:"),
                        dbc.Switch(
                            id="cubecapswitch",
                            value=True,
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    children=make_opacity_slider("cubeslider", 0.4),
                    width=9,
                ),
            ],
        ),
    ),
    color="light",
)

point_controls = dbc.Card(
    dbc.CardBody(
        dbc.Row(
            dbc.Col(
                children=make_opacity_slider("pointslider", 0.1),
                width=12,
            ),
        ),
    ),
    color="light",
)

study_downloads = html.Div(
    children=[
        html.P(
            "Here is the data collected in this study, available as an Excel file or a VTK file."
        ),
        dbc.Button(
            "Download Excel Spreadsheet",
            id="btn-download-xlsx",
            className="download-button",
        ),
        dcc.Download(id="download-xlsx"),
        dbc.Button(
            "Download VTK File",
            id="btn-download-vtk",
            className="download-button",
        ),
        dcc.Download(id="download-vtk"),
    ]
)

ili_downloads = html.Div(
    children=[
        html.P(
            children=[
                "If you would like to visualize this data using the `ili spatial data mapping tool, open the ",
                html.A(
                    "`ili website",
                    href="http://ili.embl.de/",
                ),
                ", select 'Volume', and drag and drop the following two files into the viewer. Then click on the '3D' tab, and choose 'Lego' for Render Mode.",
            ]
        ),
        dbc.Button(
            "Download `ili Spreadsheet",
            id="btn-download-ili-xlsx",
            className="download-button",
        ),
        dcc.Download(id="download-ili-xlsx"),
        dbc.Button(
            "Download `ili Volume File",
            id="btn-download-ili-volume",
            className="download-button",
        ),
        dcc.Download(id="download-ili-volume"),
    ]
)

"""
Layout
"""

layout = html.Div(
    children=[
        html.Section(
            id="cross-section",
            children=[
                html.Header(
                    html.H2(
                        "Spatial Proteome Map of a Single Islet Microenvironment from Pancreas Block P1-20C"
                    )
                ),
                html.P(
                    "These charts show a 3D proteome mapping of a single pancreatic islet microenvironment at 50–µm resolution."
                ),
                filters,
                html.Div(id="current-filters"),
                tab_content,
                dcc.Store(id="protein-store"),
                dcc.Store(id="color-store"),
                dcc.Store(id="cap-store"),
                dcc.Store(id="cube-opacity-store"),
                dcc.Store(id="point-opacity-store"),
                dcc.Store(id="layer-store"),
            ],
        ),
        html.Section(
            id="download-dataset",
            children=[
                html.Header(html.H2("Download Data Here")),
                study_downloads,
                html.Hr(),
                ili_downloads,
                html.Hr(),
            ],
        ),
    ]
)

"""
Callbacks
"""


@callback(
    Output("extra-filters", "children"),
    Input("tabs", "active_tab"),
)
def update_controls(at):
    if at == "cube-tab":
        return cube_controls
    elif at == "point-tab":
        return point_controls


@callback(
    Output("proteomics-graph", "figure"),
    Input("tabs", "active_tab"),
    Input("color-store", "data"),
    Input("protein-store", "data"),
    Input("cap-store", "data"),
    Input("cube-opacity-store", "data"),
    Input("point-opacity-store", "data"),
    Input("layer-store", "data"),
)
def update_fig(tab, color, protein, cap, cubeopacity, pointopacity, layer):
    props = [color, protein, cap, cubeopacity, pointopacity, layer]
    settings = [D_SCHEME, D_PROTEIN, True, 0.4, 0.1, "All"]
    for i in range(6):
        if props[i] is not None:
            settings[i] = props[i]
    if tab == "cube-tab":
        return make_cube_fig(
            colorscheme=settings[0],
            protein=settings[1],
            caps=settings[2],
            opacity=settings[3],
            layer=settings[5],
        )
    elif tab == "point-tab":
        return make_point_fig(
            colorscheme=settings[0],
            protein=settings[1],
            opacity=settings[4],
            layer=settings[5],
        )
    elif tab == "layer-tab":
        return make_layer_fig(
            colorscheme=settings[0], protein=settings[1], layer=settings[5]
        )
    elif tab == "sphere-tab":
        return make_sphere_fig(
            colorscheme=settings[0], protein=settings[1], layer=settings[5]
        )


@callback(Output("protein-store", "data"), Input("proteinsdd", "value"))
def save_protein_filter(value):
    return value


@callback(Output("color-store", "data"), Input("cschemedd", "value"))
def save_color_scheme(value):
    return value


@callback(Output("layer-store", "data"), Input("layersdd", "value"))
def save_layer(value):
    return value


@callback(Output("cap-store", "data"), Input("cubecapswitch", "value"))
def save_cap_setting(value):
    return value


@callback(Output("cube-opacity-store", "data"), Input("cubeslider", "value"))
def save_cube_opacity(value):
    return value


@callback(Output("point-opacity-store", "data"), Input("pointslider", "value"))
def save_point_opacity(value):
    return value


@callback(
    Output("download-xlsx", "data"),
    Input("btn-download-xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def download_xlsx(n_clicks):
    app_logger.debug("Sending assets/HubMAP_TMC_p1_20C_3D_protINT_May8_sorted.xlsx")
    return dcc.send_file("assets/HubMAP_TMC_p1_20C_3D_protINT_May8_sorted.xlsx")


@callback(
    Output("download-vtk", "data"),
    Input("btn-download-vtk", "n_clicks"),
    prevent_initial_call=True,
)
def download_vtk(n_clicks):
    app_logger.debug("Sending assets/HubMAP_TMC_p1_20C_3D_protINT_May8_sorted.vti")
    return dcc.send_file("assets/HubMAP_TMC_p1_20C_3D_protINT_May8_sorted.vti")


@callback(
    Output("download-ili-xlsx", "data"),
    Input("btn-download-ili-xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def download_ili_xlsx(n_clicks):
    app_logger.debug("Sending assets/HuBMAP_ili_data10-11-24.csv")
    return dcc.send_file("assets/HuBMAP_ili_data10-11-24.csv")


@callback(
    Output("download-ili-volume", "data"),
    Input("btn-download-ili-volume", "n_clicks"),
    prevent_initial_call=True,
)
def download_ili_volume(n_clicks):
    app_logger.debug("Sending assets/ili_vol_template.nrrd")
    return dcc.send_file("assets/ili_vol_template.nrrd")
