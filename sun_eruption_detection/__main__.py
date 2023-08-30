import os
from pathlib import Path
from logging import config

from math import acos
import cv2 as cv
import numpy as np
from scipy.io import readsav
import datetime as dt
import shutil

from sun_eruption_detection.scripts.images_to_video_converter import ImagesToVideConverter

# if opencv autocomplete does not work export a system environment variable PYTHONPATH with cv2 directory path

BASE_PATH: Path = Path(__file__).parent
SAV_FILES: Path = BASE_PATH / "static" / "sav_files"
IMAGES_PATH: Path = BASE_PATH / "static" / "images"
NARROWED_IMAGES_PATH: Path = BASE_PATH / "static" / "narrowed_images"
MARKED_IMAGES_PATH: Path = BASE_PATH / "static" / "marked_images"


def read_sav_file(path: Path, verbose: bool = False) -> np.recarray:
    sav_content = readsav(str(path.absolute()), verbose=verbose)
    return sav_content.erupt_str


def write_sav_to_file(path: Path, file_name: str, sav_data: np.recarray) -> None:
    sav_data.tofile(path / file_name, sep=";")


def find_nearest_datetime_path(sav_time: dt.datetime) -> Path:
    image_data = {}
    for image_path in IMAGES_PATH.iterdir():
        image_dt = dt.datetime.strptime("__".join(image_path.name.split("__")[:2]), "%Y_%m_%d__%H_%M_%S_%f")
        image_timestamp = image_dt.replace(year=sav_time.year).timestamp()
        image_data[image_timestamp] = image_path

    return image_data[min(image_data.keys(), key=lambda ts: abs(ts - sav_time.timestamp()))]


def get_image_path_by_date(image_dt: dt.datetime) -> Path:
    return IMAGES_PATH / f"{image_dt.strftime('%Y_%m_%d__%H_%M_%S_%f')}_SDO_AIA_AIA_171.jp2"


def asec(x):
    return 1/acos(x)


def narrow_image_quantity(np_rec_array: np.recarray):
    for name, value in zip(np_rec_array[0].dtype.names, np_rec_array[0], strict=True):
        if name == "TIMES":
            for sav_time in value:
                converted_sav_time = dt.datetime.fromtimestamp(sav_time) - dt.timedelta(hours=1)
                if converted_sav_time.year != 1970:
                    nearest_date_path = find_nearest_datetime_path(converted_sav_time)
                    shutil.copyfile(nearest_date_path, f"{NARROWED_IMAGES_PATH / nearest_date_path.name}")


def main():
    np_rec_array = read_sav_file(SAV_FILES / "erupt_str.sav")

    # TODO -> why 1 hour has to be subtracted + year is 2005 for 2014, 2006 for 2015
    t_start = dt.datetime.fromtimestamp(np_rec_array[0][1]) - dt.timedelta(hours=1)
    t_peak = t_end = dt.datetime.fromtimestamp(np_rec_array[0][3]) - dt.timedelta(hours=1)
    t_end = dt.datetime.fromtimestamp(np_rec_array[0][2]) - dt.timedelta(hours=1)

    # TODO -> the number of images downloaded should be reduced to n_points based on the time that the image was taken
    n_points = np_rec_array[0][6]

    x_start, y_start = np_rec_array[0][12], np_rec_array[0][15]
    # ---------------------------------------------------------
    # narrow_image_quantity(np_rec_array) # adjust the image quantity from heliover to eruptivesun

    x_center = np_rec_array[0]["X_CENTER"]
    y_center = np_rec_array[0]["Y_CENTER"]

    x_center = x_center[x_center != 0]
    y_center = y_center[y_center != 0]

    for image_path, x, y in zip(NARROWED_IMAGES_PATH.iterdir(), x_center, y_center, strict=True):
        jp2 = cv.imread(str(image_path))
        resized_jp2 = cv.resize(jp2, (3000, 3000), interpolation=cv.INTER_AREA)

        dimensions = resized_jp2.shape
        img_center_x, img_center_y = dimensions[1]//2, dimensions[0]//2

        new_x, new_y = img_center_x + int(x), img_center_y - int(y)
        print(f"x: {x}, y: {y}")  # , asec of x: {asec(x)} asec of y: {asec(y)}
        # TODO -> why 125 had to be added to adjust the event position?
        cv.circle(resized_jp2, (new_x + 125, new_y), 100, (255, 0, 0), thickness=5)
        resized_jp2_1 = cv.resize(resized_jp2, (1024, 1024), interpolation=cv.INTER_AREA)

        # cv.imshow("Sun Eruption", resized_jp2_1)
        # cv.waitKey(0)
        os.chdir(MARKED_IMAGES_PATH)
        cv.imwrite(image_path.name, resized_jp2)


if __name__ == "__main__":
    config.fileConfig(BASE_PATH / "log.config")
    main()
