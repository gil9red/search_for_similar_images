#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt6.QtWidgets import QFormLayout, QDialog, QLabel, QLineEdit, QWidget
from PyQt6.QtGui import QIcon

from search_for_similar_images.third_party.explore__windows import explore
from search_for_similar_images.config import DIR_IMAGES


class ImageHashDetailsDialog(QDialog):
    def __init__(self, file_name: str, data: dict, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("ImageHash Details")

        self._layout = QFormLayout()

        value_widget = self._addRow("File name", file_name)
        value_widget.setToolTip(file_name)

        action_run = value_widget.addAction(
            QIcon(DIR_IMAGES + "/run_image.svg"),
            QLineEdit.ActionPosition.TrailingPosition,
        )
        action_run.triggered.connect(lambda: explore(value_widget.text(), select=False))

        action_view = value_widget.addAction(
            QIcon(DIR_IMAGES + "/view.svg"),
            QLineEdit.ActionPosition.TrailingPosition,
        )
        action_view.triggered.connect(lambda: explore(value_widget.text()))

        for k, v in data.items():
            self._addRow(k, v)

        self.setLayout(self._layout)

    def _addRow(self, key: str, value) -> QWidget:
        try:
            value = str(value)
        except Exception as e:
            value = f"<Error: {e}>"

        label_widget = QLabel(key + ":")
        font = label_widget.font()
        font.setBold(True)
        label_widget.setFont(font)

        value_widget = QLineEdit()
        value_widget.setReadOnly(True)
        value_widget.setText(value)
        value_widget.setStyleSheet(
            """
            QLineEdit {
                border: 0;
                background: transparent;
            }
            """
        )

        self._layout.addRow(label_widget, value_widget)

        return value_widget
