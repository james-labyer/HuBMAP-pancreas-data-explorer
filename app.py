import pandas as pd
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import math
from dash_slicer import VolumeSlicer
from bioio import BioImage
import bioio_czi

app = Dash(
    __name__,
    title="Islet Proteome Map",
    external_stylesheets=[dbc.themes.LUMEN],
)

server = app.server
LAYERS = ["All", "Layer 1", "Layer 2", "Layer 3", "Layer 4"]
X_AXIS = [221, 271, 321, 371, 421, 471, 521, 571, 621, 671]
Y_AXIS = [248, 301, 354, 407, 460, 513]
Z_AXIS = [0, 35, 70, 105, 140]
D_PROTEIN = "INS"
D_SCHEME = "jet"
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
slices_img = BioImage(
    "assets/P2-13A INS 488 tile 25um stack.czi", reader=bioio_czi.Reader
)


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


def make_fig1(
    opacity=0.4, caps=True, colorscheme=D_SCHEME, protein=D_PROTEIN, layer="All"
):
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
        )
    )

    fig1.update_layout(
        scene=dict(
            xaxis=dict(tickvals=X_AXIS),
            yaxis=dict(tickvals=Y_AXIS),
            zaxis=dict(tickvals=Z_AXIS),
        )
    )
    return fig1


def make_fig2(opacity=0.1, colorscheme=D_SCHEME, protein=D_PROTEIN, layer="All"):
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
        )
    )
    return fig2


def make_fig3(cscheme=D_SCHEME, protein=D_PROTEIN):
    x = X_AXIS[:9]
    y = Y_AXIS[:5]
    z1 = [[35 for i in x] for j in y]
    z2 = [[70 for i in x] for j in y]
    z3 = [[105 for i in x] for j in y]
    z4 = [[140 for i in x] for j in y]

    color_sets = []

    for k in range(4):
        this_layer = select_layer(LAYERS[k], points_df)
        color_sets.append(get_colors(this_layer, protein))

    fig = go.Figure(
        data=[
            go.Surface(x=x, y=y, z=z1, colorscale=cscheme, surfacecolor=color_sets[0]),
            go.Surface(
                x=x,
                y=y,
                z=z2,
                showscale=False,
                colorscale=cscheme,
                surfacecolor=color_sets[1],
            ),
            go.Surface(
                x=x,
                y=y,
                z=z3,
                showscale=False,
                colorscale=cscheme,
                surfacecolor=color_sets[2],
            ),
            go.Surface(
                x=x,
                y=y,
                z=z4,
                showscale=False,
                colorscale=cscheme,
                surfacecolor=color_sets[3],
            ),
        ]
    )

    return fig


def make_fig4(opacity=1, cscheme=D_SCHEME, protein=D_PROTEIN):
    res = 5
    data = []
    cmin = math.floor(protein_df.loc[0, protein])
    cmax = math.ceil(protein_df.loc[1, protein])
    for k in points_df.index:
        s_color = points_df.loc[k, protein]
        if not np.isnan(s_color):
            (X, Y, Z) = make_sphere(
                x=points_df.loc[k, "X Center"],
                y=points_df.loc[k, "Y Center"],
                z=points_df.loc[k, "Z Center"],
                radius=16,
                resolution=res,
            )
            c = [[s_color.item() for i in range(res)] for j in range(res * 2)]
            if k == 1:
                data.append(
                    go.Surface(
                        x=X,
                        y=Y,
                        z=Z,
                        surfacecolor=c,
                        colorscale=cscheme,
                        cmin=cmin,
                        cmax=cmax,
                        opacity=opacity,
                    )
                )
            else:
                data.append(
                    go.Surface(
                        x=X,
                        y=Y,
                        z=Z,
                        surfacecolor=c,
                        colorscale=cscheme,
                        cmin=cmin,
                        cmax=cmax,
                        showscale=False,
                        opacity=opacity,
                    )
                )

    fig4 = go.Figure(data=data)
    return fig4


