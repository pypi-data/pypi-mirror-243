from collections import defaultdict
from datetime import datetime
from pathlib import Path
import os
from pprint import pprint, pformat

import lasio
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from scipy.interpolate import interp1d


def convert_numeric(v):
    if v == "NA":
        return pd.NA
    else:
        return pd.to_numeric(v)


def read(
    fn, encoding="utf-16", parse_dts=True, datefmt="auto", auto_revert_encoding="cp1252"
):
    """Read KorEXO sonde profile.

    Args:
        fn (str): filename
        encoding (str): file encoding. I believe raw KorEXO output is
            in UTF-16.
        parse_dts (bool): whether to attempt to parse datetimes
            or not.
        datefmt (str): use "auto" to use the column header to infer the date
            format, although note that this isn't always correct. In that case,
            set it here using Python datetime string formats e.g.
            ``"%d/%m/%Y"``
        auto_revert_encoding (str or None/False): attempt to check whether
            the file is UTF-16 and if it is not i.e. there is no BOM, then use
            whatever encoding is set here. Set to ``False`` only if you want the
            code to attempt *encoding* and fail messily if it is not.

    Returns:
        dict: with keys 'metadata', 'dataframe' and 'datasets'. See
        package documentation for more details.

    """
    if auto_revert_encoding:
        values = open(fn, "rb").read(2)
        if values != b"\xff\xfe":
            encoding = auto_revert_encoding
    with open(fn, "rb") as f:
        count = 0
        header_line = 0
        for i, line in enumerate(f.read().decode(encoding).splitlines()):
            if i < 1:
                # print(f"i < 1: {i}: {line}")
                continue
            elif i > 1:
                if count == 0:
                    # print(f"i > 1: count==0: {i}: {line}")
                    break
                else:
                    # print(f"i > 0: {i}: {line}")
                    if line.startswith("Date ("):
                        header_line = i
                        break
            else:
                # print(f"i == 0: {i}: {line}")
                for char in line:
                    if char == ",":
                        count += 1
                # print(f" (count=={count})")
        if count > 0:
            return _read_korexo_format(fn, encoding, parse_dts, datefmt)
        else:
            return _read_korexo_format(fn, encoding, parse_dts, datefmt)


def _read_korexo_format(fn, encoding, parse_dts=True, datefmt="auto"):
    md = {}
    md["created_file"] = datetime.fromtimestamp(os.path.getctime(fn))
    md["modified_file"] = datetime.fromtimestamp(os.path.getmtime(fn))
    p_offset = 4
    with open(fn, "rb") as f:
        for i, line in enumerate(f.read().decode(encoding).splitlines()):
            if line.startswith("FILE CREATED"):
                created_stated = line.split(",", 1)[1].strip()
                md["created_info"] = created_stated
            elif "MEAN VALUE:" in line:
                means_line = line.split(",")
                means = [convert_numeric(x) for x in means_line[p_offset:]]
            elif "STANDARD DEVIATION:" in line:
                stdev_line = line.split(",")
                stdevs = [convert_numeric(x) for x in stdev_line[p_offset:]]
            elif "SENSOR SERIAL NUMBER:" in line:
                sensor_line = line.split(",")
                sensors = sensor_line[p_offset:]
            elif line.startswith("Date ("):
                md["header_line_no"] = i + 1
                params_ = line.split(",")
                params = params_[p_offset:]
                indices = [i for i in range(len(params)) if params[i] != ""]
                md["params"] = [params[i] for i in indices]
                md["sensors"] = [sensors[i] for i in indices]
                md["means"] = [means[i] for i in indices]
                md["stdevs"] = [stdevs[i] for i in indices]
    df = pd.read_csv(
        fn,
        skiprows=(md["header_line_no"] - 1),
        encoding=encoding,
    )
    record = {}
    datasets = []
    # print(f"md = \n" + pformat(md))
    for i in range(len(params_)):
        param = params_[i]
        # print(f"{i} {param}")
        if i >= p_offset and param != "":
            pi = i - p_offset
            data = df[param].values
            if len(np.unique(data)) == 1:
                median = data[0]
            else:
                try:
                    median = np.median(data)
                except TypeError:
                    median = data[0]
            dataset = {
                "name": params[pi],
                "column": param,
                "sensor": sensors[pi],
                "mean": means[pi],
                "stdev": stdevs[pi],
                "data": data,
                "median": median,
            }
            datasets.append(dataset)
        elif params_[i] != "":
            param = params_[i]
            if "(" in param:
                name = param.split("(", 1)[0].strip()
            else:
                name = param
            data = df[param].values
            if parse_dts:
                if name == "Date":
                    if datefmt == "auto":
                        unitfmt = param.split("(", 1)[1][:-1].strip()
                        if unitfmt == "MM/DD/YYYY":
                            datefmt = "%m/%d/%Y"
                        elif unitfmt == "DD/MM/YYYY":
                            datefmt = "%d/%m/%Y"
                        if len(data) > 0:
                            parts = data[0].split("/")
                            first = parts[0]
                            second = parts[1]
                            if unitfmt == "MM/DD/YYYY" and int(first) > 12:
                                datefmt = "%d/%m/%Y"
                            elif unitfmt == "DD/MM/YYYY" and int(second) > 12:
                                datefmt = "%m/%d/%Y"
                            else:
                                pass
                    try:
                        data = [
                            ts.date()
                            for ts in pd.to_datetime(
                                data, format=datefmt, errors="coerce"
                            )
                        ]
                    except:
                        pass
            if len(np.unique(data)) == 1:
                median = data[0]
            else:
                try:
                    median = np.median(data)
                except TypeError:
                    median = data[0]
            dataset = {
                "name": name,
                "column": param,
                "sensor": "",
                "mean": pd.NA,
                "stdev": pd.NA,
                "data": data,
                "median": median,
            }
            datasets.append(dataset)
    record["metadata"] = md
    record["datasets"] = datasets
    record["dataframe"] = df
    return record


