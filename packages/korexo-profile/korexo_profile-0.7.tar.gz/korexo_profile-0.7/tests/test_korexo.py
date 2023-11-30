import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest


import numpy as np
from datetime import date
from pathlib import Path

cwd = Path(os.path.dirname(__file__))

import korexo_profile


def test_example1():
    data = korexo_profile.read(cwd / "example1.csv")


def test_example2():
    data = korexo_profile.read(cwd / "example2.csv")


def test_example2_utf8():
    data = korexo_profile.read(cwd / "example2_utf8.csv", encoding="utf-8")


def test_example2_utf8_encoding_fail_check():
    with pytest.raises(UnicodeDecodeError):
        data = korexo_profile.read(cwd / "example2_utf8.csv", auto_revert_encoding=False)


def test_datefmt_auto():
    data = korexo_profile.read(cwd / "example1.csv", datefmt="auto")
    datecol = data["datasets"][0]
    assert datecol["median"] == date(2019, 11, 12)


def test_datefmt_specified():
    data = korexo_profile.read(cwd / "example1.csv", datefmt="%d/%m/%Y")
    datecol = data["datasets"][0]
    assert datecol["median"] == date(2019, 12, 11)


def test_datefmt_specified_2():
    data = korexo_profile.read(cwd / "example1.csv", datefmt="%m/%d/%Y")
    datecol = data["datasets"][0]
    assert datecol["median"] == date(2019, 11, 12)


def test_remapping():
    data = korexo_profile.read(cwd / "example1.csv")
    df = korexo_profile.convert_datasets_to_df(data["datasets"])
    assert list(df.columns) == [
        "datetime",
        "date",
        "time",
        "time_sec",
        "site",
        "cond",
        "water_depth",
        "cond_nlf",
        "do_sat",
        "do_local",
        "do_conc",
        "orp_mv",
        "press",
        "sal_psu",
        "spcond",
        "tds",
        "ph",
        "ph_mv",
        "temp",
        "vert_pos",
        "battery",
        "cable_power",
    ]

def test_resampling():
    data = korexo_profile.read(cwd / "example1_full.csv")
    df = korexo_profile.convert_datasets_to_df(data["datasets"])
    df["dtw"] = df.water_depth + 5.15
    df2 = korexo_profile.make_regularly_spaced(df, "dtw", step=0.05)
    # Check that it is less than 1 cm; previously 1 mm which was too harsh on the interpolation.
    assert (np.abs(df2.index.values[:3] - np.asarray([5.15, 5.20, 5.25])) <= 0.01).all()