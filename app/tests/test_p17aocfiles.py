import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent.parent))
import app.app
from app.pages.P17AocFiles import data

# some pages require files that are too large to check into GitHub, so they
# must be skipped when this is run in the GitHub Action
dev_pages = [3, 4, 7, 8, 9, 10, 11]

oc = pd.read_csv("assets/optical-clearing-czi/oc-files.csv")


def test_7a_links():
    # check that each link in AocFiles references an oc that exists in oc-files.csv
    for i in range(data["Link"].size):
        link_oc = data.at[i, "Link"].split("/")[-1]
        assert link_oc in oc["oc"].values
