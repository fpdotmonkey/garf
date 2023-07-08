#!/usr/bin/env python3

import os
from typing import Iterable

from PIL import Image


PANEL_OUTPUT = "./panels/"
FILE_EXT = ".gif"


def main():
    create_output_dir()
    with os.scandir(".") as decades:
        for decade in decades:
            if not decade.is_dir() or decade.name == "panels":
                continue
            with os.scandir(decade.path) as years:
                for year in years:
                    if not year.is_dir():
                        continue
                    with os.scandir(year.path) as comics:
                        generate_panels(comics)


def create_output_dir():
    os.makedirs(os.path.join(PANEL_OUTPUT, "0"), exist_ok=True)
    os.makedirs(os.path.join(PANEL_OUTPUT, "1"), exist_ok=True)
    os.makedirs(os.path.join(PANEL_OUTPUT, "2"), exist_ok=True)


def generate_panels(comics: Iterable) -> None:
    slice_points = (418, 784)
    for comic in comics:
        image = Image.open(comic.path)
        width, height = image.size
        if height / width > 1 / 2:
            continue
        image.crop((0, 0, slice_points[0], height)).save(
            os.path.join(PANEL_OUTPUT, "0", comic.name)
        )
        image.crop((slice_points[0], 0, slice_points[1], height)).save(
            os.path.join(PANEL_OUTPUT, "1", comic.name)
        )
        image.crop((slice_points[1], 0, width, height)).save(
            os.path.join(PANEL_OUTPUT, "2", comic.name)
        )


if __name__ == "__main__":
    main()
