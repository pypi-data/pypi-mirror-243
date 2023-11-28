#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2022-11-17 10:08:10
LastEditors  : Kofi
LastEditTime : 2022-11-17 10:08:11
Description  : 组件函数
"""
from functools import partial
from PyQt5.QtCore import QRegExp, Qt, QSize
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QWidget,
)
from KofiPyQtHelper.enums.ComboboxValueType import ComboboxValueType
from KofiPyQtHelper.components.MatplotlibFigure import MatplotlibFigure
from KofiPyQtHelper.components.CustomGraphics import CustomGraphics
from KofiPyQtHelper.components.ImageView import ImageView
from KofiPyQtHelper.utils.Ui.component.TableHelper import TableHelper
from KofiPyQtHelper.utils.Ui.component.TreeHelper import TreeHelper
from KofiPyQtHelper.utils.Ui.component.ListviewHelper import ListviewHelper
from KofiPyQtHelper.utils.Ui.component.ValueHelper import ValueHelper


class ComponentHelper(TableHelper, TreeHelper, ListviewHelper, ValueHelper):
    def initHSplitter(self, parent, info):
        splitter = QSplitter(Qt.Horizontal)
        self.addToParentContainer(parent, splitter)
        return splitter

    def initVSplitter(self, parent, info):
        splitter = QSplitter(Qt.Vertical)
        self.addToParentContainer(parent, splitter)
        return splitter

    def initStretch(self, parent: QWidget, info):
        if type(parent) == QGridLayout:
            parent.addWidget(
                QWidget(),
                self.gridInfo[parent]["currentRow"],
                self.gridInfo[parent]["currentColumn"],
                1,
                int(info["value"]),
            )
            self.gridCalculate(parent)
        else:
            parent.addStretch(int(info["value"]))

    def initLabel(self, parent, info):
        Label = QLabel(info["label"])
        if "name" in info:
            Label.setObjectName(info["name"])
        parent.addWidget(Label)

    def initPixlabel(self, parent, info):
        pix = QPixmap(info["src"])
        label = QLabel()
        label.setPixmap(pix)
        if "name" in info:
            label.setObjectName(info["name"])
        if "maximumSize" in info:
            label.setMaximumSize(int(info["maximumSize"]), int(info["maximumSize"]))
        if "height" in info:
            label.setFixedHeight(int(info["height"]))
        label.setScaledContents(True)
        parent.addWidget(label)

    def initCustomgraphics(self, parent, info):
        vbox = self.initVbox(parent, info)
        customGraphics = CustomGraphics()
        self.components.append({info["name"]: customGraphics})

        buttons = QHBoxLayout()
        buttons.setProperty("class", "toolbar")
        buttons.setSpacing(0)

        home = QPushButton(QIcon("./styles/icons/首页.png"), "")
        home.setProperty("class", "btn")
        home.clicked.connect(customGraphics.resetView)
        buttons.addWidget(home)

        pan = QPushButton(QIcon("./styles/icons/全屏.png"), "")
        pan.setProperty("class", "btn")
        pan.clicked.connect(customGraphics.pan)
        buttons.addWidget(pan)

        save = QPushButton(QIcon("./styles/icons/保存.png"), "")
        save.setProperty("class", "btn")
        save.clicked.connect(customGraphics.saveImage)
        buttons.addWidget(save)

        buttons.addStretch(0)
        vbox.addLayout(buttons)
        vbox.addWidget(customGraphics)

    def initMatplotlib(self, parent, info):
        vbox = self.initVbox(parent, info)
        width = info["width"] if "width" in info else None
        height = info["height"] if "height" in info else None
        matplot = MatplotlibFigure(width=width, heigh=height)
        self.components.append({info["name"]: matplot})
        buttons = QHBoxLayout()
        buttons.setProperty("class", "toolbar")
        # buttons.setContentsMargins(0, 0, 0, 0)
        buttons.setSpacing(0)

        home = QPushButton(QIcon("./styles/icons/首页.png"), "")
        home.setProperty("class", "btn")
        home.clicked.connect(matplot.home)
        buttons.addWidget(home)

        pan = QPushButton(QIcon("./styles/icons/全屏.png"), "")
        pan.setProperty("class", "btn")
        pan.clicked.connect(matplot.pan)
        buttons.addWidget(pan)

        zoom = QPushButton(QIcon("./styles/icons/放大镜.png"), "")
        zoom.setProperty("class", "btn")
        zoom.clicked.connect(matplot.zoom)
        buttons.addWidget(zoom)

        save = QPushButton(QIcon("./styles/icons/保存.png"), "")
        save.setProperty("class", "btn")
        save.clicked.connect(matplot.save)
        buttons.addWidget(save)

        buttons.addStretch(0)

        vbox.addLayout(buttons)
        vbox.addWidget(matplot)

    def initPlaintext(self, parent, info):
        area = QPlainTextEdit()
        if "enable" in info:
            flag = info["enable"].lower() == "true"
            area.setEnabled(flag)
        self.components.append({info["name"]: area})
        self.variates[info["name"]] = area.toPlainText()
        if "value" in info:
            self.setPlainTextValue(area, info["value"])
        area.textChanged.connect(partial(self.plainTextKillFocus, info["name"], area))

        area.adjustSize()
        if "label" in info:
            self.parentAddWidget(
                parent,
                area,
                info["label"],
                labelWidth=None if "labelWidth" not in info else info["labelWidth"],
            )
        else:
            parent.addWidget(area)
        return area

    def initButton(self, parent: QWidget, info):
        if "icon" in info:
            bt = QPushButton(QIcon(info["icon"]), info["label"])
        else:
            bt = QPushButton(info["label"])

        if type(info["command"]).__name__ == "str":
            if "params" not in info:
                info["params"] = []
            info["params"].append({"name": "window", "value": self})
            if info["command"] == "close":
                commands = self.commands["close"]
            else:
                commands = partial(self.commands[info["command"]], info["params"])
            bt.clicked.connect(commands)
        else:
            bt.clicked.connect(info["command"])

        if "name" in info:
            self.components.append({info["name"]: bt})
        if hasattr(parent, "addWidget"):
            parent.addWidget(bt)
        elif hasattr(parent, "addItem"):
            parent.addItem(bt)

    def createButtonLayout(self, button_list, name):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        for bt in button_list:
            params = bt.get("params", [])
            params.append({"name": "variates", "value": name})
            params.append({"name": "window", "value": self})
            command = partial(self.commands[bt["command"]], params)
            button = QPushButton(bt["label"])
            button.clicked.connect(command)
            layout.addWidget(button)

        widget = QWidget()
        widget.setFixedWidth(120)
        widget.setLayout(layout)
        return widget

    def initTextbox(self, parent: QWidget, info):
        objInput = QLineEdit()
        if "validator" in info:
            if info["validator"] == "Int":
                objInput.setValidator(QIntValidator())
            elif info["validator"] == "Float":
                objInput.setValidator(QDoubleValidator())
            elif info["validator"] == "Reg":
                regexp = QRegExp(info["reg"])
                validator = QRegExpValidator(regexp)
                objInput.setValidator(validator)

        placeholder = (
            info["placeholder"] if "placeholder" in info else "请输入" + info["label"]
        )
        objInput.setPlaceholderText(placeholder)
        objInput.resize(200, 30)

        if "value" in info:
            self.setTextValue(objInput, info["value"])
        objInput.textChanged.connect(
            partial(self.textBoxEditKillFocus, info["name"], objInput)
        )
        self.components.append({info["name"]: objInput})
        self.variates[info["name"]] = objInput.text()

        if "enable" in info:
            objInput.setEnabled(bool(info["enable"]))

        self.parentAddWidget(
            parent,
            objInput,
            info["label"],
            labelWidth=None if "labelWidth" not in info else info["labelWidth"],
        )

    def initHidden(self, parent: QWidget, info):
        self.variates[info["name"]] = info["value"]

    def initCombobox(self, parent: QWidget, info):
        objInput = QComboBox()
        item_params = info.get("itemParams")
        item_command = info.get("itemCommand")

        if item_command:
            item_params.append({"name": "window", "value": self})
            info["items"] = self.commands[item_command](item_params)
            info["value"] = info.get("value", info["items"][0] if info["items"] else "")

        items = info.get("items", [])
        objInput.addItems(items)

        info_name = info["name"]
        info_valueType = info.get("valueType")
        self.items[info_name] = {"type": info_valueType, "data": items}
        objInput.currentIndexChanged.connect(
            partial(self.comboboxKillFocus, info, objInput)
        )
        self.components.append({info_name: objInput})

        info_value = info.get("value")
        if info_value is not None:
            self.setComboValue(objInput, info_valueType, items, info_value)
            self.variates[info_name] = info_value
        else:
            self.variates[info_name] = ""

        label_width = info.get("labelWidth")
        self.parentAddWidget(
            parent,
            objInput,
            info["label"],
            labelWidth=None if label_width is None else label_width,
        )

    def initColorcombo(self, parent: QWidget, info):
        objInput = QComboBox()
        colorList = QColor.colorNames()
        self.items[info["name"]] = {"type": info["valueType"], "data": colorList}
        for color in colorList:
            pix = QPixmap(QSize(70, 20))
            pix.fill(QColor(color))
            objInput.addItem(QIcon(pix), color)
            objInput.setIconSize(QSize(70, 20))
            objInput.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        objInput.currentIndexChanged.connect(
            partial(self.comboboxKillFocus, info, objInput)
        )
        self.components.append({info["name"]: objInput})

        if "value" in info:
            if info["value"] == 0:
                info["value"] = 7
            self.setComboValue(objInput, info["valueType"], colorList, info["value"])
            self.variates[info["name"]] = info["value"]
        else:
            self.variates[info["name"]] = ""

        self.parentAddWidget(
            parent,
            objInput,
            info["label"],
            labelWidth=None if "labelWidth" not in info else info["labelWidth"],
        )

    def parentAddWidget(self, parent, objInput, label, labelWidth):
        if type(parent) == QFormLayout:
            parent.addRow(label, objInput)
        else:
            current = QWidget()
            current_layout = QHBoxLayout()
            current_layout.setContentsMargins(5, 5, 5, 5)
            current.setLayout(current_layout)
            labelWidget = QLabel(label)
            if labelWidth == None:
                labelWidget.setFixedWidth(40)
            else:
                labelWidget.setFixedWidth(labelWidth)

            current_layout.addWidget(labelWidget)
            current_layout.addWidget(objInput)
            if type(parent) == QGridLayout:
                parent.addWidget(
                    current,
                    self.gridInfo[parent]["currentRow"],
                    self.gridInfo[parent]["currentColumn"],
                )
                self.gridCalculate(parent)
            else:
                parent.addWidget(current)

    def comboboxKillFocus(self, info, objInput: QComboBox):
        if info["valueType"] == ComboboxValueType.Val.value:
            current = objInput.currentText()
        else:
            current = objInput.currentIndex()

        self.variates[info["name"]] = current
        if "change" in info and info["change"] in self.commands:
            self.commands[info["change"]]()

    def textBoxEditKillFocus(self, name, objInput: QLineEdit):
        self.variates[name] = objInput.text()

    def plainTextKillFocus(self, name, objInput: QPlainTextEdit):
        self.variates[name] = objInput.toPlainText()

    def initImageview(self, parent: QWidget, info):
        objInput = ImageView()
        self.components.append({info["name"]: objInput})
        label_width = info.get("labelWidth")
        self.parentAddWidget(
            parent,
            objInput,
            info["label"],
            labelWidth=None if label_width is None else label_width,
        )
