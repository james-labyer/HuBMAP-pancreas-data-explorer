import filetype
import io
import pandas as pd
import nh3
import magic
from pathlib import Path
import os
import re

VALID_EXTS = {
    "excel": ["xls", "xlsx"],
    "image": [
        # Allows PNG, AVI, Image Cytometry Standard, OME-TIFF, TIFF, CZI, SVS, AFI, SCN, GDAL, ZVI, DCM, NDPI, and VSI extensions
        "png",
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
    "image": ["image/tiff", "image/png", "video/x-msvideo"],
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
FILE_DESTINATION = {
    "si-block": {
        "block-data": "./depot/blocks.csv",
        "si-files": "./depot/image-sets.csv",
    },
    "proteomics": "",
    "obj-files": "",
    "sci-images": "./depot/images",
}


def check_file_type(file, valid_type, filename=None):
    ftype = filetype.guess(file)
    # print(ftype)
    if ftype is None:
        if valid_type == "image":
            # print(magic.from_buffer(file, mime=True))
            ftype = magic.from_buffer(file)
            if ftype == "data":
                if filename is None:
                    return False, "Filename missing"
                else:
                    # File content checking is not supported for some needed formats, so just look at extension
                    print("success, used ext")
                    s = Path(filename).suffix
                    if s[1:] in VALID_EXTS[valid_type]:
                        return True, ""
                    else:
                        return False, "Invalid file type"
            else:
                # since using magic, need to get mime type from magic and ext from name
                ext = Path(filename).suffix
                mime = magic.from_buffer(file, mime=True)
                if (ext in VALID_EXTS[valid_type]) and (
                    mime in VALID_MIMES[valid_type]
                ):
                    print("success, used filetype")
                    return True, ""
                else:
                    return False, "Invalid file type"
        else:
            return False, "Invalid file type"
    elif (ftype.extension in VALID_EXTS[valid_type]) and (
        ftype.mime in VALID_MIMES[valid_type]
    ):
        print("success, used filetype")
        return True, ""
    else:
        return False, "Invalid file type"


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
            df.to_csv(FILE_DESTINATION[which_headers][key], index=False)
            return True, ""
        else:
            return False, "Column headers must match the template."


def process_sci_image(file, filename):
    # find image in metadata
    # send image to main server
    # "si-block" "si-files"
    df = pd.read_csv(FILE_DESTINATION["si-block"]["si-files"])
    if df.empty:
        return False, "You must upload image metadata before uploading images"
    ext = Path(filename).suffix
    # if not a PNG, search for the name exactly
    matches = 0
    end_nums = False
    if ext != ".png":
        matches = df["File"].eq(filename).sum()
        end_nums = True
    # if PNG, check naming scheme
    else:
        # {Source file name}_C{Channel number, starting at zero}{sequence number, starting at zero and padded with zeroes to four digits}
        nameparts = filename.split("_C")
        if len(nameparts) != 2:
            return False, "Filename must contain the sequence _C exactly once"
        namereg = nameparts[0] + r"\.\w{3,8}"
        matches = df["File"].str.contains(namereg).sum()
        numreg = r"\d{5}\.png"
        nr = re.compile(numreg)
        m = nr.fullmatch(nameparts[1])
        if m:
            end_nums = True

    if matches != 1:
        # error
        return False, "Filename must match exactly one filename in metadata"
    elif not end_nums:
        return False, "Filename must end in exactly five number characters"
    else:
        # save file
        with open(os.path.join(FILE_DESTINATION["sci-images"], filename), "wb") as fp:
            fp.write(file)
        return True, ""


# "No files over 1 GB. Can upload source files for download from website and .PNG images for display on website. Source file names must match names in image metadata file exactly. PNG image names must be of the following format: {Source file name}_C{Channel number, starting at zero}{sequence number, starting at zero and padded with zeroes to four digits}. Example: P1_4A2_image_stack_C10001.png . New images will replace existing images with the same name."
