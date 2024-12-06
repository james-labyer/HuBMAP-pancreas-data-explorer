import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.append(str(Path(__file__).parent.parent.parent))
import app.app
from app.pages.proteomics import update_fig

D_PROTEIN = "INS"
D_SCHEME = "jet"
D_OPACITY = 0.4
D_LAYER = "All"
D_CAPS = False

protein_df = pd.read_csv("assets/protein_labels.csv")


def test_uf_cube_opacity():
    # test that fig1's opacity value is updated as expected
    fig1 = update_fig("cube-tab", D_SCHEME, D_PROTEIN, D_CAPS, 0.5, 0.4)
    fig2 = update_fig("cube-tab", D_SCHEME, D_PROTEIN, D_CAPS, 0, 0.4)

    assert fig1["data"][0]["opacity"] == 0.5
    assert fig2["data"][0]["opacity"] == 0
    with pytest.raises(ValueError):
        update_fig("cube-tab", D_SCHEME, D_PROTEIN, D_CAPS, 11, 1)


def test_uf_cube_cap():
    # test that fig1's cap value is updated as expected
    fig1 = update_fig("cube-tab", D_SCHEME, D_PROTEIN, False, D_OPACITY, D_OPACITY)
    assert fig1["data"][0]["caps"]["x"]["show"] is False
    assert fig1["data"][0]["caps"]["y"]["show"] is False
    assert fig1["data"][0]["caps"]["z"]["show"] is False


def test_uf_cube_cscheme():
    # test that fig1's color scheme value is updated as expected
    fig1 = update_fig("cube-tab", "inferno", D_PROTEIN, D_CAPS, D_OPACITY, D_OPACITY)

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


def test_uf_point_opacity():
    # test that fig2's opacity value is updated as expected
    fig1 = update_fig("point-tab", D_SCHEME, D_PROTEIN, D_CAPS, D_OPACITY, 0.5)
    fig2 = update_fig("point-tab", D_SCHEME, D_PROTEIN, D_CAPS, D_OPACITY, 0)

    assert fig1["data"][0]["opacity"] == 0.5
    assert fig2["data"][0]["opacity"] == 0
    with pytest.raises(ValueError):
        update_fig("point-tab", D_SCHEME, D_PROTEIN, D_CAPS, D_OPACITY, 11)


def test_uf_point_cscheme():
    # test that fig2's color scheme value is updated as expected
    fig1 = update_fig("point-tab", "inferno", D_PROTEIN, D_CAPS, D_OPACITY, D_OPACITY)

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


def test_uf_layer_cscheme():
    # test that fig3's color scheme value is updated as expected
    fig1 = update_fig("layer-tab", "inferno", D_PROTEIN, D_CAPS, D_OPACITY, D_OPACITY)

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


def test_uf_sphere_cscheme():
    # test that fig4's color scheme value is updated as expected
    fig1 = update_fig("sphere-tab", "inferno", D_PROTEIN, D_CAPS, D_OPACITY, D_OPACITY)

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


def test_uo_protein():
    # test that max and min values for the specified protein are as expected
    fig1 = update_fig("cube-tab", D_SCHEME, "GCG", D_CAPS, D_OPACITY, D_OPACITY)

    assert min(fig1["data"][0]["value"]) == protein_df.loc[0, "GCG"]
    assert max(fig1["data"][0]["value"]) == protein_df.loc[1, "GCG"]
