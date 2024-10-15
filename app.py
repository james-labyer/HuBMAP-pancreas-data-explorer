import pandas as pd
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

app = Dash(external_stylesheets=[dbc.themes.LUMEN])

df = pd.read_csv("assets/rectangles_output.csv")


X = df.loc[:, "X Center"]
Y = df.loc[:, "Y Center"]
Z = df.loc[:, "Z Center"]
values = df.loc[:, "CYB5A"]

fig1 = go.Figure(
    data=go.Volume(
        x=X,
        y=Y,
        z=Z,
        value=values,
        isomin=-10,
        isomax=10,
        opacity=0.5,
        surface_count=180,
        slices_z=dict(show=True, locations=[0.4]),
        caps=dict(x_show=True, y_show=True, z_show=True, x_fill=1),
        colorscale="Jet",
    )
)

fig1.update_layout(
    scene=dict(
        xaxis=dict(tickvals=[221, 271, 321, 421, 471, 521, 571, 621, 671]),
        yaxis=dict(tickvals=[248, 301, 354, 407, 460, 513]),
        zaxis=dict(tickvals=[0, 35, 70, 105, 140]),
    )
)

df2 = pd.read_csv("assets/protein_labels.csv")
proteins = df2.columns.tolist()

app.layout = html.Div(
    children=[
        html.Header(
            children=[
                html.H1("Spatial Proteome Map of a Single Human Islet Microenvironment")
            ]
        ),
        html.Main(
            id="main-content",
            children=[
                html.Div(
                    id="navbar",
                    children=[
                        dbc.Nav(
                            [
                                dbc.NavLink(
                                    "Proteome Cross-Section View",
                                    href="#cross-section",
                                    external_link=True,
                                ),
                                dbc.NavLink(
                                    "Proteomics Scatter Plot",
                                    href="#scatter-plot",
                                    external_link=True,
                                ),
                                dbc.NavLink(
                                    "Download Data",
                                    href="#download-dataset",
                                    external_link=True,
                                ),
                            ],
                            vertical=True,
                        )
                    ],
                ),
                html.Div(
                    id="content-div",
                    children=[
                        html.Section(
                            id="cross-section",
                            children=[
                                html.Header(html.H2("Proteome Cross-Section View")),
                                html.P(
                                    "Here is a 3D cross-section of the tissue. Select a protein to view its concentrations throughout the tissue sample:"
                                ),
                                dcc.Dropdown(
                                    proteins,
                                    "CYB5A",
                                    id="proteinsdd",
                                ),
                                html.P("Select a tissue layer to view"),
                                dcc.Dropdown(
                                    ["All", "Layer 1", "Layer 2", "Layer 3", "Layer 4"],
                                    "All",
                                    id="layersdd",
                                ),
                                dcc.Graph(
                                    figure=fig1,
                                    className="dcc-graph",
                                    id="cross-section-graph",
                                ),
                                html.Div(
                                    children=[
                                        html.Div(
                                            id="caps-and-color-div",
                                            children=[
                                                html.Div(
                                                    children=[
                                                        html.P(
                                                            "Add or remove end caps:"
                                                        ),
                                                        dbc.Switch(
                                                            id="capswitch", value=False
                                                        ),
                                                    ],
                                                    id="caps-div",
                                                ),
                                                html.Div(
                                                    children=[
                                                        html.P(
                                                            "Choose a color scheme:"
                                                        ),
                                                        dcc.Dropdown(
                                                            [
                                                                "YlGnBu",
                                                                "Bluered",
                                                                "Blues",
                                                                "Greens",
                                                                "Greys",
                                                                "Jet",
                                                                "Reds",
                                                                "Viridis",
                                                                "YlOrRd",
                                                            ],
                                                            "Jet",
                                                            id="colorschemedd",
                                                        ),
                                                    ],
                                                    id="color-scheme-div",
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            children=[
                                                html.P(
                                                    "Adjust the opacity of the model:"
                                                ),
                                                dcc.Slider(
                                                    0,
                                                    1,
                                                    0.2,
                                                    value=0.4,
                                                    id="opacityslider",
                                                ),
                                            ],
                                            id="opacity-div",
                                        ),
                                    ],
                                    id="cross-section-controls",
                                ),
                            ],
                        ),
                        html.Section(
                            id="scatter-plot",
                            children=[
                                html.Header(html.H2("Proteomics Scatter Plot")),
                                html.P("Explanation text"),
                                html.Div(
                                    "Visualization placeholder",
                                    className="viz-placeholder",
                                ),
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
                                                ", select 'Volume', and drag and drop the following two files into the viewer:",
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Footer("This site made possible by the Texas Advanced Computing Center."),
    ]
)


def select_layer(zlayer):
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


@callback(
    Output("cross-section-graph", "figure"),
    Input("opacityslider", "value"),
    Input("capswitch", "value"),
    Input("colorschemedd", "value"),
    Input("proteinsdd", "value"),
    Input("layersdd", "value"),
)
def update_output(opacityslider, capswitch, colorschemedd, proteinsdd, layersdd):
    df1 = select_layer(layersdd)
    # print(df[(df["Z Center"] >= 35) & (df["Z Center"] < 70)].loc[:, "X Center"])
    fig1 = go.Figure(
        data=go.Volume(
            x=df1.loc[:, "X Center"],
            y=df1.loc[:, "Y Center"],
            z=df1.loc[:, "Z Center"],
            value=df1.loc[:, proteinsdd],
            isomin=-10,
            isomax=10,
            opacity=opacityslider,
            surface_count=180,
            slices_z=dict(show=True, locations=[0.4]),
            caps=dict(x_show=capswitch, y_show=capswitch, z_show=capswitch, x_fill=1),
            colorscale=colorschemedd,
        )
    )
    fig1.update_layout(
        scene=dict(
            xaxis=dict(tickvals=[221, 271, 321, 371, 421, 471, 521, 571, 621, 671]),
            yaxis=dict(tickvals=[248, 301, 354, 407, 460, 513]),
            zaxis=dict(tickvals=[0, 35, 70, 105, 140]),
        )
    )
    return fig1


@callback(
    Output("download-xlsx", "data"),
    Input("btn-download-xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def download_xlsx(n_clicks):
    return dcc.send_file("assets/HubMAP_TMC_p1_20C_3D_protINT_May8_sorted.xlsx")


@callback(
    Output("download-vtk", "data"),
    Input("btn-download-vtk", "n_clicks"),
    prevent_initial_call=True,
)
def download_vtk(n_clicks):
    return dcc.send_file("assets/HubMAP_TMC_p1_20C_3D_protINT_May8_sorted.vti")


if __name__ == "__main__":
    app.run_server(debug=True)
