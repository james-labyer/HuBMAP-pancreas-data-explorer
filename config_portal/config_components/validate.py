import filetype
import io
import pandas as pd
import nh3
import magic
from pathlib import Path
import os
import re
import sys
from config_components import ui, constants
import shutil
import traceback
from PIL import Image, ImageDraw, ImageOps
import logging

MAX_TITLE_LENGTH = 2048
FINAL_THUMBNAIL_SIZE = (220, 110)
THUMBNAIL_TILE = (110, 110)
NAMEREG = r"\.\w{3,8}"  # regex to check file name format
VALID_EXTS = {
    "excel": ["xls", "xlsx"],
    "image": [
        # Allows PNG, AVI, Image Cytometry Standard, OME-TIFF, TIFF, CZI, SVS, AFI, SCN, GDAL, ZVI, DCM, NDPI, and VSI extensions
        "png",
        "jpg",
        "avi",
        "ids",
        "ics",
        "ome.tif",
        "ome.tiff",
        "ome.tf2",
        "ome.tf8",
        "ome.btf",
        "tif",
        "tiff",
        "tf2",
        "tf8",
        "btf",
        "czi",
        "svs",
        "afi",
        "scn",
        "gdal",
        "zvi",
        "dcm",
        "ndpi",
        "vsi",
        "zarr",
    ],
}


VALID_MIMES = {
    "excel": [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ],
    "image": ["image/tiff", "image/png", "video/x-msvideo", "image/jpeg"],
}
EXPECTED_HEADERS = {
    "si-block": {
        "block-data": [
            "Tissue Block",
            "Organ ID",
            "Organ Description",
            "Order",
            "Anatomical region",
            "Images",
            "Reports",
            "Proteomics",
        ],
        "si-files": [
            "Tissue Block",
            "Image Set",
            "Image Category",
            "File",
            "Height",
            "Width",
            "Slices",
            "Channels",
        ],
    },
    "proteomics": {},
    "obj-files": {},
}

FD = constants.FILE_DESTINATION

app_logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
app_logger.handlers = gunicorn_logger.handlers
app_logger.setLevel(gunicorn_logger.level)


def check_file_type(file, valid_type, filename=None):
    ftype = filetype.guess(file)
    if ftype is None:
        if valid_type == "image":
            ftype = magic.from_buffer(file)
            if ftype == "data":
                if filename is None:
                    return False, "Filename missing"
                else:
                    # File content checking is not supported for some needed formats, so just look at extension
                    s = Path(filename).suffix
                    if s[1:] in VALID_EXTS[valid_type]:
                        return True, ""
                    else:
                        return False, f"Invalid file type {s}"
            else:
                # since using magic, need to get mime type from magic and ext from name
                ext = Path(filename).suffix
                mime = magic.from_buffer(file, mime=True)
                if (ext in VALID_EXTS[valid_type]) and (
                    mime in VALID_MIMES[valid_type]
                ):
                    return True, ""
                else:
                    return False, f"Invalid file type {ext}"
        else:
            return False, f"Invalid file type {ftype}"
    elif (ftype.extension in VALID_EXTS[valid_type]) and (
        ftype.mime in VALID_MIMES[valid_type]
    ):
        return True, ""
    else:
        return False, f"Invalid file type {ftype}"


def check_html_helper(some_text):
    if nh3.is_html(str(some_text)):
        return nh3.clean_text(str(some_text))
    else:
        return some_text


def update_links(column, df):
    link_columns = ["Images", "Reports", "Proteomics"]
    i = 0
    if column in link_columns:
        while i < df[column].size:
            links = {
                "Images": f"/scientific-images-list/{df["Tissue Block"].at[i]}",
                "Reports": "/reports",
                "Proteomics": f"/proteomics/{df["Tissue Block"].at[i]}",
            }
            if not (df[column].at[i] == " "):
                df[column].at[i] = links[column]
            i += 1


def process_si_block_file(file, which_headers):
    for key, item in EXPECTED_HEADERS[which_headers].items():
        try:
            df = pd.read_excel(
                io.BytesIO(file), sheet_name=key, engine="calamine", na_values=[" "]
            )
        except ValueError:
            return False, "Worksheet names must match the template."
        except Exception as err:
            return False, f"Import failed with error: {err}"
        for col in ["Images", "Reports", "Proteomics"]:
            if col in df.columns and df.dtypes[col] != "object":
                df[col] = df[col].astype("object")
        # check for appropriate column headers
        df.fillna(" ", inplace=True)
        if df.columns.to_list() == EXPECTED_HEADERS[which_headers][key]:
            # sanitize spreadsheet content
            for column in EXPECTED_HEADERS[which_headers][key]:
                if df[column].dtype == "object":
                    # if column is a string, check for html
                    df[column] = df[column].apply(check_html_helper)
                    # calculate link values for main page links
                    if key == "block-data":
                        update_links(column, df)
            # save validated data as csv
            df.to_csv(FD[which_headers][key]["depot"], index=False)
        else:
            return False, "Column headers must match the template."
    return True, ""


