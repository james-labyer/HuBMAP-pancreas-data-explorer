FILE_DESTINATION = {
    "si-block": {
        "block-data": {"depot": "./depot/blocks.csv", "publish": "/config/blocks.csv"},
        "si-files": {
            "depot": "./depot/image-sets.csv",
            "publish": "/config/image-sets.csv",
        },
    },
    "spatial-map": {
        "meta": {"depot": "./depot/spatial-map", "publish": "/config/spatial-map"},
        "downloads": {
            "depot": "./depot/spatial-map",
            "publish": "/config/spatial-map",
        },
        "downloads-file": {
            "depot": "./depot/spatial-map/downloads.csv",
            "publish": "/config/spatial-map/downloads.csv",
        },
    },
    "obj-files": {
        "summary": {"depot": "./depot/obj", "publish": "/config/obj"},
        "volumes": {"depot": "./depot/obj/volumes", "publish": "/config/obj/volumes"},
    },
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
