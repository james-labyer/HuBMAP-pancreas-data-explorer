import os
from PIL import Image, ImageOps, ImageDraw
import pandas as pd

img_data = pd.read_csv("thumbnails.csv")

FINAL_SIZE = (220, 110)


def make_thumbnail(img1, img2):
    w = img1.size[0] + img2.size[0]
    h = max(img1.size[1], img2.size[1])
    im = Image.new("RGB", (w, h))
    im.paste(img1)
    im.paste(img2, (img1.size[0], 0))
    draw = ImageDraw.Draw(im)
    draw.line(
        [(img1.size[0], 0), (img1.size[0], h)],
        fill=(255, 255, 255),
        width=10,
    )
    return im


parent = ""
children = []
imgs = []
for i in range(img_data.shape[0]):
    if parent == "":
        parent = img_data.at[i, "parent"]
        children.append(img_data.at[i, "filename"])
    elif parent != "" and img_data.at[i, "parent"] == parent:
        children.append(img_data.at[i, "filename"])
        for j in range(len(children)):
            imgs.append(Image.open(f"t-in/{children[j]}"))
        im = make_thumbnail(imgs[0], imgs[1])
        ImageOps.cover(im, FINAL_SIZE).save(f"t-out/{parent}_thumbnail.png")
        parent = ""
        children = []
        imgs = []
    elif parent != "" and img_data.at[i, "parent"] != parent:
        # previous img was from a one-channel image, process it
        im = Image.open(f"t-in/{children[0]}")
        ImageOps.contain(im, FINAL_SIZE).save(f"t-out/{parent}_thumbnail.png")
        # set up this one for processing
        children = []
        parent = img_data.at[i, "parent"]
        children.append(img_data.at[i, "filename"])
