FILE_DESTINATION = {
    "si-block": {
        "block-data": {"depot": "./depot/blocks.csv", "publish": "/config/blocks.csv"},
        "si-files": {
            "depot": "./depot/image-sets.csv",
            "publish": "/config/image-sets.csv",
        },
    },
    "proteomics": {"depot": "", "publish": ""},
    "obj-files": {"depot": "", "publish": ""},
    "sci-images": {
        "depot": "./depot/scientific-images",
        "publish": "/config/scientific-images",
    },
    "thumbnails": {
        "publish": "/config/scientific-images/thumbnails",
        "catalog": "/config/scientific-images/thumbnails/thumbnails.csv",
    },
    "title": {"depot": "./config/labels.csv", "publish": "/config/labels.csv"},
}
