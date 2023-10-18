import datetime as dt
import logging
from logging import config
from typing import Final

import click
import requests
from bs4 import BeautifulSoup

from sun_eruption_detection.consts import BASE_PATH, IMAGES_PATH
from sun_eruption_detection.error_handling.exceptions import InvalidEruptionDateTimeException


class SunImageScraper:
    _URL: str = "https://helioviewer.org/jp2/AIA"
    _DATE_PREFIX: Final[str] = "171"
    _DATETIME_FORMAT: str = "%Y/%m/%d %H:%M:%S"
    _IMAGE_DATETIME_FORMAT: str = "%Y_%m_%d__%H_%M_%S_%f"
    _REQUEST_TIMEOUT: Final[int] = 15

    def __init__(self, eruption_start: str, eruption_end: str):
        self._eruption_start = eruption_start
        self._eruption_end = eruption_end

        self._eruption_start_datetime = dt.datetime.strptime(self._eruption_start, self._DATETIME_FORMAT)
        self._eruption_end_datetime = dt.datetime.strptime(self._eruption_end, self._DATETIME_FORMAT)

    def scrape(self) -> None:
        urls = self._get_urls()

        for url in urls:
            request = requests.get(url, timeout=self._REQUEST_TIMEOUT)
            soup = BeautifulSoup(request.content, "html.parser")
            self._save_images(url, soup)

    def _save_images(self, url: str, soup: BeautifulSoup) -> None:
        for anchor in soup.find_all("a"):
            image_name = anchor.get("href")
            if self._is_eruption_in_date_range(image_name):
                logging.info(f"Downloaded {image_name}")
                with open(IMAGES_PATH / image_name, "wb") as file:
                    file.write(requests.get(f"{url}/{image_name}", stream=True, timeout=self._REQUEST_TIMEOUT).content)

    def _is_eruption_in_date_range(self, image_name: str) -> bool:
        try:
            image_datetime = dt.datetime.strptime("__".join(image_name.split("__")[:2]), self._IMAGE_DATETIME_FORMAT)
        except ValueError:
            return False

        if self._eruption_start_datetime < image_datetime < self._eruption_end_datetime:
            return True
        return False

    def _get_urls(self) -> list[str]:
        self._validate_eruption_date()
        return self._format_urls()

    def _format_urls(self) -> list[str]:
        date_format = self._DATETIME_FORMAT.split(" ")[0]
        if self._eruption_start_datetime.day != self._eruption_end_datetime.day:
            return [
                f"{self._URL}/{self._eruption_start_datetime.strftime(date_format)}/{self._DATE_PREFIX}",
                f"{self._URL}/{self._eruption_end_datetime.strftime(date_format)}/{self._DATE_PREFIX}",
            ]
        return [f"{self._URL}/{self._eruption_start_datetime.strftime(date_format)}/{self._DATE_PREFIX}"]

    def _validate_eruption_date(self) -> None:
        """
        Validate the passed date based on the available helioviewer directories and raise
          an exception if the date is invalid.
        """
        eruptive_catalogue_start_date = dt.datetime(2010, 6, 2)

        if (
            self._eruption_start_datetime < eruptive_catalogue_start_date
            or self._eruption_start_datetime > dt.datetime.now()
        ):
            raise InvalidEruptionDateTimeException(
                message=f"Invalid start datetime passed. Please check the {self._URL} for a valid datetime"
            )
        if (
            self._eruption_end_datetime < eruptive_catalogue_start_date
            or self._eruption_end_datetime > dt.datetime.now()
        ):
            raise InvalidEruptionDateTimeException(
                message=f"Invalid end datetime passed. Please check the {self._URL} for a valid datetime"
            )
        if self._eruption_end_datetime < self._eruption_start_datetime:
            raise InvalidEruptionDateTimeException(message="Invalid datetime passed. Start datetime is older than end")


@click.command()
@click.option("-s", "--start", help="Eruption start date (format: YYYY/mm/dd HH:MM:SS)")
@click.option("-e", "--end", help="Eruption end date (format: YYYY/mm/dd HH:MM:SS)")
def run_sun_image_scraper(start, end):
    sun_image_scraper = SunImageScraper(start, end)
    sun_image_scraper.scrape()


if __name__ == "__main__":
    config.fileConfig(BASE_PATH / "log.config")
    run_sun_image_scraper()
