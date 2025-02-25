import json

import dash_bootstrap_components as dbc
import plotly
import pytest
from dash import dcc, html

import app
from pages.model3d import (
    display_click_data,
    make_mesh_data,
    make_mesh_fig,
    make_mesh_settings,
    read_obj,
)


def test_read_obj():
    vertices, faces = read_obj("./assets/obj/P1_Pancreas_Head_4A.obj")
    assert vertices.shape == (8, 3)
    assert faces.shape == (12, 3)

    vertices, faces = read_obj("./assets/obj/head_invert.obj")
    assert vertices.shape == (269694, 3)
    assert faces.shape == (535314, 3)

    with pytest.raises(IndexError):
        vertices, faces = read_obj("./assets/obj/obj-files.csv")


def test_make_mesh_settings():
    vertices, faces = read_obj("./assets/obj/P1_Pancreas_Head_4A.obj")
    settings1 = make_mesh_settings(
        vertices,
        faces,
        "Pancreas 1",
        color="cyan",
        opacity=1,
    )

    assert settings1[0]["color"] == "cyan"
    assert settings1[0]["opacity"] == 1

    vertices, faces = read_obj("./assets/obj/P1_Pancreas_Head_4A.obj")
    settings2 = make_mesh_settings(
        vertices,
        faces,
        "Pancreas 1",
        color="#ED780B",
        opacity=0.5,
    )

    assert settings2[0]["color"] == "#ED780B"
    assert settings2[0]["opacity"] == 0.5


def test_make_mesh_data():
    test1 = make_mesh_data("Head", "./assets/obj/head_invert.obj")
    assert test1[0]["name"] == "Head"

    test2 = make_mesh_data("Tail", "./assets/obj/tail_invert.obj")
    assert test2[0]["name"] == "Tail"


def test_make_mesh_fig():
    fig1 = make_mesh_fig(1)
    assert len(fig1["data"]) == 12
    assert fig1["layout"]["height"] == 500


def test_display_click_data():
    click1 = {
        "points": [
            {
                "x": -392,
                "y": 1749.50244140625,
                "z": 746,
                "curveNumber": 3,
                "pointNumber": 52662,
                "i": 28916,
                "j": 28769,
                "k": 28768,
                "bbox": {
                    "x0": 539.0667184592023,
                    "x1": 539.0667184592023,
                    "y0": 401.4491349814796,
                    "y1": 401.4491349814796,
                },
            }
        ]
    }
    layout1 = json.loads(
        json.dumps(display_click_data(click1), cls=plotly.utils.PlotlyJSONEncoder)
    )
    testlayout1 = [
        dbc.CardHeader("Block Data"),
        dbc.CardBody(
            [
                html.P("Click on a block to view available datasets"),
            ],
        ),
    ]
    test1 = json.loads(json.dumps(testlayout1, cls=plotly.utils.PlotlyJSONEncoder))
    assert layout1 == test1

    # click2 = {
    #     "points": [
    #         {
    #             "x": -392,
    #             "y": 1749.50244140625,
    #             "z": 746,
    #             "curveNumber": 4,
    #             "pointNumber": 52662,
    #             "i": 28916,
    #             "j": 28769,
    #             "k": 28768,
    #             "bbox": {
    #                 "x0": 539.0667184592023,
    #                 "x1": 539.0667184592023,
    #                 "y0": 401.4491349814796,
    #                 "y1": 401.4491349814796,
    #             },
    #         }
    #     ]
    # }
    # layout2 = json.loads(
    #     json.dumps(display_click_data(click2), cls=plotly.utils.PlotlyJSONEncoder)
    # )
    # testlayout2 = [
    #     dbc.CardHeader("Block P1-4A", class_name="card-title"),
    #     dbc.CardBody(
    #         [
    #             html.P("Anatomical region: Pancreatic head"),
    #             html.P(
    #                 [
    #                     dcc.Link(
    #                         "View scientific images",
    #                         href="/optical-clearing-files/P1-4A",
    #                     )
    #                 ]
    #             ),
    #             html.P([dcc.Link("View reports", href="/geomx/P1")]),
    #         ]
    #     ),
    # ]
    # test2 = json.loads(json.dumps(testlayout2, cls=plotly.utils.PlotlyJSONEncoder))
    # assert layout2 == test2
