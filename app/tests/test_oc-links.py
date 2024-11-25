import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent.parent))
import app.app
from app.pages.P17AocFiles import data as data7a
from app.pages.P114AocFiles import data as data14a

oc = pd.read_csv("assets/optical-clearing-czi/oc-files.csv")

# some pages require files that are too large to check into GitHub, so they
# must be skipped when this is run in the GitHub Action
dev_pages_7a = [3, 4, 7, 8, 9, 10, 11]
dev_pages_14a = [1, 3, 4, 6, 8, 9, 11]


def test_7a_links():
    # check that each link in AocFiles references an oc that exists in oc-files.csv
    for i in range(data7a["Link"].size):
        link_oc = data7a.at[i, "Link"].split("/")[-1]
        assert link_oc in oc["oc"].values


def test_14a_links():
    # check that each link in AocFiles references an oc that exists in oc-files.csv
    for i in range(data14a["Link"].size):
        link_oc = data14a.at[i, "Link"].split("/")[-1]
        assert link_oc in oc["oc"].values
