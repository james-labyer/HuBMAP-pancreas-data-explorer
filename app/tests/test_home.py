import sys
from pathlib import Path
from dash import page_registry

sys.path.append(str(Path(__file__).parent.parent.parent))
from app.pages.home import blocks


def test_links():
    relative_paths = []
    for page in page_registry.values():
        relative_paths.append(page["relative_path"])
    for i in range(blocks["Optical clearing"].size):
        if blocks["Optical clearing"][i] != " ":
            assert blocks["Optical clearing"][i] in relative_paths
    for j in range(blocks["GeoMX"].size):
        if blocks["GeoMX"][j] != " ":
            assert blocks["GeoMX"][j] in relative_paths
    for k in range(blocks["Proteomics"].size):
        if blocks["Proteomics"][k] != " ":
            assert blocks["Proteomics"][k] in relative_paths
