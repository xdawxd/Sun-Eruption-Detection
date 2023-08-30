import logging
from logging import config
from pathlib import Path

import cv2 as cv

from sun_eruption_detection.scripts.consts import BASE_PATH, IMAGES_PATH

VIDEOS_PATH: Path = BASE_PATH / "static" / "videos"


class ImagesToVideConverter:
    @classmethod
    def convert(cls) -> None:
        suffix = cls._get_new_file_suffix()
        out = cv.VideoWriter(
            str(VIDEOS_PATH / f"eruption{suffix}.avi"), cv.VideoWriter_fourcc(*"DIVX"), 5, (1024, 1024)
        )
        for image_path in IMAGES_PATH.iterdir():
            jp2 = cv.imread(str(image_path))
            resized_jp2 = cv.resize(jp2, (1024, 1024), interpolation=cv.INTER_AREA)
            out.write(resized_jp2)
            logging.info(f"{image_path.name} processed.")
        out.release()

    @staticmethod
    def _get_new_file_suffix() -> str:
        biggest_suffix = 0

        for video in VIDEOS_PATH.glob("**/*"):
            video_name = video.name
            if "_" in video_name:
                int_suffix = int(video_name.split("_")[1].split(".")[0])
                if biggest_suffix <= int_suffix:
                    biggest_suffix = int_suffix + 1
            else:
                biggest_suffix = 1

        if biggest_suffix == 0:
            return ""

        return f"_{biggest_suffix}"


if __name__ == "__main__":
    config.fileConfig(BASE_PATH / "log.config")
    ImagesToVideConverter.convert()
