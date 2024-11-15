import sys
from pathlib import Path
from dash import dcc, Dash

from dash_slicer import VolumeSlicer

sys.path.append(str(Path(__file__).parent.parent.parent))
import app.app
from app.pages.P114Aopticalclearing import (
    P114Aopticalclearing1,
    P114Aopticalclearing3,
    P114Aopticalclearing8,
)


def test_make_vol():
    app = Dash()
    vol_list = [
        {
            "vols": P114Aopticalclearing1.vols,
            "shapes": [(1, 2048, 2048), (1, 2048, 2048)],
            "slices": [1, 1],
        },
        {"vols": P114Aopticalclearing3.vols, "shapes": [(1, 947, 1185)], "slices": [1]},
        {
            "vols": P114Aopticalclearing8.vols,
            "shapes": [(99, 256, 256)],
            "slices": [99],
        },
    ]
    for vol_set in vol_list:
        for i in range(len(vol_set["vols"])):
            assert vol_set["vols"][i].shape == vol_set["shapes"][i]
            s = VolumeSlicer(app, vol_set["vols"][i])
            assert isinstance(s.graph, dcc.Graph)
            assert isinstance(s.slider, dcc.Slider)
            assert s.nslices == vol_set["slices"][i]


def test_apply_overlay():
    overlay1 = P114Aopticalclearing1.apply_overlay(0, 0)
    assert isinstance(overlay1, list)

    overlay2 = P114Aopticalclearing8.apply_overlay(0, 0)
    assert isinstance(overlay2, list)
