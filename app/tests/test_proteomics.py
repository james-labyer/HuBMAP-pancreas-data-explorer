import pandas as pd
import pytest
import os
import sys

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
import app
from pages.proteomics import update_fig

D_PROTEIN = "INS"
D_SCHEME = "jet"
D_OPACITY = 0.4
D_LAYER = "All"

protein_df = pd.read_csv("assets/protein_labels.csv")


def test_uf_cube_opacity():
    # test that fig1's opacity value is updated as expected
    fig1 = update_fig("cube-tab", D_SCHEME, D_PROTEIN, 0.5, 0.4, "All", "All")
    fig2 = update_fig("cube-tab", D_SCHEME, D_PROTEIN, 0, 0.4, "All", "All")

    assert fig1["data"][0]["opacity"] == 0.5
    assert fig2["data"][0]["opacity"] == 0
    with pytest.raises(ValueError):
        update_fig("cube-tab", D_SCHEME, D_PROTEIN, 11, 1, "All", "All")


def test_uf_cube_cscheme():
    # test that fig1's color scheme value is updated as expected
    fig1 = update_fig(
        "cube-tab", "inferno", D_PROTEIN, D_OPACITY, D_OPACITY, "All", "All"
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
        "cube-tab", D_SCHEME, D_PROTEIN, D_OPACITY, D_OPACITY, "All", "All"
    )
    fig2 = update_fig(
        "cube-tab", D_SCHEME, D_PROTEIN, D_OPACITY, D_OPACITY, "Layer 2", "All"
    )
    assert fig1["data"][0]["z"].min() == 0.0
    assert fig1["data"][0]["z"].max() == 139.999
    assert fig2["data"][0]["z"].min() == 35.0
    assert fig2["data"][0]["z"].max() == 69.999


def test_uf_cube_islet():
    fig1 = update_fig(
        "cube-tab", D_SCHEME, D_PROTEIN, D_OPACITY, D_OPACITY, "All", "All"
    )
    fig2 = update_fig(
        "cube-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "Pixels with islet tissue",
    )
    fig3 = update_fig(
        "cube-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "Pixels without islet tissue",
    )
    assert len(fig1["data"][0]["z"]) == 1440
    assert len(fig2["data"][0]["z"]) == 728
    assert len(fig3["data"][0]["z"]) == 712


def test_uf_point_opacity():
    # test that fig2's opacity value is updated as expected
    fig1 = update_fig("point-tab", D_SCHEME, D_PROTEIN, D_OPACITY, 0.5, "All", "All")
    fig2 = update_fig("point-tab", D_SCHEME, D_PROTEIN, D_OPACITY, 0, "All", "All")

    assert fig1["data"][0]["opacity"] == 0.5
    assert fig2["data"][0]["opacity"] == 0
    with pytest.raises(ValueError):
        update_fig("point-tab", D_SCHEME, D_PROTEIN, D_OPACITY, 11, "All", "All")


def test_uf_point_cscheme():
    # test that fig2's color scheme value is updated as expected
    fig1 = update_fig(
        "point-tab", "inferno", D_PROTEIN, D_OPACITY, D_OPACITY, "All", "All"
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
        "point-tab", D_SCHEME, D_PROTEIN, D_OPACITY, D_OPACITY, "All", "All"
    )
    fig2 = update_fig(
        "point-tab", D_SCHEME, D_PROTEIN, D_OPACITY, D_OPACITY, "Layer 3", "All"
    )
    assert fig1["data"][0]["z"].min() == 17.5
    assert fig1["data"][0]["z"].max() == 122.5
    assert fig2["data"][0]["z"].min() == 87.5
    assert fig2["data"][0]["z"].max() == 87.5


def test_uf_layer_cscheme():
    # test that fig3's color scheme value is updated as expected
    fig1 = update_fig(
        "layer-tab", "inferno", D_PROTEIN, D_OPACITY, D_OPACITY, "All", "All"
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
        "layer-tab", D_SCHEME, D_PROTEIN, D_OPACITY, D_OPACITY, "All", "All"
    )
    fig2 = update_fig(
        "layer-tab", D_SCHEME, D_PROTEIN, D_OPACITY, D_OPACITY, "Layer 2", "All"
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
        "sphere-tab", "inferno", D_PROTEIN, D_OPACITY, D_OPACITY, "All", "All"
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
        "sphere-tab", D_SCHEME, D_PROTEIN, D_OPACITY, D_OPACITY, "All", "All"
    )
    fig2 = update_fig(
        "sphere-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "Layer 4",
        "All",
    )
    assert fig1["data"][0]["z"].min() == 3.5
    assert fig1["data"][0]["z"].max() == 31.5
    assert fig2["data"][0]["z"].min() == 108.5
    assert fig2["data"][0]["z"].max() == 136.5


def test_uf_sphere_islet():
    fig1 = update_fig(
        "sphere-tab", D_SCHEME, D_PROTEIN, D_OPACITY, D_OPACITY, "All", "All"
    )
    fig2 = update_fig(
        "sphere-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "Pixels with islet tissue",
    )
    fig3 = update_fig(
        "sphere-tab",
        D_SCHEME,
        D_PROTEIN,
        D_OPACITY,
        D_OPACITY,
        "All",
        "Pixels without islet tissue",
    )

    assert len(fig1["data"]) == 169
    assert len(fig2["data"]) == 91
    assert len(fig3["data"]) == 78


def test_uo_protein():
    # test that max and min values for the specified protein are as expected
    fig1 = update_fig("cube-tab", D_SCHEME, "GCG", D_OPACITY, D_OPACITY, "All", "All")

    assert min(fig1["data"][0]["intensity"]) == protein_df.loc[0, "GCG"]
    assert max(fig1["data"][0]["intensity"]) == protein_df.loc[1, "GCG"]