def check_image_name(
    filename: str, df: pd.DataFrame
) -> tuple[int, str, pd.DataFrame, int, str]:
    """This function checks that the provided image name can be associated with an entry
    in the provided DataFrame. PNGs should be named like:

    {Source file name}_C{Channel number, starting at zero}{sequence number, starting at zero and padded with zeroes to four digits}

    Returns (number of matches, filename stem, df filtered to the relevant row, number of channels, error message)
    """
    ext = Path(filename).suffix
    matches = 0
    namestem = ""
    if ext != ".png":
        try:
            matches = df["File"].eq(filename).sum()
            namestem = Path(filename).stem
            filename_reg = re.escape(filename)
            new_df = df[df["File"].str.fullmatch(filename_reg)]
            channel = None
        except Exception as err:
            return (
                0,
                False,
                False,
                False,
                f"{err}",
            )
    else:
        try:
            nameparts = filename.split("_C")
            if len(nameparts) < 2:
                return (
                    0,
                    False,
                    False,
                    False,
                    f"Filename {filename} must use the sequence _C to separate channel data",
                )
            namestem = "_C".join(nameparts[:-1])
            namestem_reg = re.escape(namestem)
            nr = namestem_reg + NAMEREG
            matches = df["File"].str.contains(nr).sum()
            new_df = df[df["File"].str.contains(nr)]
        except Exception as err:
            return (
                0,
                False,
                False,
                False,
                f"{err}",
            )
        try:
            channel = int(nameparts[-1][0])
        except ValueError as err:
            return (
                0,
                False,
                False,
                False,
                "You must specify the channel for this image using the sequence _C as a separator",
            )

    if matches != 1:
        return (
            0,
            False,
            False,
            False,
            f"Filename {filename} must match exactly one filename in metadata",
        )
    else:
        return matches, namestem, new_df, channel, ""


def check_png_name_ending(filename: str) -> tuple[bool, str]:
    """Checks that the second half of a PNG follows the required naming convention:

    {Source file name}_C{Channel number, starting at zero}{sequence number, starting at zero and padded with zeroes to four digits}

    Returns (match test result, error message)
    """
    nameparts = filename.split("_C")
    numreg = r"\d{5}\.png"
    nr = re.compile(numreg)
    m = nr.fullmatch(nameparts[-1])
    if m:
        return m, ""
    else:
        return (
            m,
            f"Filename {filename} must contain exactly five consecutive number characters between the _C sequence and the file extension",
        )


def process_sci_image(file: bytes, filename: str) -> tuple[bool, str]:
    """This function is called when a user uploads files to the scientific images upload widget.
    It checks that image metadata exists and the image name conforms to naming conventions, then
    saves the image to the depot.

    Returns (check results, error message)
    """

    # should validation function clear depot before adding new stuff?
    df = pd.read_csv(FD["si-block"]["si-files"]["publish"])
    if df.empty:
        return False, "You must upload image metadata before uploading images"
    ext = Path(filename).suffix
    # if not a PNG, search for the name exactly
    name_info = check_image_name(filename, df)
    if name_info[0] == 0:
        return False, name_info[4]
    # if PNG, check naming scheme
    if ext == ".png":
        nums_check = check_png_name_ending(filename)
        if not nums_check[0]:
            return (
                nums_check[0],
                nums_check[1],
            )
    # save file
    with open(os.path.join(FD["sci-images"]["depot"], filename), "wb") as fp:
        fp.write(file)
    p = Path(f"{FD["sci-images"]["depot"]}")

    return True, ""


