import sys
from pathlib import Path
from dash import page_registry

sys.path.append(str(Path(__file__).parent.parent.parent))
from app.pages.P114AocFiles import data


def test_links():
    relative_paths = []
    for page in page_registry.values():
        relative_paths.append(page["relative_path"])
    for i in range(data["Link"].size):
        assert data["Link"][i] in relative_paths