COL_MAPPING = defaultdict(lambda: "NA")
COL_MAPPING = {}
COL_MAPPING.update(
    {
        "Date (MM/DD/YYYY)": "date",
        "Date (DD/MM/YYYY)": "date",
        "Time (HH:mm:ss)": "time",
        "Time (Fract. Sec)": "time_sec",
        "Site Name": "site",
        "Cond µS/cm": "cond",
        "Depth m": "water_depth",
        "nLF Cond µS/cm": "cond_nlf",
        "ODO % sat": "do_sat",
        "ODO % local": "do_local",
        "ODO mg/L": "do_conc",
        "ORP mV": "orp_mv",
        "Pressure psi a": "press",
        "Sal psu": "sal_psu",
        "SpCond µS/cm": "spcond",
        "TDS mg/L": "tds",
        "pH": "ph",
        "pH mV": "ph_mv",
        "Temp °C": "temp",
        "Vertical Position m": "vert_pos",
        "Battery V": "battery",
        "Cable Pwr V": "cable_power",
    }
)


def convert_datasets_to_df(datasets, mapping=COL_MAPPING):
    """Convert a list of datasets to a dataframe, include renaming of
    column names if desired.

    Args:
        datasets (list): see output of :func:`korexo_profile.read`.
        mapping (dict): optional. The default mapping is stored
            in korexo_profile.COL_MAPPING

    Returns: 
        pandas.DataFrame: dataframe with "datetime" column added.

    """
    ##### TODO FIX THIS SO THAT ANY COLUMNS CAN SURVIVE THE MAPPING
    mapping = dict(mapping) # make a copy
    missing_from_mapping = []
    for dset in datasets:
        if not dset['column'] in mapping:
            mapping[dset['column']] = dset['column']
            
    df = pd.DataFrame({mapping[dset["column"]]: dset["data"] for dset in datasets})
    timestamp = df["date"].astype(str) + " " + df["time"].astype(str)
    timestamps = pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S")
    df.insert(0, "datetime", timestamps)
    return df


