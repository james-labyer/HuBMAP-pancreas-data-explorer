import sys
from pathlib import Path
from dash import page_registry

sys.path.append(str(Path(__file__).parent.parent.parent))
from app.pages.P119AocFiles import data

# some pages require files that are too large to check into GitHub, so they
# must be skipped when this is run in the GitHub Action
dev_pages = [2, 3, 6, 7, 8, 10]


def test_links():
    relative_paths = []
    for page in page_registry.values():
        relative_paths.append(page["relative_path"])
    for i in range(data["Link"].size):
        if (i + 1) in dev_pages:
            assert data["Link"][i] in relative_paths