def update_title(value, is_open):
    if value:
        if len(value) > MAX_TITLE_LENGTH:
            return not is_open, ui.failure_toast(
                "Title not updated",
                f"Title must be shorter than {MAX_TITLE_LENGTH} characters. Please try again.",
            )
        else:
            try:
                clean_title = nh3.clean_text(value)
                d = {"title": [clean_title]}
                df = pd.DataFrame(data=d)
                # FILE_DESTINATION["title"]
                df.to_csv(f"{FD["title"]["depot"]}", index=False)
                p = Path(FD["title"]["depot"])
                t = Path(FD["title"]["publish"])
                shutil.copy2(p, t)
                return not is_open, ui.success_toast(
                    "Title updated",
                    "The configuration has been updated. Refresh the public-facing app to see the changes.",
                )
            except Exception as err:
                app_logger.debug(traceback.print_exc())
                return not is_open, ui.failure_toast(
                    "Title not updated", f"{type(err)} {err}"
                )
    else:
        return not is_open, ui.failure_toast(
            "Title not updated", "Please provide a name."
        )


def update_si_block(is_open):
    # move to shared volume /config
    try:
        for key in FD["si-block"].keys():
            # make these paths if they don't exist ?
            p = Path(FD["si-block"][key]["depot"])
            t = Path(FD["si-block"][key]["publish"])
            shutil.move(p, t)
    except FileNotFoundError as err:
        return not is_open, ui.failure_toast(
            "Metadata not updated",
            f"{err}",
            # "File not found. Please ensure you have uploaded a new configuration file."
        )
    return not is_open, ui.success_toast(
        "Metadata updated",
        "The configuration has been updated. Refresh the public-facing app to see the changes.",
    )


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
        new_im = ImageOps.cover(imgs[m], THUMBNAIL_TILE)
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


def generate_thumbnails(idx, tdf):
    # get image metadata
    mdf = pd.read_csv(FD["si-block"]["si-files"]["publish"])
    rd = {"Block": [], "Preview": [], "Name": [], "Link": []}
    new_tr = pd.DataFrame(data=rd, dtype="string")

    # get list of unique image sets from the thumbnail dataframe
    parents = tdf["parent"].unique()
    for i in range(parents.size):
        # check how many channels are in the thumbnail dataframe for this parent, and if it matches metadata
        igroup = tdf[tdf["parent"] == parents[i]]  # one row per channel
        igroup = igroup[igroup["filename"].str.endswith(".png")]  # skip non-PNG files
        # if no new PNG files, stop
        if igroup.empty:
            return
        nr = re.escape(parents[i]) + NAMEREG
        new_df = mdf[mdf["File"].str.contains(nr)]  # parent row in metadata
        # how many channels should be in thumbnail
        channels = new_df["Channels"].values[0]
        imgs = []  # images to include in thumbnail
        # compare number of rows in igroup to channels record in mdf
        if igroup.shape[0] < channels:
            # figure out which channel is missing
            actual_channels = igroup["channel"].values
            missing_channels = []
            for k in range(channels):
                if str(k) not in actual_channels:
                    missing_channels.append(k)
            # attempt to find images for any missing channels
            for m in missing_channels:
                p = Path(igroup["destination"].values[0])
                pdir = p.parent
                for file in pdir.iterdir():
                    if file.is_file() and file.suffix == ".png":
                        nameparts = file.name.split("_C")
                        if int(nameparts[-1][0]) == m:
                            # add to imgs and go to next loop iteration
                            imgs.append(Image.open(file))
                            break
            # add images for present channels
            for q in range(igroup.shape[0]):
                imgs.append(Image.open(igroup["destination"].values[q]))
        else:
            for j in range(channels):
                imgs.append(Image.open(igroup["destination"].values[j]))
        im = make_thumbnail(imgs)
        set_name = new_df["Image Set"].values[0]
        dest = Path(f"{FD["sci-images"]["publish"]}/thumbnails/{set_name}")
        thumbnail_loc = (
            f"{FD["thumbnails"]["publish"]}/{set_name}/{parents[i]}_thumbnail.png"
        )
        if not Path.exists(dest):
            Path.mkdir(dest, parents=True)
        ImageOps.cover(im, FINAL_THUMBNAIL_SIZE).save(
            thumbnail_loc,
            optimize=True,
        )
        # add new row to thumbnail records
        display_shared_vol_root = "assets"
        # {"Block": [], "Preview": [], "Name": [], "Link": []}
        new_tr.loc[i] = [
            new_df["Tissue Block"].values[0],
            f"../../{display_shared_vol_root}{thumbnail_loc}",
            new_df["File"].values[0],
            f"/scientific-images/{new_df["Tissue Block"].values[0]}/{set_name}",
        ]
    # update the thumbnails record so that the display app can access the new thumbnails
    update_thumbnails_record(new_tr)


