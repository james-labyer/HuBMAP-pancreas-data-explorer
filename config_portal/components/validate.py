import filetype
import io
import pandas as pd
import nh3

VALID_EXTS = {"excel": ["xls", "xlsx"]}
VALID_MIMES = {
    "excel": [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]
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
}


def check_file_type(file, valid_type):
    ftype = filetype.guess(file)
    if (ftype.extension in VALID_EXTS[valid_type]) and (
        ftype.mime in VALID_MIMES[valid_type]
    ):
        return True
    else:
        # add logging
        # print(ftype.extension)
        # print(ftype.mime)
        return False


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
