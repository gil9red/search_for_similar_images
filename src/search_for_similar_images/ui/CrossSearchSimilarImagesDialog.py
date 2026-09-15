#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import itertools
from collections import defaultdict

from PyQt6.QtWidgets import (
    QWidget,
    QDialog,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QProgressBar,
    QHeaderView,
    QToolBar,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QThread

from imagehash import ImageHash

from search_for_similar_images.config import DIR_IMAGES
from search_for_similar_images.utils import explore


class CrossSearchSimilarImagesThread(QThread):
    about_found_similars = pyqtSignal(str, list)

    def __init__(
        self,
        image_by_hashes: dict[str, dict[str, ImageHash | None]] | None = None,
        hash_algo: str | None = None,
        max_score: int | None = None,
    ) -> None:
        super().__init__()

        self.image_by_hashes = image_by_hashes
        self.hash_algo = hash_algo
        self.max_score = max_score

    def run(self) -> None:
        img_by_hash: dict[str, ImageHash | None] = {
            file_name: hashes[self.hash_algo]
            for file_name, hashes in self.image_by_hashes.items()
        }

        file_name_by_similars: dict[str, list[tuple[str, int]]] = defaultdict(list)
        for img_hash_1, img_hash_2 in itertools.product(img_by_hash.items(), repeat=2):
            if img_hash_1 == img_hash_2:
                continue

            file_name_1, hash_img_1 = img_hash_1
            file_name_2, hash_img_2 = img_hash_2

            score: int = int(hash_img_1 - hash_img_2)
            if score > self.max_score:
                continue

            file_name_by_similars[file_name_1].append((file_name_2, score))

        # Обратная сортировка по количеству элементов, а названия элементов сортируются по возрастанию
        items: list[tuple[str, list[tuple[str, int]]]] = sorted(
            file_name_by_similars.items(),
            key=lambda x: (-len(x[1]), x[0]),
        )
        for file_name, similars in items:
            if not similars:
                continue

            self.about_found_similars.emit(file_name, similars)


class CrossSearchSimilarImagesDialog(QDialog):
    itemDoubleClicked = pyqtSignal(str)

    window_title = "Cross search similar images"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle(self.window_title)
        self.resize(600, 600)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["FILE NAME", "SCORE"])
        self.tree_widget.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.tree_widget.header().resizeSection(0, 450)
        self.tree_widget.header().resizeSection(1, 75)
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setExpandsOnDoubleClick(False)
        self.tree_widget.itemClicked.connect(self._update_states)
        self.tree_widget.itemDoubleClicked.connect(
            lambda item, _: self.itemDoubleClicked.emit(
                item.data(0, Qt.ItemDataRole.UserRole)
            )
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

        self.thread = CrossSearchSimilarImagesThread()
        self.thread.started.connect(lambda: self.progress_bar.show())
        self.thread.finished.connect(lambda: self.progress_bar.hide())
        self.thread.about_found_similars.connect(self._on_about_found_similars)

        self.tool_bar = QToolBar("General")
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.action_select_image = self.tool_bar.addAction(
            QIcon(DIR_IMAGES + "/image.svg"),
            "Select image in explorer",
            self.select_image_file,
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tool_bar)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.tree_widget)
        self.setLayout(layout)

        self._update_states()

    def _update_states(self) -> None:
        item: QTreeWidgetItem | None = self.tree_widget.currentItem()
        self.action_select_image.setEnabled(item is not None)

    def _on_about_found_similars(
        self,
        file_name: str,
        similars: list[tuple[str, int]],
    ) -> None:
        item = QTreeWidgetItem([f"{file_name} ({len(similars)})"])
        item.setData(0, Qt.ItemDataRole.UserRole, file_name)

        self.tree_widget.addTopLevelItem(item)

        for file_name, score in similars:
            child = QTreeWidgetItem([file_name, str(score)])
            child.setData(0, Qt.ItemDataRole.UserRole, file_name)
            item.addChild(child)

    def select_image_file(self) -> None:
        item: QTreeWidgetItem | None = self.tree_widget.currentItem()
        if not item:
            return

        file_name: str = item.data(0, Qt.ItemDataRole.UserRole)
        if not file_name:
            return

        explore(file_name)

    def start(
        self,
        image_by_hashes: dict[str, dict[str, ImageHash | None]],
        hash_algo: str,
        max_score: int,
    ) -> None:
        self.setWindowTitle(
            f"{self.window_title}. hash_algo={hash_algo} max_score={max_score}"
        )
        self.tree_widget.clear()

        self.thread.image_by_hashes = image_by_hashes
        self.thread.hash_algo = hash_algo
        self.thread.max_score = max_score
        self.thread.start()

        self.show()