def make_fig5():
    vol = slices_img.data[0][0]
    slicer = VolumeSlicer(app, vol)
    slicer.graph.config["scrollZoom"] = False
    return [slicer.graph, slicer.slider, *slicer.stores]


def make_c_scheme_dd(id):
    return [
        html.P("Choose a color scheme:"),
        dcc.Dropdown(
            C_SCHEMES,
            D_SCHEME,
            id=id,
        ),
    ]


def make_opacity_slider(id, default=0.4):
    return [
        html.P("Adjust the opacity of the model:"),
        dcc.Slider(
            0,
            1,
            0.2,
            value=default,
            id=id,
        ),
    ]


app.layout = html.Div(
    children=[
        html.Header(
            children=[
                html.Div(
                    id="navbar",
                    children=[
                        dbc.Navbar(
                            dbc.Stack(
                                [
                                    dbc.Row(
                                        dbc.Col(
                                            html.Div(
                                                html.H1(
                                                    "Spatial Proteome Map of a Single Human Islet Microenvironment",
                                                    className="bg-primary text-light title w-100",
                                                ),
                                            ),
                                            width=12,
                                        )
                                    ),
                                    dbc.Row(
                                        dbc.Col(
                                            [
                                                dbc.Nav(
                                                    [
                                                        dbc.NavLink(
                                                            "Proteome Cross-Section",
                                                            href="#cross-section",
                                                            external_link=True,
                                                            className="nav-link text-light sub-nav",
                                                        ),
                                                        dbc.NavLink(
                                                            "3D Pancreas Viewer",
                                                            href="#3d-view",
                                                            external_link=True,
                                                            className="nav-link text-light",
                                                        ),
                                                        dbc.NavLink(
                                                            "Download Data",
                                                            href="#download-dataset",
                                                            external_link=True,
                                                            className="nav-link text-light",
                                                        ),
                                                    ],
                                                    navbar=True,
                                                    class_name="bg-primary",
                                                ),
                                            ],
                                        )
                                    ),
                                ]
                            ),
                            color="primary",
                            sticky="top",
                        ),
                    ],
                ),
            ]
        ),
        html.Main(
            id="main-content",
            children=[
                dbc.Container(
                    id="content-div",
                    children=[
                        html.Section(
                            id="cross-section",
                            children=[
                                html.Header(html.H2("Proteome Cross-Section View")),
                                html.P(
                                    "The following four charts show a 3D proteome mapping of single pancreatic islet microenvironment at 50–µm resolution."
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.P("Select a protein:"),
                                                        dcc.Dropdown(
                                                            proteins,
                                                            D_PROTEIN,
                                                            id="proteinsdd",
                                                        ),
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.P(
                                                            "Select a tissue layer:"
                                                        ),
                                                        dcc.Dropdown(
                                                            LAYERS,
                                                            "All",
                                                            id="layersdd",
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            justify="center",
                                        ),
                                    ),
                                    color="light",
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        dcc.Graph(
                                            figure=make_fig1(),
                                            className="dcc-graph",
                                            id="cross-section-graph",
                                        ),
                                    )
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        dbc.Row(
                                            children=[
                                                dbc.Col(
                                                    children=[
                                                        html.P(
                                                            "Add or remove end caps:"
                                                        ),
                                                        dbc.Switch(
                                                            id="fig1capswitch",
                                                            value=False,
                                                        ),
                                                    ],
                                                    width=3,
                                                ),
                                                dbc.Col(
                                                    children=make_c_scheme_dd(
                                                        "fig1colorschemedd"
                                                    ),
                                                    width=3,
                                                ),
                                                dbc.Col(
                                                    children=make_opacity_slider(
                                                        "fig1opacityslider"
                                                    ),
                                                    width=6,
                                                ),
                                            ],
                                        ),
                                    ),
                                    color="light",
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        dcc.Graph(
                                            figure=make_fig2(),
                                            className="dcc-graph",
                                            id="cross-section-graph2",
                                        ),
                                    )
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        dbc.Row(
                                            children=[
                                                dbc.Col(
                                                    children=make_c_scheme_dd(
                                                        "fig2colorschemedd"
                                                    )
                                                ),
                                                dbc.Col(
                                                    children=make_opacity_slider(
                                                        "fig2opacityslider"
                                                    )
                                                ),
                                            ],
                                        ),
                                    ),
                                    color="light",
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        dcc.Graph(
                                            figure=make_fig3(),
                                            className="dcc-graph",
                                            id="cross-section-graph3",
                                        ),
                                    )
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        dbc.Row(
                                            dbc.Col(
                                                children=make_c_scheme_dd(
                                                    "fig3colorschemedd"
                                                )
                                            )
                                        ),
                                    ),
                                    color="light",
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        dcc.Graph(
                                            figure=make_fig4(),
                                            className="dcc-graph",
                                            id="cross-section-graph4",
                                        ),
                                    )
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        dbc.Row(
                                            children=[
                                                dbc.Col(
                                                    children=make_c_scheme_dd(
                                                        "fig4colorschemedd"
                                                    )
                                                ),
                                                dbc.Col(
                                                    children=make_opacity_slider(
                                                        "fig4opacityslider", 1
                                                    )
                                                ),
                                            ],
                                        ),
                                    ),
                                    color="light",
                                ),
                            ],
                        ),
                        html.Section(
                            id="slice-view",
                            children=[
                                html.Header(html.H2("3D Pancreas View")),
                                dbc.Row(dbc.Col(make_fig5())),
                            ],
                        ),
                        html.Section(
                            id="download-dataset",
                            children=[
                                html.Header(html.H2("Download Data Here")),
                                html.Div(
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
                                ),
                                html.Hr(),
                                html.Div(
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
                                ),
                                html.Hr(),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Footer("Copyright 2024, Texas Advanced Computing Center"),
    ]
)


