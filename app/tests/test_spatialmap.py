import pandas as pd
import pytest
import os
import sys

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
import app
from pages.spatialmap import (
    make_defaults,
    make_axes,
    make_layers,
    load_data,
    find_global_value_bounds,
    update_fig,
)

D_PROTEIN = "CYB5A"
D_SCHEME = "jet"
D_OPACITY = 0.4
D_LAYER = "All"

page_info, defaults, layers, cat_opts, value_info, axes, downloads = load_data("P1-20C")
ranges = find_global_value_bounds(value_info)


def test_make_defaults():
    range_data = {
        "CYB5A": [0, 1, True],
        "ALB": [0, 1, False],
    }
    range_df = pd.DataFrame(data=range_data, index=["Min", "Max", "Default"])
    expected = {
        "d_scheme": "haline",
        "d_layer": "All",
        "d_category": "All",
        "d_value": "CYB5A",
    }
    assert make_defaults(range_df) == expected


def test_make_axes():
    measurements = {
        "X Min": [0],
        "X Max": [3],
        "X Size": [1],
        "Y Min": [0],
        "Y Max": [3],
        "Y Size": [1],
        "Z Min": [0],
        "Z Max": [3],
        "Z Size": [1],
    }
    df = pd.DataFrame(data=measurements)
    expected_axes = {"X": [0, 1, 2, 3], "Y": [0, 1, 2, 3], "Z": [0, 1, 2, 3]}
    assert make_axes(df) == expected_axes


def test_make_layers():
    z_axis = [0, 1, 2, 3]
    expected_layers = ["All", "Layer 1", "Layer 2", "Layer 3"]
    assert make_layers(z_axis) == expected_layers


def test_load_data():
    page_info, defaults, layers, cat_opts, value_info, axes, downloads = load_data(
        "P1-20C"
    )
    expected_page_info = {
        "Block": "P1-20C",
        "Title": "Spatial Proteome Map of a Single Islet Microenvironment from Pancreas Block P1-20C",
        "Description": "These charts show a 3D proteome mapping of a single pancreatic islet microenvironment at 50–µm resolution.",
    }
    assert page_info == expected_page_info
    expected_defaults = {
        "d_scheme": "haline",
        "d_layer": "All",
        "d_category": "All",
        "d_value": "CYB5A",
    }
    assert defaults == expected_defaults
    expected_layers = ["All", "Layer 1", "Layer 2", "Layer 3", "Layer 4"]
    assert layers == expected_layers
    expected_cat_opts = {
        "Category": "Islet",
        "Label (Only True)": "Pixels with islet tissue",
        "Label (Only False)": "Pixels without islet tissue",
    }
    assert cat_opts == expected_cat_opts
    expected_value_info = {
        "CYB5A": {"Min": -2.51951, "Max": 0.985942},
        "SOD1": {"Min": -1.4, "Max": 1.46514},
        "CA2": {"Min": -3.22522, "Max": 1.92273},
        "RBP4": {"Min": -2.27831, "Max": 2.67374},
        "ALB": {"Min": -2.86227, "Max": 4.58218},
        "TF": {"Min": -0.93333, "Max": 3.05702},
        "CAT": {"Min": -2.63998, "Max": 2.60333},
    }
    assert value_info == expected_value_info
    expected_axes = {
        "X": [221, 271, 321, 371, 421, 471, 521, 571, 621, 671],
        "Y": [248, 301, 354, 407, 460, 513],
        "Z": [0, 35, 70, 105, 140],
    }
    assert axes == expected_axes
    expected_downloads_data = {
        "Name": [
            "HubMAP_TMC_p1_20C_3D_protINT_May8_sorted.vti",
            "ili_vol_template.nrrd",
        ],
        "Label": ["Download .vti", "Download `ili volume file"],
        "Desc": [
            "Download the data collected in this study as a VTK file",
            "Download a volume for use with the `ili website",
        ],
        "Block": ["P1-20C", "P1-20C"],
    }
    expected_downloads = pd.DataFrame(data=expected_downloads_data)
    assert downloads.equals(expected_downloads)


