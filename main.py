import os
from logging import config

import cv2 as cv
import numpy as np
from scipy.io import readsav

# if opencv autocomplete does not work export a system environment variable PYTHONPATH with cv2 directory path

BASE_DIR: str = os.path.dirname(__file__)
STATIC_FILES: str = os.path.join(BASE_DIR, "static")


def read_sav_file(path: str, verbose: bool = False) -> np.recarray:
    sav_content = readsav(path, verbose=verbose)
    return sav_content.erupt_str


def write_sav_to_file(path: str, file_name: str, sav_data: np.recarray) -> None:
    sav_data.tofile(os.path.join(path, file_name), sep=";")


if __name__ == "__main__":
    config.fileConfig(os.path.join(BASE_DIR, "log.config"))
    sav_path = os.path.join(STATIC_FILES, "erupt_str.sav")
    np_rec_array = read_sav_file(sav_path)

    jp2 = cv.imread(os.path.join(STATIC_FILES, "2014_01_08__03_44_37_54__SDO_AIA_AIA_171.jp2"), 0)
    cv.imshow("test", jp2)
    cv.waitKey(0)

    for name, value in zip(np_rec_array[0].dtype.names, np_rec_array[0]):
        print(f"{name} - {value.dtype.name}: {value}")
