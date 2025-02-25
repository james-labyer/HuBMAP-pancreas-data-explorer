import app
from pages.ocfiles import thumbnails
from pages.ocpage import s_imgs


def test_oc_page_links():
    # check that each link in on the oc file summary pages references an oc that exists in ocpage
    for i in range(thumbnails["Link"].size):
        link_oc = thumbnails.at[i, "Link"].split("/")[-1]
        link_block = thumbnails.at[i, "Link"].split("/")[-2]
        assert link_oc in s_imgs["Image Set"].values
        assert link_block in s_imgs["Tissue Block"].values