def test_find_global_value_bounds():
    test_dict = {"A": {"Min": 0, "Max": 0}, "B": {"Min": 0, "Max": 1}}
    expected_bounds = (0, 1)
    assert find_global_value_bounds(test_dict) == expected_bounds


def test_uf_cube_opacity():
    # test that fig1's opacity value is updated as expected
    fig1 = update_fig(
        "cube-tab",
        D_SCHEME,
        D_PROTEIN,
        0.5,
        0.4,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    fig2 = update_fig(
        "cube-tab",
        D_SCHEME,
        D_PROTEIN,
        0,
        0.4,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )

    assert fig1["data"][0]["opacity"] == 0.5
    assert fig2["data"][0]["opacity"] == 0
    with pytest.raises(ValueError):
        update_fig(
            "cube-tab",
            D_SCHEME,
            D_PROTEIN,
            11,
            1,
            "All",
            "All",
            category_data=cat_opts,
            value_ranges=ranges,
            axes=axes,
            block="P1-20C",
        )


def test_uf_cube_cscheme():
    # test that fig1's color scheme value is updated as expected
    fig1 = update_fig(
        "cube-tab",
        "inferno",
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )

    assert fig1["data"][0]["colorscale"] == (
        (0.0, "#000004"),
        (0.1111111111111111, "#1b0c41"),
        (0.2222222222222222, "#4a0c6b"),
        (0.3333333333333333, "#781c6d"),
        (0.4444444444444444, "#a52c60"),
        (0.5555555555555556, "#cf4446"),
        (0.6666666666666666, "#ed6925"),
        (0.7777777777777778, "#fb9b06"),
        (0.8888888888888888, "#f7d13d"),
        (1.0, "#fcffa4"),
    )


def test_uf_cube_layer():
    fig1 = update_fig(
        "cube-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    fig2 = update_fig(
        "cube-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "Layer 2",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    assert fig1["data"][0]["z"].min() == 0.0
    assert fig1["data"][0]["z"].max() == 139.999
    assert fig2["data"][0]["z"].min() == 35.0
    assert fig2["data"][0]["z"].max() == 69.999


def test_uf_cube_islet():
    fig1 = update_fig(
        "cube-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    fig2 = update_fig(
        "cube-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "Pixels with islet tissue",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    fig3 = update_fig(
        "cube-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "Pixels without islet tissue",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    assert len(fig1["data"][0]["z"]) == 1440
    assert len(fig2["data"][0]["z"]) == 728
    assert len(fig3["data"][0]["z"]) == 712


def test_uf_point_opacity():
    # test that fig2's opacity value is updated as expected
    fig1 = update_fig(
        "point-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        0.5,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    fig2 = update_fig(
        "point-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        0,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )

    assert fig1["data"][0]["opacity"] == 0.5
    assert fig2["data"][0]["opacity"] == 0
    with pytest.raises(ValueError):
        update_fig(
            "point-tab",
            D_SCHEME,
            D_PROTEIN,
            D_OPACITY,
            11,
            "All",
            "All",
            category_data=cat_opts,
            value_ranges=ranges,
            axes=axes,
            block="P1-20C",
        )


def test_uf_point_cscheme():
    # test that fig2's color scheme value is updated as expected
    fig1 = update_fig(
        "point-tab",
        "inferno",
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )

    assert fig1["data"][0]["colorscale"] == (
        (0.0, "#000004"),
        (0.1111111111111111, "#1b0c41"),
        (0.2222222222222222, "#4a0c6b"),
        (0.3333333333333333, "#781c6d"),
        (0.4444444444444444, "#a52c60"),
        (0.5555555555555556, "#cf4446"),
        (0.6666666666666666, "#ed6925"),
        (0.7777777777777778, "#fb9b06"),
        (0.8888888888888888, "#f7d13d"),
        (1.0, "#fcffa4"),
    )


def test_uf_point_layer():
    fig1 = update_fig(
        "point-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    fig2 = update_fig(
        "point-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "Layer 3",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    assert fig1["data"][0]["z"].min() == 17.5
    assert fig1["data"][0]["z"].max() == 122.5
    assert fig2["data"][0]["z"].min() == 87.5
    assert fig2["data"][0]["z"].max() == 87.5


def test_uf_layer_cscheme():
    # test that fig3's color scheme value is updated as expected
    fig1 = update_fig(
        "layer-tab",
        "inferno",
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )

    assert fig1["data"][0]["colorscale"] == (
        (0.0, "#000004"),
        (0.1111111111111111, "#1b0c41"),
        (0.2222222222222222, "#4a0c6b"),
        (0.3333333333333333, "#781c6d"),
        (0.4444444444444444, "#a52c60"),
        (0.5555555555555556, "#cf4446"),
        (0.6666666666666666, "#ed6925"),
        (0.7777777777777778, "#fb9b06"),
        (0.8888888888888888, "#f7d13d"),
        (1.0, "#fcffa4"),
    )


def test_uf_layer_layer():
    fig1 = update_fig(
        "layer-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    fig2 = update_fig(
        "layer-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "Layer 2",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    f1l1maxes = []
    f1l1mins = []
    for nlist in fig1["data"][0]["z"]:
        f1l1maxes.append(max(nlist))
        f1l1mins.append(min(nlist))
    f1l4maxes = []
    f1l4mins = []
    for nlist in fig1["data"][3]["z"]:
        f1l4maxes.append(max(nlist))
        f1l4mins.append(min(nlist))
    assert min(f1l1mins) == 17.5
    assert max(f1l1maxes) == 17.5
    assert min(f1l4mins) == 122.5
    assert max(f1l4maxes) == 122.5

    f2l1maxes = []
    f2l1mins = []
    for nlist in fig2["data"][0]["z"]:
        f2l1maxes.append(max(nlist))
        f2l1mins.append(min(nlist))
    assert min(f2l1mins) == 52.5
    assert max(f2l1maxes) == 52.5

    with pytest.raises(IndexError):
        fig2["data"][1]


def test_uf_sphere_cscheme():
    # test that fig4's color scheme value is updated as expected
    fig1 = update_fig(
        "sphere-tab",
        "inferno",
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )

    assert fig1["data"][0]["colorscale"] == (
        (0.0, "#000004"),
        (0.1111111111111111, "#1b0c41"),
        (0.2222222222222222, "#4a0c6b"),
        (0.3333333333333333, "#781c6d"),
        (0.4444444444444444, "#a52c60"),
        (0.5555555555555556, "#cf4446"),
        (0.6666666666666666, "#ed6925"),
        (0.7777777777777778, "#fb9b06"),
        (0.8888888888888888, "#f7d13d"),
        (1.0, "#fcffa4"),
    )


def test_uf_sphere_layer():
    fig1 = update_fig(
        "sphere-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    fig2 = update_fig(
        "sphere-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "Layer 4",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    assert fig1["data"][0]["z"].min() == 3.5
    assert fig1["data"][0]["z"].max() == 31.5
    assert fig2["data"][0]["z"].min() == 108.5
    assert fig2["data"][0]["z"].max() == 136.5


def test_uf_sphere_islet():
    fig1 = update_fig(
        "sphere-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    fig2 = update_fig(
        "sphere-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "Pixels with islet tissue",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )
    fig3 = update_fig(
        "sphere-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "Pixels without islet tissue",
        category_data=cat_opts,
        value_ranges=ranges,
        axes=axes,
        block="P1-20C",
    )

    assert len(fig1["data"]) == 177
    assert len(fig2["data"]) == 91
    assert len(fig3["data"]) == 86


def test_uo_protein():
    # test that max and min values for the specified protein are as expected
    fig1 = update_fig(
        "cube-tab",
        D_SCHEME,
        "ALB",
        D_OPACITY,
        D_OPACITY,
        "All",
        "All",
        category_data=cat_opts,
        value_ranges=(0, 1),
        axes=axes,
        block="P1-20C",
    )

    assert min(fig1["data"][0]["intensity"]) == value_info["ALB"]["Min"]
    assert max(fig1["data"][0]["intensity"]) == value_info["ALB"]["Max"]
