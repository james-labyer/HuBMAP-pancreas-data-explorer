import pandas as pd
from dash import html, dcc, register_page, Output, Input, callback
import dash_bootstrap_components as dbc
import numpy as np
from pywavefront import Wavefront
import plotly.graph_objects as go
import logging

register_page(__name__, path="/3d", title="3D Pancreas Model")
app_logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
app_logger.handlers = gunicorn_logger.handlers
app_logger.setLevel(gunicorn_logger.level)

blocks = pd.read_csv("assets/block-data.csv")
traces = pd.read_csv("assets/obj/obj-files.csv")


def read_obj(file):
    pancreas = Wavefront(file, collect_faces=True)
    matrix_vertices = np.array(pancreas.vertices)
    faces = np.array(pancreas.mesh_list[0].faces)
    app_logger.debug(
        f"Read {file} and found vertices ndarray of shape {matrix_vertices.shape} and faces ndarray of shape {faces.shape}"
    )
    return matrix_vertices, faces


def make_mesh_settings(
    vertices,
    faces,
    color="cyan",
    opacity=1,
):
    x, y, z = vertices.T
    L, M, N = faces.T

    mesh = {
        "type": "mesh3d",
        "x": y,
        "y": z,
        "z": x,
        # "x": x,
        # "y": y,
        # "z": z,
        "color": color,
        "flatshading": False,
        "opacity": opacity,
        "i": L,
        "j": M,
        "k": N,
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

    return [mesh]


def make_mesh_data(name, file, color=None, opacity=1):
    vertices, faces = read_obj(file)
    data = make_mesh_settings(vertices, faces, color=color, opacity=opacity)
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
                pancreas_traces.at[i, "opacity"],
            )
            fig = go.Figure(data1)
            name = data1[0]["name"]
            app_logger.info(
                f"Added trace for {name} to 3D Model of Pancreas {pancreas}"
            )
        else:
            data = make_mesh_data(
                pancreas_traces.at[i, "name"],
                pancreas_traces.at[i, "file"],
                pancreas_traces.at[i, "color"],
                pancreas_traces.at[i, "opacity"],
            )
            fig.add_trace(go.Mesh3d(data[0]))
            name = data[0]["name"]
            app_logger.info(
                f"Added trace for {name} to 3D Model of Pancreas {pancreas}"
            )
    fig.update_layout(
        height=500,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    return fig


def make_graph_layout(pancreas=1):
    container = html.Section(
        [
            dbc.Row(dbc.Col(html.Header(html.H2(f"3D Model of Pancreas {pancreas}")))),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                dcc.Graph(
                                    id="pancreas-graph",
                                    figure=make_mesh_fig(pancreas),
                                    config={"scrollZoom": False},
                                    className="centered-graph",
                                )
                            )
                        ],
                        width=9,
                    ),
                    dbc.Col(
                        dbc.Card(
                            id="click-data",
                            color="light",
                            class_name="block-card",
                        ),
                        width=3,
                    ),
                ],
                className="g-3",
            ),
        ],
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
        block_name = row.iloc[0]["Block ID"]
        app_logger.info(f"Displaying click data for {block_name}")
        item_data = [
            {"label": "Block ", "value": row.iloc[0]["Block ID"]},
            {"label": "Anatomical region: ", "value": row.iloc[0]["Anatomical region"]},
            {
                "label": "View optical clearing data",
                "value": row.iloc[0]["Optical clearing"],
            },
            {"label": "View GeoMx data", "value": row.iloc[0]["GeoMx"]},
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
        content = "Click on a block to view available datasets"
        card_content = [
            dbc.CardHeader("Block Data"),
            dbc.CardBody(
                [
                    html.P(content),
                ],
            ),
        ]
        return card_content