@callback(
    Output("cross-section-graph", "figure"),
    Output("cross-section-graph2", "figure"),
    Output("cross-section-graph3", "figure"),
    Output("cross-section-graph4", "figure"),
    Input("fig1opacityslider", "value"),
    Input("fig1capswitch", "value"),
    Input("fig1colorschemedd", "value"),
    Input("fig2opacityslider", "value"),
    Input("fig2colorschemedd", "value"),
    Input("fig3colorschemedd", "value"),
    Input("fig4opacityslider", "value"),
    Input("fig4colorschemedd", "value"),
    Input("proteinsdd", "value"),
    Input("layersdd", "value"),
)
def update_output(
    fig1opacityslider,
    fig1capswitch,
    fig1colorschemedd,
    fig2opacityslider,
    fig2colorschemedd,
    fig3colorschemedd,
    fig4opacityslider,
    fig4colorschemedd,
    proteinsdd,
    layersdd,
):
    fig1 = make_fig1(
        fig1opacityslider, fig1capswitch, fig1colorschemedd, proteinsdd, layersdd
    )
    fig2 = make_fig2(fig2opacityslider, fig2colorschemedd, proteinsdd, layersdd)
    fig3 = make_fig3(fig3colorschemedd, protein=proteinsdd)
    fig4 = make_fig4(fig4opacityslider, fig4colorschemedd, proteinsdd)
    return fig1, fig2, fig3, fig4


@callback(
    Output("download-xlsx", "data"),
    Input("btn-download-xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def download_xlsx(n_clicks):
    return dcc.send_file("assets/HubMAP_TMC_p1_20C_3D_protINT_May8_sorted.xlsx")


@callback(
    Output("download-ili-xlsx", "data"),
    Input("btn-download-ili-xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def download_ili_xlsx(n_clicks):
    return dcc.send_file("assets/HuBMAP_ili_data10-11-24.csv")


@callback(
    Output("download-ili-volume", "data"),
    Input("btn-download-ili-volume", "n_clicks"),
    prevent_initial_call=True,
)
def download_ili_volume(n_clicks):
    return dcc.send_file("assets/ili_vol_template.nrrd")


if __name__ == "__main__":
    app.run_server(
        host="0.0.0.0",
        port="8050",
        dev_tools_props_check=False,
    )
