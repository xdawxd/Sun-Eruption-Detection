import datetime as dt
from logging import config
from pathlib import Path

import cv2 as cv
import numpy as np
from sunpy.io.jp2 import get_header

from sun_eruption_detection.consts import BASE_PATH, IMAGES_PATH, NARROWED_IMAGES_PATH
from sun_eruption_detection.sun_eruption_finder import SunEruptionFinder
from sun_eruption_detection.utils import read_sav_file

# if opencv autocomplete does not work export a system environment variable PYTHONPATH with cv2 directory path


def get_outside_pixels(circle_x: float, circle_y: float, radius: float, points) -> np.ndarray:
    points_array = np.squeeze(points)
    distances = np.sqrt((points_array[:, 0] - circle_x) ** 2 + (points_array[:, 1] - circle_y) ** 2)
    outside_indices = np.where(distances > radius)[0]
    return points_array[outside_indices]


def main():
    sun_eruption_finder = SunEruptionFinder()
    sun_eruption_finder.find()

    # img_path_1 = list(NARROWED_IMAGES_PATH.iterdir())[0]
    # img_1 = cv.imread(str(img_path_1))
    #
    # headers = get_header(str(img_path_1))[0]
    # sun_radius = headers["R_SUN"] - 400
    # x_img_center, y_img_center = headers["X0_MP"], headers["Y0_MP"]
    #
    # image_area_map = {}
    # min_area = 100
    # for idx, img_path in enumerate(list(NARROWED_IMAGES_PATH.iterdir())[1:]):
    #     img_2 = cv.imread(str(img_path))
    #
    #     subs_res = cv.subtract(img_1, img_2)  # image subtraction
    #     gray = cv.cvtColor(subs_res, cv.COLOR_BGR2GRAY)  # rgb -> greyscale
    #     thresh = cv.threshold(gray, 16, 255, cv.THRESH_BINARY)[1]  # threshold (obtain binary image)
    #
    #     contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # contour the thresholded image
    #     contours = contours[0] if len(contours) == 2 else contours[1]
    #
    #     max_area = max([cv.contourArea(contour) for contour in contours])
    #     min_area = (
    #         max_area // 2
    #     )  # Excluding smaller contoured areas. The scale of increase for this variable differs for each eruption case
    #     white_spots = []
    #     for contour in contours:
    #         area = cv.contourArea(contour)
    #         if area > min_area:
    #             cv.circle(
    #                 subs_res,
    #                 (int(x_img_center), int(y_img_center)),
    #                 int(sun_radius),
    #                 (255, 0, 0),
    #                 thickness=5,
    #             )
    #             image_area_map[area] = subs_res
    #             white_spots.append(contour)
    #
    #             coordinates = get_outside_pixels(x_img_center, y_img_center, sun_radius, contour)
    #
    #             if coordinates.any():
    #                 cv.drawContours(img_2, [np.expand_dims(coordinates, axis=1)], -1, (36, 255, 12), 4)
    #
    #             resized_img_2 = cv.resize(img_2, (1024, 1024), interpolation=cv.INTER_AREA)
    #             cv.imshow("image", resized_img_2)
    #             cv.waitKey(1)
    #
    #     print(f"White Dots count is: {len(white_spots)}, max_area: {max_area}, min_area: {min_area}, image: {idx+1}")


if __name__ == "__main__":
    config.fileConfig(BASE_PATH / "log.config")
    main()
