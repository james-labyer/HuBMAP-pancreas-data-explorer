from dash import page_registry
import os
import sys
import pandas as pd

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
import app
from pages.geomx import reports
from pages.home import read_blocks
from pages.constants import FILE_DESTINATION as FD

thumbnails = pd.read_csv(FD["thumbnails"]["catalog"])
blocks = read_blocks()


def test_links():
    relative_paths = []
    for page in page_registry.values():
        relative_paths.append(page["relative_path"])
    for i in range(blocks["Images"].size):
        if blocks["Images"][i] != " ":
            pass
            # block_name = blocks["Images"][i].split("/")[-1]
            # assert block_name in thumbnails["Block"].values
    for j in range(blocks["Reports"].size):
        if blocks["Reports"][j] != " ":
            pass
            # pancreas = blocks["Reports"][j].split("/")[-1]
            # assert pancreas in reports["pancreas"].values
    for k in range(blocks["Proteomics"].size):
        if blocks["Proteomics"][k] != " ":
            pass
            # assert blocks["Proteomics"][k] in relative_paths
