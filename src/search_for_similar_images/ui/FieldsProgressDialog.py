#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import Any

from PyQt6.QtWidgets import QWidget, QProgressDialog, QLabel, QFormLayout
from PyQt6.QtCore import Qt


class KeyValueLabel(QLabel):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._field_by_row: dict[str, Any] = dict()
        self._layout = QFormLayout()
        self.setLayout(self._layout)

        self.setMinimumSize(200, 150)

    def setFields(self, fields: dict[str, Any]) -> None:
        while not self._layout.isEmpty():
            self._layout.takeAt(0)

        for label, field in self._field_by_row.values():
            label.hide()
            field.hide()

        for field_title, value in fields.items():
            value = str(value)

            if field_title in self._field_by_row:
                label_widget, field_widget = self._field_by_row[field_title]
                label_widget.show()
                field_widget.show()

            else:
                label_widget = QLabel(field_title + ":")
                font = label_widget.font()
                font.setBold(True)
                label_widget.setFont(font)

                field_widget = QLabel()
                self._field_by_row[field_title] = (label_widget, field_widget)

            field_widget.setText(value)

            self._layout.addRow(label_widget, field_widget)

    def sizeHint(self):
        return self._layout.sizeHint()


class FieldsProgressDialog(QProgressDialog):
    def __init__(
        self,
        minimum: int,
        maximum: int,
        window_title: str,
        label_text: str = "Operation in progress...",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setRange(minimum, maximum)
        self.setWindowTitle(window_title)

        self._label = KeyValueLabel(self)
        self.setLabel(self._label)

        self.setLabelText(label_text)

    def setFields(self, fields: dict[str, Any]) -> None:
        self._label.setFields(fields)

        # NOTE: Для вызова внутреннего ensureSizeIsAtLeastSizeHint, без которого не будет
        #       обновлен размер progress dialog.
        #       https://code.woboq.org/qt5/qtbase/src/widgets/dialogs/qprogressdialog.cpp.html#387
        self.setLabelText("")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtTest import QTest

    app = QApplication([])

    label = KeyValueLabel()
    label.setFields(
        {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
        }
    )
    label.show()

    QTest.qWait(2000)

    label.setFields(
        {
            "a": 1,
            "d": 4,
        }
    )

    QTest.qWait(2000)

    label.setFields(
        {
            "abc": 123,
            "x": 2**3,
        }
    )

    QTest.qWait(2000)

    app.exec()
