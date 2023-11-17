from pathlib import Path

import numpy as np

from sun_eruption_detection.consts import NARROWED_IMAGES_PATH
import cv2 as cv
from sunpy.io.jp2 import get_header

from sun_eruption_detection.models import ImageHeaders

# TODO:
#  - Zapuscic algorytm na sekwencji obrazow np. 1 - 2 dni w celu przeanalizowania poprawnego klasyfikowania zdarzen jako erupcje
#  a nastepnie poprawic dzialanie algorytmu tak aby wykryc przemieszczanie sie pixeli np. oznaczanie obszaru bedacego wynikiem
#  progowania oraz sprawdzania pozycji tych pikseli
#  - Zastosowac filtr medianowy zamiast prostej operacji max_area // 2
class SunEruptionFinder:
    def __init__(self):
        self._first_image_path: Path = self._eruption_images[0]
        self._headers = get_header(str(self._first_image_path))[0]
        self._image_area_map: dict = {}

    def find(self) -> None:
        for idx in range(len(self._eruption_images) - 1):
            first_image = cv.imread(str(self._eruption_images[idx]))
            second_image = cv.imread(str(self._eruption_images[idx+1]))
            subtraction_result = cv.subtract(first_image, second_image)
            gray_scaled_image = cv.cvtColor(subtraction_result, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(gray_scaled_image, (5, 5), 0)
            binary_image = cv.threshold(blur, 4, 255, cv.THRESH_BINARY)[1]

            contours = cv.findContours(binary_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            min_area, max_area = self._calculate_min_contour_area(contours)

            white_spots = self._draw_contours(contours, min_area, second_image)  # second_image

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
                    cv.drawContours(second_image, [coordinates], -1, (36, 255, 12), 4)  # [np.expand_dims(coordinates, axis=1)]

                resized_img_2 = cv.resize(second_image, (1024, 1024), interpolation=cv.INTER_AREA)
                cv.imshow("image", resized_img_2)
                cv.waitKey(1)
        return white_spots

    # TODO -> przeanalizowaać sprawdzanie ruchu na podstawie dwóch okręgów ograniczających pewny obszar, a następnie
    #  sprawdzić jak szybko erupcja wychodzi poza obszar, bądź przemieszcza się od r1 do r2.
    def _get_outside_pixels(self, points: np.ndarray) -> np.ndarray:  # dodac okrag poza promieniem slonca
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
            max_area // 2  # filtr medianowy zamiast - maksymalny obszar // 2
        )  # Excluding smaller contoured areas. The scale of increase for this variable differs for each eruption case
        return min_area, max_area