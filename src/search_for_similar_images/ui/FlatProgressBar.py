#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt6.QtWidgets import QProgressBar


class FlatProgressBar(QProgressBar):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        self.setTextVisible(False)
        self.setStyleSheet("""
            QProgressBar {
                background-color: rgba(128, 128, 128, 0.3);
                border: 0px solid gray;
                border-radius: 5px;
                max-height: 3px;
                margin-top: 5px;
                margin-bottom: 2px;
            }
            QProgressBar::chunk {
                background-color: gray;
            }
            """)

    def setValue(self, value: int) -> None:
        super().setValue(value)

        self.setToolTip(
            f"{self.value()} / {self.maximum()} ({self.value() / self.maximum():.1%})"
        )
