from dash import page_registry

import app
from pages.geomx import reports
from pages.home import read_blocks
from pages.ocfiles import thumbnails

blocks = read_blocks()


def test_links():
    relative_paths = []
    for page in page_registry.values():
        relative_paths.append(page["relative_path"])
    for i in range(blocks["Images"].size):
        if blocks["Images"][i] != " ":
            block_name = blocks["Images"][i].split("/")[-1]
            # assert block_name in thumbnails["Block"].values
    for j in range(blocks["Reports"].size):
        if blocks["Reports"][j] != " ":
            pancreas = blocks["Reports"][j].split("/")[-1]
            # assert pancreas in reports["pancreas"].values
    for k in range(blocks["Proteomics"].size):
        if blocks["Proteomics"][k] != " ":
            pass
            # assert blocks["Proteomics"][k] in relative_paths
