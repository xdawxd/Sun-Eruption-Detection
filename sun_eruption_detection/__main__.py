from logging import config
from time import sleep

import numpy as np


from sun_eruption_detection.consts import BASE_PATH, NARROWED_IMAGES_PATH
import cv2 as cv
from matplotlib import pyplot as plt
from sun_eruption_detection.sun_eruption_finder import SunEruptionFinder
from sun_eruption_detection.utils import read_sav_file

# if opencv autocomplete does not work export a system environment variable PYTHONPATH with cv2 directory path


def get_outside_pixels(circle_x: float, circle_y: float, radius: float, points) -> np.ndarray:
    points_array = np.squeeze(points)
    distances = np.sqrt((points_array[:, 0] - circle_x) ** 2 + (points_array[:, 1] - circle_y) ** 2)
    outside_indices = np.where(distances > radius)[0]
    return points_array[outside_indices]


def main():
    # image_paths = list(NARROWED_IMAGES_PATH.iterdir())
    # for idx in range(len(image_paths) - 1):
    #     img1 = cv.imread(str(image_paths[idx]), cv.IMREAD_GRAYSCALE)
    #     img2 = cv.imread(str(image_paths[idx+1]), cv.IMREAD_GRAYSCALE)
    #     img = cv.subtract(img1, img2)
    #     # img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #     img = cv.GaussianBlur(img, (5, 5), 0)
    #     canny = cv.Canny(img, threshold1=5, threshold2=20)
    #     plt.hist(canny.ravel(), 256, [0, 256])
    #     plt.show()
    #     sleep(1)

        # ret, th1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
        # th2 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
        # th3 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
        # titles = ['Original Image', 'Global Thresholding (v = 127)',
        #           'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
        # images = [img, th1, th2, th3]
        # for i in range(4):
        #     plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
        #     plt.title(titles[i])
        #     plt.xticks([]), plt.yticks([])
        # plt.show()
        # break


    sun_eruption_finder = SunEruptionFinder()
    sun_eruption_finder.find()


if __name__ == "__main__":
    config.fileConfig(BASE_PATH / "log.config")
    main()
