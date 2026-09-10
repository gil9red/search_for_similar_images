#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from pathlib import Path

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices

from showinfm import show_in_file_manager


def open_with_associated_app(file_path: str) -> None:
    absolute_path = os.path.abspath(file_path)

    if os.path.exists(absolute_path):
        file_url = QUrl.fromLocalFile(absolute_path)
        QDesktopServices.openUrl(file_url)


def explore(path: str | Path, select: bool = True) -> None:
    if isinstance(path, Path):
        path: str = str(path)

    if not os.path.exists(path):
        return

    if select:
        show_in_file_manager(path)
        return

    open_with_associated_app(path)
