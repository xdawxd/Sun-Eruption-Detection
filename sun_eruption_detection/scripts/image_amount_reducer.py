import datetime as dt
import shutil
from logging import config
from pathlib import Path

import numpy as np
from sunpy import time

from sun_eruption_detection.consts import BASE_PATH, NARROWED_IMAGES_PATH
from sun_eruption_detection.utils import read_sav_file

IMAGES_PATH: Path = BASE_PATH / "static" / "images"


class ImageAmountReducer:
    @classmethod
    def find_nearest_datetime_path(cls, sav_time: time) -> Path:
        image_data = {}
        for image_path in IMAGES_PATH.iterdir():
            image_dt = dt.datetime.strptime("__".join(image_path.name.split("__")[:2]), "%Y_%m_%d__%H_%M_%S_%f")
            image_timestamp = image_dt.replace(year=sav_time.year).timestamp()
            image_data[image_timestamp] = image_path

        return image_data[min(image_data.keys(), key=lambda ts: abs(ts - sav_time.timestamp()))]

    @classmethod
    def narrow_image_quantity(cls, sav_file_contents: np.recarray):
        for name, value in zip(sav_file_contents[0].dtype.names, sav_file_contents[0], strict=True):
            if name == "TIMES":
                for sav_time in value:
                    converted_sav_time = time.parse_time(sav_time, format="utime").to_datetime()
                    if converted_sav_time.year != 1970:
                        nearest_date_path = cls.find_nearest_datetime_path(converted_sav_time)
                        shutil.copyfile(nearest_date_path, f"{NARROWED_IMAGES_PATH / nearest_date_path.name}")


if __name__ == "__main__":
    config.fileConfig(BASE_PATH / "log.config")
    np_rec_array = read_sav_file()
    ImageAmountReducer.narrow_image_quantity(np_rec_array)  # adjust the image quantity from helioviewer to eruptivesun
