import sys
from pathlib import Path

from dash import page_registry

sys.path.append(str(Path(__file__).parent.parent.parent))
import app.app
from app.pages.geomx import reports
from app.pages.home import blocks
from app.pages.ocfiles import thumbnails


def test_links():
    relative_paths = []
    for page in page_registry.values():
        relative_paths.append(page["relative_path"])
    for i in range(blocks["Optical clearing"].size):
        if blocks["Optical clearing"][i] != " ":
            block_name = blocks["Optical clearing"][i].split("/")[-1]
            assert block_name in thumbnails["Block"].values
    for j in range(blocks["GeoMx"].size):
        if blocks["GeoMx"][j] != " ":
            pancreas = blocks["GeoMx"][i].split("/")[-1]
            assert pancreas in reports["pancreas"].values
    for k in range(blocks["Proteomics"].size):
        if blocks["Proteomics"][k] != " ":
            assert blocks["Proteomics"][k] in relative_paths
