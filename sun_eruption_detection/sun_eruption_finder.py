from pathlib import Path

import numpy as np

from sun_eruption_detection.consts import NARROWED_IMAGES_PATH
import cv2 as cv
from sunpy.io.jp2 import get_header

from sun_eruption_detection.models import ImageHeaders


class SunEruptionFinder:
    def __init__(self):
        self._first_image_path: Path = self._eruption_images[0]
        self._headers = get_header(str(self._first_image_path))[0]
        self._image_area_map: dict = {}

    def find(self) -> None:
        first_image = cv.imread(str(self._first_image_path))
        for idx, img_path in enumerate(self._eruption_images[1:]):
            second_image = cv.imread(str(img_path))
            subtraction_result = cv.subtract(first_image, second_image)
            gray_scaled_image = cv.cvtColor(subtraction_result, cv.COLOR_BGR2GRAY)
            binary_image = cv.threshold(gray_scaled_image, 2, 255, cv.THRESH_BINARY)[1]

            contours = cv.findContours(binary_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            min_area, max_area = self._calculate_min_contour_area(contours)

            white_spots = self._draw_contours(contours, min_area, binary_image)  # second_image

            print(
                f"White Dots count is: {len(white_spots)}, max_area: {max_area}, min_area: {min_area}, image: {idx + 1}"
            )

    def _draw_contours(self, contours, min_area, second_image) -> list:
        white_spots = []
        for contour in contours:
            area = cv.contourArea(contour)
            if area > min_area:
                white_spots.append(contour)

                if (coordinates := self._get_outside_pixels(contour)).any():
                    cv.drawContours(second_image, [np.expand_dims(coordinates, axis=1)], -1, (36, 255, 12), 4)

                resized_img_2 = cv.resize(second_image, (1024, 1024), interpolation=cv.INTER_AREA)
                cv.imshow("image", resized_img_2)
                cv.waitKey(1)
        return white_spots

    def _get_outside_pixels(self, points: np.ndarray) -> np.ndarray:
        points_array = np.squeeze(points)
        distances = np.sqrt(
            (points_array[:, 0] - self._image_headers.image_center_y) ** 2
            + (points_array[:, 1] - self._image_headers.image_center_y) ** 2
        )
        outside_indices = np.where(distances > self._image_headers.sun_radius)[0]
        return points_array[outside_indices]

    @property
    def _image_headers(self) -> ImageHeaders:
        return ImageHeaders(
            sun_radius=self._headers["R_SUN"] - 400,
            image_center_x=self._headers["X0_MP"],
            image_center_y=self._headers["Y0_MP"],
        )

    @property
    def _eruption_images(self) -> list[Path]:
        return list(NARROWED_IMAGES_PATH.iterdir())

    @staticmethod
    def _calculate_min_contour_area(contours) -> tuple[float, float]:
        max_area = max([cv.contourArea(contour) for contour in contours])
        min_area = (
            max_area // 2
        )  # Excluding smaller contoured areas. The scale of increase for this variable differs for each eruption case
        return min_area, max_area
