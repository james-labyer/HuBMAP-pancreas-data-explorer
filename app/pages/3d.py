import pandas as pd
from dash import html, dcc, register_page, Output, Input, callback
import dash_bootstrap_components as dbc
import numpy as np
from pywavefront import Wavefront
import plotly.graph_objects as go

register_page(__name__, title="3D Pancreas Model")

blocks = pd.read_csv("assets/block-data.csv")
traces = pd.read_csv("assets/obj/obj-files.csv")


def read_obj(file):
    pancreas = Wavefront(file, collect_faces=True)
    matrix_vertices = np.array(pancreas.vertices)
    faces = np.array(pancreas.mesh_list[0].faces)
    return matrix_vertices, faces


def make_mesh_settings(
    vertices,
    faces,
    color="cyan",
    intensities=None,
    flatshading=False,
    plot_edges=False,
):

    x, y, z = vertices.T
    I, J, K = faces.T

    if intensities is None:
        intensities = z

    mesh = {
        "type": "mesh3d",
        "x": y,
        "y": z,
        "z": x,
        "color": color,
        "flatshading": flatshading,
        "opacity": 0.5,
        "i": I,
        "j": J,
        "k": K,
        "name": "Pancreas",
        "showscale": None,
        "lighting": {
            "ambient": 0.18,
            "diffuse": 1,
            "fresnel": 0.1,
            "specular": 1,
            "roughness": 0.1,
            "facenormalsepsilon": 1e-6,
            "vertexnormalsepsilon": 1e-12,
        },
        "lightposition": {"x": 100, "y": 200, "z": 0},
    }

    if plot_edges is False:
        return [mesh]


def make_mesh_data(name, file, color=None):
    vertices, faces = read_obj(file)
    if color:
        data = make_mesh_settings(vertices, faces, color)
    else:
        data = make_mesh_settings(vertices, faces)
    data[0]["name"] = name
    return data


def make_mesh_fig(pancreas=1):

    pancreas_traces = traces.loc[traces["pancreas"] == pancreas]
    for i in range(pancreas_traces.shape[0]):
        if i == 0:
            data1 = make_mesh_data(
                pancreas_traces.at[i, "name"],
                pancreas_traces.at[i, "file"],
                pancreas_traces.at[i, "color"],
            )
            fig = go.Figure(data1)
        else:
            data = make_mesh_data(
                pancreas_traces.at[i, "name"],
                pancreas_traces.at[i, "file"],
                pancreas_traces.at[i, "color"],
            )
            fig.add_trace(go.Mesh3d(data[0]))

    return fig


def make_graph_layout(pancreas=1):
    container = dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H2(f"3D Model of Pancreas {pancreas}"),
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(
                                id="pancreas-graph",
                                figure=make_mesh_fig(pancreas),
                                config={"scrollZoom": False},
                                className="centered-graph",
                            )
                        ],
                        width=10,
                    ),
                    dbc.Col(
                        dbc.Card(
                            id="click-data",
                            color="light",
                            class_name="block-card",
                        ),
                        width=2,
                    ),
                ],
                className="g-2",
            ),
        ],
        fluid=True,
        class_name="model-page",
    )
    return container


layout = html.Div([make_graph_layout(1)])


@callback(Output("click-data", "children"), [Input("pancreas-graph", "clickData")])
def display_click_data(click_data):
    if click_data and click_data["points"][0]["curveNumber"] > 3:
        row = blocks.loc[
            blocks["Block ID"]
            == traces.loc[click_data["points"][0]["curveNumber"], "name"]
        ]
        item_data = [
            {"label": "Block ", "value": row.iloc[0]["Block ID"]},
            {"label": "Anatomical region: ", "value": row.iloc[0]["Anatomical region"]},
            {
                "label": "View optical clearing data",
                "value": row.iloc[0]["Optical clearing"],
            },
            {"label": "View GeoMX data", "value": row.iloc[0]["GeoMX"]},
            {"label": "View proteomics data", "value": row.iloc[0]["Proteomics"]},
        ]
        card_content = []
        card_body_content = []
        for i in range(5):
            label_str = str(item_data[i]["label"])
            value_str = str(item_data[i]["value"])
            if i == 0:
                card_content.append(
                    dbc.CardHeader(label_str + value_str, class_name="card-title")
                )
            elif i == 1:
                child = html.P(label_str + value_str)
                card_body_content.append(child)
            elif item_data[i]["value"] == " ":
                continue
            else:
                value_str = item_data[i]["value"]
                child = html.P([dcc.Link(label_str, href=f"{value_str}")])
                card_body_content.append(child)
        card_content.append(dbc.CardBody(card_body_content))
        return card_content
    else:
        card_content = [
            dbc.CardHeader("Block Data"),
            dbc.CardBody(
                [
                    html.P("Click on a block to view available datasets"),
                ],
            ),
        ]
        return card_content