def update_thumbnails_record(new_tr):
    # new_tr: {"Block": [], "Preview": [], "Name": [], "Link": []}
    # try to open thumbnails workbook
    try:
        df = pd.read_csv(FD["thumbnails"]["catalog"])
    except FileNotFoundError:
        # if the file doesn't exist, check if directory exists and create if needed
        dest = Path(f"{FD['thumbnails']['publish']}")
        if not Path.exists(dest):
            Path.mkdir(dest, parents=True)
        new_tr.to_csv(FD["thumbnails"]["catalog"], index=False)
        return
    # check for duplicate records and skip them (file info should stay the same even if image is new)
    df_idx = df.shape[0]
    for i in range(new_tr.shape[0]):
        # look up row in existing df by "Name"
        filename = new_tr.loc[i, "Name"]
        new_df = df[df["Name"].str.contains(filename)]
        # if not found, add new row
        if new_df.empty:
            df.loc[df_idx] = new_tr.loc[i]
    # once all rows are processed, save updated data
    df.to_csv(FD["thumbnails"]["catalog"], index=False)


def update_new_thumbnails_list(
    tdf: pd.DataFrame,
    tdi: int,
    filename: str,
    filestem: str,
    channels: str,
    dest_dir: str,
) -> tuple[pd.DataFrame, int]:
    """
    Checks whether the provided image needs to be added to the list of thumbnail updates.

    Returns the updated dataframe of updates and updated index.
    """
    # pick one img per channel per set for thumbnail
    # check if there is already a row in tdf for the parent & channel of this image
    tdf_needs_new = False
    if tdf["parent"].str.contains(filestem).empty:
        tdf_needs_new = True
    else:
        parent_rows = tdf.loc[(tdf["parent"].str.contains(filestem))]
        if not parent_rows["channel"].str.contains(channels).any():
            tdf_needs_new = True
    if tdf_needs_new:
        dest_loc = f"{dest_dir}/{filename}"
        tdf.loc[tdi] = [
            filename,
            filestem,
            channels,
            dest_loc,
        ]
        tdi += 1
    return tdf, tdi


def publish_sci_images(src_path: Path, dest_dir: str, filename: str) -> None:
    """Moves a file to a new location, after ensuring the new location exists."""
    try:
        dest = Path(dest_dir)
        if not Path.exists(dest):
            Path.mkdir(dest, parents=True)
        # move to publish dir
        dest_name = Path(f"{dest_dir}/{filename}")
        shutil.move(src_path, dest_name)
    except Exception as err:
        # print(err, file=sys.stdout, flush=True)
        app_logger.debug(traceback.print_exc())


def update_sci_images(is_open: bool) -> tuple[bool, object]:
    """This function is called when the user clicks "Publish" in the Scientific Images section.
    It checks that there is image metadata, then processes each image by checking that the image
    name is valid & present in metadata, then capturing any info needed to create thumbnails, and
    moving the image to the public location. It then calls another function to generate thumbnails.

    Return (all tasks succeeded, dbc.Alert with error or success message)
    """
    # get image location info
    df = pd.read_csv(FD["si-block"]["si-files"]["publish"])
    if df.empty:
        return False, "You must upload image metadata before uploading images"

    p = Path(FD["sci-images"]["depot"])

    # get images in depot
    files = os.listdir(p)

    # start dictionary that will make thumbnails df
    td = {"filename": [], "parent": [], "channel": [], "destination": []}
    tdf = pd.DataFrame(data=td, dtype="string")
    tdi = 0
    # iterate over images in depot
    for file in files:
        child = Path(f"{FD["sci-images"]["depot"]}/{file}")
        # check if a file or dir
        if child.is_file():
            # if file, look up info about destination dir structure
            match_info = check_image_name(child.name, df)
            if match_info[0] == 0:
                return not is_open, ui.failure_toast(
                    "Image not published", match_info[4]
                )
            row = match_info[2]
            if row.empty:
                return not is_open, ui.failure_toast(
                    "Image not published",
                    "All images must be present in the image metadata.",
                )
            try:
                dest_dir = f"{FD["sci-images"]["publish"]}/{row["Tissue Block"].values[0]}/{match_info[1]}"
                tdf, tdi = update_new_thumbnails_list(
                    tdf,
                    tdi,
                    child.name,
                    match_info[1],
                    str(match_info[3]),
                    dest_dir,
                )
                publish_sci_images(child, dest_dir, child.name)
            except Exception as err:
                app_logger.debug(traceback.print_exc())
                return not is_open, ui.failure_toast("Image not published", f"{err}")
    # create thumbnails
    generate_thumbnails(tdi, tdf)
    return not is_open, ui.success_toast(
        "Images published", "Images transferred successfully"
    )
