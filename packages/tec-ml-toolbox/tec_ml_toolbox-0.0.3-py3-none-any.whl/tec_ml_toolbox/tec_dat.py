import os
import re
from datetime import date, datetime, timedelta
from os import walk
from os.path import join
from typing import TypedDict

import pandas as pd
import tqdm

NEEDED_PARAMETERS = (
    "hmax",
    "FiltWindow",
    "Time Range",
    "Minimum duration of series",
    "time step",
)

DATA_HEADERS = (
    "tsn",
    "time",
    "el",
    "az",
    "latp",
    "lonp",
    "tec",
    "tec_filtered",
    "validity",
)


class TecDataFrame(TypedDict):
    name: str
    df: pd.DataFrame


class SiteSatParsed(TypedDict):
    day_number: int
    receiver_code: str
    sat_code: str


def date_by_number(year: int = 1970, day_number: int = 1) -> datetime:
    """Calculate the date by given year and day of year number.
    Returns a datetime with 0h 0m 0s."""

    assert 1900 <= year <= 9999, "Year must be from 1900 to 9999."
    assert 1 <= day_number <= 366, "Day of year must be from 1 to 366."

    return datetime.combine(
        date(year, 1, 1) + timedelta(days=day_number - 1), datetime.min.time()
    )


def parse_site_sat_filename(filename: str = "") -> SiteSatParsed:
    """Parse file path with name of site-sat pair with DOY `foo\\bar\\stk2G20_165.dat` where:
    stk2 - GNSS site (4 symbols, may start with _),
    G20 - sat code,
    165 - DOY."""

    site_sat_doy = os.path.basename(os.path.splitext(filename)[0])
    regexp = re.compile(r"^(\w{4,4})([G,R]\d\d)_(\d\d\d)$")
    match_name = regexp.match(site_sat_doy)

    assert match_name is not None, "Filename dosn't match to pattern"

    return {
        "receiver_code": match_name.group(1),
        "sat_code": match_name.group(2),
        "day_number": int(match_name.group(3)),
    }


def dat_to_df(filename: str = "", year: int = 1970) -> pd.DataFrame:
    """Read TEC .dat file to dataframe. Used cols: time, filtered_tec, tec.
    Date converts to pandas datetime."""

    # name, _ = os.path.basename(filename).split(".")
    file_name_parts = parse_site_sat_filename(filename)

    dataframe = pd.read_csv(
        filepath_or_buffer=filename,
        delim_whitespace=True,
        comment="#",
        names=DATA_HEADERS,
    )
    # combine year and DOY and add to dataframe
    dt = date_by_number(year=year, day_number=file_name_parts["day_number"])
    dataframe["time"] = (
        pd.to_timedelta(dataframe["time"], unit="h").add(dt).astype("datetime64[s]")
    )

    return dataframe[["time", "tec_filtered", "tec"]].rename(
        columns={"time": "timestamp", "tec": "vtec"}
    )


def get_file_list(path: str = "", template: str = ".*") -> list[str]:
    """Files list by name pattern."""

    file_list = []
    for dirpath, _, filenames in walk(path):
        for filename in filenames:
            if re.match(template, filename) is not None:
                file_list.append(join(dirpath, filename))

    return file_list


def get_parts_dataset(df=None, fname="", size=30, step=30):
    """Деление датафрейма на равные части размера окна с шагом step."""

    roll = list(df.rolling(window=size))[size - 1 :: step]
    roll = [window for window in roll if len(window) == size]
    return [(f"{fname}.{i}", part) for i, part in enumerate(roll, 1)]


def _get_bounds_chunks(df=None, time_gap=60):
    """Вычисление точек - границ сегментов ряда
    между большими временными перерывами."""

    df["LONG_"] = (df["timestamp"].diff()).dt.seconds > time_gap
    df2 = df[df["LONG_"] == True]

    df.drop("LONG_", axis=1, inplace=True)
    df2.drop("LONG_", axis=1, inplace=True)

    bounds = []

    for r in df2.index:
        bounds.append(df["timestamp"].iloc[r - 1])
        bounds.append(df["timestamp"].iloc[r])

    bounds = [df["timestamp"].iloc[0], *bounds, df["timestamp"].iloc[-1]]

    return [bounds[i : i + 2] for i in range(0, len(bounds), 2)]


def split_df(df=None, time_gap=120):
    """Разделение датафрейма ряда на куски
    разделенные большим временным перерывом.
    Т.к. исходные данные содежат перерывы.
    Длительносить перерыва определяется параметром time_gap.
    Имеет смысл ставить time_gap больше 60.

    TODO: в исходных dat файлах есть информация - использовать ее?
    Хотя ее не всегда можно корректно использовать.
    """

    bounds = _get_bounds_chunks(df, time_gap=time_gap)
    parts = []

    for pair in bounds:
        left, right = pair
        start_row = df.loc[df["timestamp"] == left]
        end_row = df.loc[df["timestamp"] == right]
        parts.append(df[start_row.index[0] : end_row.index[0] + 1])

    return parts


def collect_dat(data_path: str = "", year: int = 2009) -> TecDataFrame:
    """Read all .dat files to TectDataFrame object
    from given folder with respect to filename template."""

    file_list = get_file_list(
        path=data_path, template=r"^\w{4,4}[G,R]\d\d_\d\d\d\.dat$"
    )

    tec_data = []

    for filename in tqdm.tqdm(file_list):
        name, _ = os.path.basename(filename).split(".")
        try:
            df = dat_to_df(filename=filename, year=year)
        except ValueError as e:
            print(f" Ошибка при обработке файла {name}. Файл пропущен.")
            print(e)
            continue

        tec_data.append(
            {
                "name": name,
                "df": df,
            }
        )

    return tec_data
