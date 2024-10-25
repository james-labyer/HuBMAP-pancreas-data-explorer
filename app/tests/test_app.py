from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
import pandas as pd
import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from app.app import update_output

D_PROTEIN = "INS"
D_SCHEME = "jet"
D_OPACITY = 0.4
D_LAYER = "All"
D_CAPS = False

protein_df = pd.read_csv("assets/protein_labels.csv")


def test_uo_fig1opacity():
    # test that fig1's opacity value is updated as expected
    figs1 = update_output(
        0.5,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # D_LAYER,
    )

    figs2 = update_output(
        0,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # D_LAYER,
    )

    assert figs1[0]["data"][0]["opacity"] == 0.5
    assert figs2[0]["data"][0]["opacity"] == 0
    with pytest.raises(ValueError):
        update_output(
            11,
            D_CAPS,
            D_SCHEME,
            D_OPACITY,
            D_SCHEME,
            D_SCHEME,
            # D_OPACITY,
            D_SCHEME,
            D_PROTEIN,
            # D_LAYER,
        )


def test_uo_fig1cap():
    # test that fig1's cap value is updated as expected
    figs1 = update_output(
        D_OPACITY,
        True,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # D_LAYER,
    )
    assert figs1[0]["data"][0]["caps"]["x"]["show"] == True
    assert figs1[0]["data"][0]["caps"]["y"]["show"] == True
    assert figs1[0]["data"][0]["caps"]["z"]["show"] == True


def test_uo_fig1cscheme():
    # test that fig1's color scheme value is updated as expected
    figs1 = update_output(
        D_OPACITY,
        D_CAPS,
        "inferno",
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # D_LAYER,
    )

    assert figs1[0]["data"][0]["colorscale"] == (
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


def test_uo_fig2opacity():
    # test that fig2's opacity value is updated as expected
    figs1 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        0.5,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # D_LAYER,
    )

    figs2 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        0,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # D_LAYER,
    )

    assert figs1[1]["data"][0]["opacity"] == 0.5
    assert figs2[1]["data"][0]["opacity"] == 0
    with pytest.raises(ValueError):
        update_output(
            D_OPACITY,
            D_CAPS,
            D_SCHEME,
            11,
            D_SCHEME,
            D_SCHEME,
            # D_OPACITY,
            D_SCHEME,
            D_PROTEIN,
            # D_LAYER,
        )


def test_uo_fig2cscheme():
    # test that fig2's color scheme value is updated as expected
    figs1 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        "inferno",
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # D_LAYER,
    )

    assert figs1[1]["data"][0]["colorscale"] == (
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


def test_uo_fig3cscheme():
    # test that fig3's color scheme value is updated as expected
    figs1 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        "inferno",
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # D_LAYER,
    )

    assert figs1[2]["data"][0]["colorscale"] == (
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


"""
def test_uo_fig4opacity():
    # test that fig4's opacity value is updated as expected
    figs1 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        0.5,
        D_SCHEME,
        D_PROTEIN,
        D_LAYER,
    )

    figs2 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        0,
        D_SCHEME,
        D_PROTEIN,
        D_LAYER,
    )

    assert figs1[3]["data"][0]["opacity"] == 0.5
    assert figs2[3]["data"][0]["opacity"] == 0
    with pytest.raises(ValueError):
        update_output(
            D_OPACITY,
            D_CAPS,
            D_SCHEME,
            D_OPACITY,
            D_SCHEME,
            D_SCHEME,
            11,
            D_SCHEME,
            D_PROTEIN,
            D_LAYER,
        )
"""


def test_uo_fig4cscheme():
    # test that fig4's color scheme value is updated as expected
    figs1 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        "inferno",
        D_PROTEIN,
        # D_LAYER,
    )

    assert figs1[3]["data"][0]["colorscale"] == (
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


def test_uo_layer():
    # test that z array contains expected values for each layer
    figs1 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # D_LAYER,
    )

    """
    figs2 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # "Layer 1",
    )

    figs3 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # "Layer 2",
    )

    figs4 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # "Layer 3",
    )

    figs5 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        D_PROTEIN,
        # "Layer 4",
    )
    """
    assert np.isin(35, figs1[0]["data"][0]["z"])
    assert np.isin(70, figs1[0]["data"][0]["z"])
    assert np.isin(105, figs1[0]["data"][0]["z"])
    assert np.isin(139.999, figs1[0]["data"][0]["z"])
    assert np.isin(17.5, figs1[1]["data"][0]["z"])
    assert np.isin(52.5, figs1[1]["data"][0]["z"])
    assert np.isin(87.5, figs1[1]["data"][0]["z"])
    assert np.isin(122.5, figs1[1]["data"][0]["z"])

    """
    assert np.isin(34.999, figs2[0]["data"][0]["z"])
    assert not np.isin(70, figs2[0]["data"][0]["z"])
    assert np.isin(17.5, figs2[1]["data"][0]["z"])
    assert not np.isin(87.5, figs2[1]["data"][0]["z"])

    assert np.isin(69.999, figs3[0]["data"][0]["z"])
    assert not np.isin(105, figs3[0]["data"][0]["z"])
    assert np.isin(52.5, figs3[1]["data"][0]["z"])
    assert not np.isin(87.5, figs3[1]["data"][0]["z"])

    assert np.isin(104.999, figs4[0]["data"][0]["z"])
    assert not np.isin(140, figs4[0]["data"][0]["z"])
    assert np.isin(87.5, figs4[1]["data"][0]["z"])
    assert not np.isin(17.5, figs4[1]["data"][0]["z"])

    assert np.isin(139.999, figs5[0]["data"][0]["z"])
    assert not np.isin(70, figs5[0]["data"][0]["z"])
    assert np.isin(122.5, figs5[1]["data"][0]["z"])
    assert not np.isin(17.5, figs5[1]["data"][0]["z"])
    """


def test_uo_protein():
    # test that max and min values for the specified protein are as expected
    figs1 = update_output(
        D_OPACITY,
        D_CAPS,
        D_SCHEME,
        D_OPACITY,
        D_SCHEME,
        D_SCHEME,
        # D_OPACITY,
        D_SCHEME,
        "GCG",
        # D_LAYER,
    )

    assert min(figs1[0]["data"][0]["value"]) == protein_df.loc[0, "GCG"]
    assert max(figs1[0]["data"][0]["value"]) == protein_df.loc[1, "GCG"]
