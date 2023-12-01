
#! -*- coding: utf-8 -*-
"""Library to read and write dataframes"""

import os
import pandas as pd

def get_dataframe(ds_name, project_id=os.getenv("project_id"), row_count=-1, strategy="top", user_id="1001",
                  filter_condition=None):
    pass


def get_local_dataframe(local_file_path, row_count=-1):
    """
    Param:
        local_file_path,
        row_count
    To read data frame from NAS local file system
    """
    try:
        sub_type = local_file_path.split(".")[-1]
        nrows = row_count if int(row_count) > 0 else None
        if sub_type == "csv":
            return pd.read_csv(filepath_or_buffer=local_file_path,
                               sep=",",
                               nrows=nrows)
        elif sub_type == "tsv":
            return pd.read_csv(filepath_or_buffer=local_file_path,
                               sep="\t",
                               nrows=nrows)
        elif sub_type == "xlsx":
            return pd.read_excel(io=local_file_path,
                                 nrows=nrows,
                                 parse_dates=False,
                                 engine="openpyxl")
        elif sub_type == "xls":
            return pd.read_excel(io=local_file_path,
                                 nrows=nrows,
                                 parse_dates=False)
    except Exception as ex:
        print(f"Exception occurred in get_local_dataframe: {ex}")

