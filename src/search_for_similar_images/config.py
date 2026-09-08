#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

from PyQt5.QtCore import QStandardPaths

from dotenv import load_dotenv, find_dotenv


BASE_DIR: Path

pyproject_path: str = find_dotenv("pyproject.toml")
if pyproject_path:
    BASE_DIR = Path(pyproject_path).parent
else:
    load_dotenv()
    BASE_DIR = Path.cwd()

DIR: Path = Path(__file__).resolve().parent

DB_FILE_NAME: str = str(BASE_DIR / "database.sqlite")

DIR_IMAGES: str = str(DIR / "images")

IMAGE_HASH_ALGO: list[str] = [
    "phash",
    "average_hash",
    "phash_simple",
    "dhash",
    "dhash_vertical",
    "whash",
    "colorhash",
]
DEFAULT_IMAGE_HASH_ALGO: str = IMAGE_HASH_ALGO[0]
DEFAULT_IMAGE_HASH_MAX_SCORE: int = 10

DEFAULT_SUFFIXES: str = "jpg,jpeg,png,bmp"

USER_PICTURES_DIR: str = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)[0]

ICON_WIDTH: int = 128
ICON_HEIGHT: int = 128

SETTINGS_FILE_NAME: str = str(BASE_DIR / "settings.ini")