def make_regularly_spaced(df, index_col="dtw", step=0.05, step_precision=5):
    """Convert dataframe to regular spacing based on an index column.

    Args:
        df (pandas DataFrame)
        index_col (str): column of *df* for which a regularly-spaced set of
            values should be created at *step* and then all other data
            interpolated against.
        step (float): interval desired in *index_col*
        step_precision (int)

    Returns:
        pandas.DataFrame: dataframe, where the newly created *index_col* values are set
        as the dataframe index. All other columns of *df* are included
        as columns of the *df*, interpolated at the new *index_col* values.

    """
    index_min = np.round(df[index_col].min(), 0) - 1
    while index_min < df[index_col].min():
        index_min += step
    index_min = np.round(index_min - step, step_precision)

    index_max = np.round(df[index_col].max(), 0) + 1
    while index_max > df[index_col].max():
        index_max -= step
    index_max = np.round(index_max + step, step_precision)

    index_new = np.linspace(
        index_min, index_max, int((index_max - index_min) / step) + 1
    )

    new_df = {}
    groupby = df.groupby(index_col)
    for col in df.columns:
        if is_numeric_dtype(df[col]) and not col == index_col:
            series = groupby[col].mean()
            data = interp1d(
                series.index, series.values, assume_sorted=True, bounds_error=False
            )(index_new)
            new_df[col] = data
    return pd.DataFrame(new_df, index=index_new).rename_axis(index_col)


def to_las(
    df,
    fn,
    encoding="utf-16",
    col_metadata=None,
    well_metadata=None,
    param_metadata=None,
    add_mtime_date="DATE",
    auto_revert_encoding="cp1252",
):
    """Convert a KorEXO profile file to Log ASCII Standard (LAS).

    Args:
        df (pandas DataFrame): a regularly-spaced output from
            reading a KorEXO profile CSV file.
        fn (str): the original CSV file
        col_metadata (dict): optional metadata for the columns. The keys should
            refer to columns of *df* and each value should be a tuple.
            The first item of the tuple is a string for the unit
            e.g. ``"m"``, and the second item is the description.
        well_metadata (dict): dict of metadata to add to the LAS
            file's ~Well section.
        param_metadata (dict): dict of metadata to add to the LAS
            file's ~Param section
        add_mtime_date (str): add the file modified time of *fn*
            as a value in the ~Well section. Set to False or None
            to prevent adding it at all.
        auto_revert_encoding (bool): attempt to check whether the file is UTF-16
            and if it is not i.e. there is no BOM, then use this encoding
            instead. Set to ``False`` only if you want the code to fail
            messily if you have the encoding wrong.

    Returns:
        lasio.LASFile object

    The contents of the original KorEXO profile CSV file will be
    recorded in the LAS file's ~Other block.

    Example:

    .. code-block::

        >>> import korexo_profile
        >>> data = korexo_profile.read(fn, datefmt="%d/%m/%Y")
        >>> df = korexo_profile.convert_datasets_to_df(data["datasets"])
        >>> df["depth"] = df["vert_pos"] + 0.27 + WELL_DEPTH_TO_WATER_MEASUREMENT
        >>> df2 = korexo_profile.make_regularly_spaced(df, "water_depth", step=0.05)
        >>> las = korexo_profile.to_las(df2, fn)

    """
    if auto_revert_encoding:
        values = open(fn, "rb").read(2)
        if values != b"\xff\xfe":
            encoding = auto_revert_encoding

    if col_metadata is None:
        col_metadata = {}
    if well_metadata is None:
        well_metadata = {}
    if param_metadata is None:
        param_metadata = {}

    las = lasio.LASFile()
    las.set_data_from_df(
        df,
    )
    for curve in las.curves:
        if curve.mnemonic in col_metadata.keys():
            unit, descr = col_metadata[curve.mnemonic]
            curve.unit = unit
            curve.descr = descr

    p = Path(fn)
    stat = p.stat()

    from datetime import datetime as dt_class

    ctime = pd.Timestamp(dt_class.fromtimestamp(stat.st_ctime))
    mtime = pd.Timestamp(dt_class.fromtimestamp(stat.st_mtime))
    other = f"Filename: {p.absolute()}"
    other += f"\nFile creation date: {ctime}"
    other += f"\nFile modified date: {mtime}"
    other += "\nFile contents follow.\n"
    with open(fn, "rb") as f:
        other += f.read().decode(encoding)
    las.other = other

    for key, value in well_metadata.items():
        if "DATE" in las.well:
            del las.well["DATE"]

        if not key in las.well:
            las.well.append(lasio.HeaderItem(key, value=value))
        else:
            las.well[key] = value

    for key, value in param_metadata.items():
        if not key in las.params:
            las.params.append(lasio.HeaderItem(key, value=value))
        else:
            las.params[key] = value

    if add_mtime_date:
        las.well.append(
            lasio.HeaderItem(add_mtime_date, value=mtime.strftime("%Y-%m-%d"))
        )

    return las