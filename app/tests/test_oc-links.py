import os
import sys
import pandas as pd

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
import app
from pages.ocpage import s_imgs
from pages.constants import FILE_DESTINATION as FD

thumbnails = pd.read_csv(FD["thumbnails"]["catalog"])


def test_oc_page_links():
    # check that each link in on the oc file summary pages references an oc that exists in ocpage
    for i in range(thumbnails["Link"].size):
        link_oc = thumbnails.at[i, "Link"].split("/")[-1]
        link_block = thumbnails.at[i, "Link"].split("/")[-2]
        assert link_oc in s_imgs["Image Set"].values
        assert link_block in s_imgs["Tissue Block"].values
