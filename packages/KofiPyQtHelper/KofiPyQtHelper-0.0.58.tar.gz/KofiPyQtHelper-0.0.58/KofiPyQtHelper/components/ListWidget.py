#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-11-22 17:36:51
LastEditors  : Kofi
LastEditTime : 2023-11-22 17:37:56
Description  : 
"""
from PyQt5.QtWidgets import QListWidget, QWidget


class ListWidget(QListWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.itemClicked.connect(self.clicked)
        self.special_item_callbacks = {}

    def clicked(self, item):
        callback = getattr(item, "callback", None)
        if callback:
            callback()
