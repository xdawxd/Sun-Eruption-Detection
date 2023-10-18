import datetime as dt
from logging import config
from pathlib import Path

import cv2 as cv
import numpy as np
from sunpy.io.jp2 import get_header

from sun_eruption_detection.consts import BASE_PATH, IMAGES_PATH, NARROWED_IMAGES_PATH
from sun_eruption_detection.utils import read_sav_file

# if opencv autocomplete does not work export a system environment variable PYTHONPATH with cv2 directory path


def get_image_path_by_date(image_dt: dt.datetime) -> Path:
    return IMAGES_PATH / f"{image_dt.strftime('%Y_%m_%d__%H_%M_%S_%f')}_SDO_AIA_AIA_171.jp2"


def find_white_areas():
    img_path_1 = list(NARROWED_IMAGES_PATH.iterdir())[0]
    img_path_2 = list(NARROWED_IMAGES_PATH.iterdir())[15]

    img_1 = cv.imread(str(img_path_1))
    img_2 = cv.imread(str(img_path_2))

    subs_res = cv.subtract(img_1, img_2)
    gray = cv.cvtColor(subs_res, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 16, 255, cv.THRESH_BINARY)[1]

    cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    min_area = 0.1  # 15000
    white_dots = []
    for c in cnts:
        area = cv.contourArea(c)
        if area > min_area:
            cv.drawContours(subs_res, [c], -1, (36, 255, 12), 2)
            white_dots.append(c)

    print("White Dots count is:", len(white_dots))
    resized_img_1 = cv.resize(img_1, (768, 768), interpolation=cv.INTER_AREA)
    resized_img_2 = cv.resize(img_2, (768, 768), interpolation=cv.INTER_AREA)
    resized_subs_res = cv.resize(subs_res, (768, 768), interpolation=cv.INTER_AREA)
    horizontal_joined_images = np.concatenate((resized_img_1, resized_img_2, resized_subs_res), axis=1)
    cv.imshow("images", horizontal_joined_images)
    cv.waitKey()


def get_outside_pixels(circle_x: float, circle_y: float, radius: float, points):
    points_array = np.squeeze(points)
    distances = np.sqrt((points_array[:, 0] - circle_x) ** 2 + (points_array[:, 1] - circle_y) ** 2)
    outside_indices = np.where(distances > radius)[0]
    return points_array[outside_indices]


def main():
    np_rec_array = read_sav_file()  # noqa

    img_path_1 = list(NARROWED_IMAGES_PATH.iterdir())[0]
    img_1 = cv.imread(str(img_path_1))

    headers = get_header(str(img_path_1))[0]
    sun_radius = headers["R_SUN"]
    x_img_center, y_img_center = headers["X0_MP"], headers["Y0_MP"]

    image_area_map = {}
    min_area = 500
    for idx, img_path in enumerate(NARROWED_IMAGES_PATH.iterdir()):
        img_2 = cv.imread(str(img_path))

        subs_res = cv.subtract(img_1, img_2)  # image subtraction
        gray = cv.cvtColor(subs_res, cv.COLOR_BGR2GRAY)  # rgb -> greyscale
        thresh = cv.threshold(gray, 16, 255, cv.THRESH_BINARY)[1]  # threshold (obtain binary image)

        contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # contour the thresholded image
        contours = contours[0] if len(contours) == 2 else contours[1]

        # min_area += 500  # 15000
        white_dots = []
        for contour in contours:
            area = cv.contourArea(contour)
            if area > min_area:
                cv.circle(
                    subs_res,
                    (int(x_img_center), int(y_img_center)),
                    int(sun_radius) - 400,
                    (255, 0, 0),
                    thickness=5,
                )
                image_area_map[area] = subs_res
                white_dots.append(contour)

                coordinates = get_outside_pixels(x_img_center, y_img_center, sun_radius, contour)

                if coordinates.any():
                    cv.drawContours(subs_res, [np.expand_dims(coordinates, axis=1)], -1, (36, 255, 12), 4)

                resized_subs_res = cv.resize(subs_res, (1024, 1024), interpolation=cv.INTER_AREA)
                cv.imshow("image", resized_subs_res)
                cv.waitKey(1)

        print(f"White Dots count is:, {len(white_dots)}, min area: {min_area}, image: {idx}")
        # resized_subs_res = cv.resize(subs_res, (128, 128), interpolation=cv.INTER_AREA)
        #
        # images_list.append(resized_subs_res)

    # biggest_area = max(image_area_map.keys())
    #
    # cv.circle(
    #     image_area_map[biggest_area],
    #     (int(x_img_center), int(y_img_center)),
    #     int(sun_radius) - 400,
    #     (255, 0, 0),
    #     thickness=5,
    # )
    #
    # resized_img_1 = cv.resize(image_area_map[biggest_area], (2048, 2048), interpolation=cv.INTER_AREA)
    # cv.imshow("image", resized_img_1)
    # cv.waitKey(0)


if __name__ == "__main__":
    config.fileConfig(BASE_PATH / "log.config")
    main()
