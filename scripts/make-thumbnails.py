import pandas as pd
from PIL import Image, ImageDraw, ImageOps

img_data = pd.read_csv("thumbnails1-4A.csv")

FINAL_SIZE = (220, 110)
TILE = (110, 110)


def make_thumbnail(imgs):
    w = 0
    h = 0
    for k in range(len(imgs)):
        w += imgs[k].size[0]
        if imgs[k].size[1] > h:
            h = imgs[k].size[1]
    im = Image.new("RGB", (len(imgs) * 110, 110))
    offset = 0
    draw = ImageDraw.Draw(im)
    for m in range(len(imgs)):
        new_im = ImageOps.cover(imgs[m], TILE)
        if m == 0:
            im.paste(new_im)
        else:
            offset += 110
            im.paste(new_im, (offset, 0))
            draw.line(
                [(offset, 0), (offset, h)],
                fill=(255, 255, 255, 255),
                width=2,
            )
    return im


img_sets = {}

for i in range(img_data.shape[0]):
    if img_data.at[i, "parent"] in img_sets:
        img_sets[img_data.at[i, "parent"]].append(img_data.at[i, "filename"])
    else:
        img_sets[img_data.at[i, "parent"]] = []
        img_sets[img_data.at[i, "parent"]].append(img_data.at[i, "filename"])

for set in img_sets:
    set_len = len(img_sets[set])
    if set_len == 1:
        im = Image.open(f"t-in/{img_sets[set][0]}")
        ImageOps.cover(im, FINAL_SIZE).save(f"t-out/{set}_thumbnail.png", optimize=True)
    else:
        imgs = []
        for j in range(set_len):
            imgs.append(Image.open(f"t-in/{img_sets[set][j]}"))
        im = make_thumbnail(imgs)
        ImageOps.cover(im, FINAL_SIZE).save(f"t-out/{set}_thumbnail.png", optimize=True)
