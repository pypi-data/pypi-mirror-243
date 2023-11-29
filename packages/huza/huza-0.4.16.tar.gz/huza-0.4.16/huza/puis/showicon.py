# coding=utf-8
import re, os, time, codecs
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QApplication, QVBoxLayout, QLineEdit, QWidget, QHBoxLayout, \
    QLabel
from loguru import logger
from huza.base.dockview import DockView
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(581, 485)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


class ShowIcon_Form(Ui_Form, DockView):

    def setupUi(self, Form):
        self.form = Form
        super(ShowIcon_Form, self).setupUi(Form)
        self.load()
        self.connect()

    def add_tab_icon(self, j):
        qvbox = QVBoxLayout()
        qhbox = QHBoxLayout()
        label = QLabel()
        label.setText('搜索：')
        line = QLineEdit()
        line.setMaximumWidth(300)
        all_icon_names = list(getattr(self.iconlist, j)._icon_database.keys())
        icon_j = getattr(self.iconlist, j)
        icon_j.name = j
        line.textChanged.connect(self.itemChange)
        qhbox.addWidget(label)
        qhbox.addWidget(line)
        qhbox.addStretch()
        qvbox.addLayout(qhbox)
        listWidget = QListWidget()
        listWidget.all_icon_names = all_icon_names
        listWidget.icon_j = icon_j
        qvbox.addWidget(listWidget)
        listWidget.setIconSize(QSize(60, 60))
        listWidget.setResizeMode(QListWidget.Adjust)
        listWidget.setViewMode(QListWidget.IconMode)
        listWidget.setMovement(QListWidget.Static)
        listWidget.setSpacing(10)

        for i in all_icon_names:
            item = QListWidgetItem(getattr(getattr(self.iconlist, j), i), i)
            item.setToolTip(i)
            item.setSizeHint(QSize(80, 80))
            item._text = f'{j}.{i}'
            listWidget.addItem(item)
        listWidget.itemDoubleClicked.connect(self.click)
        return qvbox

    def itemChange(self, text):
        listWidget = self.tabWidget.currentWidget().findChild(QListWidget)
        all_icon_names = listWidget.all_icon_names
        icon_j = listWidget.icon_j
        listWidget.clear()
        if text.strip() == '':
            all_icon_names2 = all_icon_names
        else:
            all_icon_names2 = []
            for j1 in all_icon_names:
                if text.lower() in j1.lower():
                    all_icon_names2.append(j1)
        for i in all_icon_names2:
            item = QListWidgetItem(getattr(icon_j, i), i)
            item.setToolTip(i)
            item.setSizeHint(QSize(80, 80))
            item._text = f'{icon_j.name}.{i}'
            listWidget.addItem(item)

    def load(self):
        for j in list(self.iconlist._iconlist.keys()):
            qw = QWidget()
            self.tabWidget.addTab(qw, j)
        self.tab_widgetchanged(1)
        self.tabWidget.setCurrentIndex(1)

    def click(self, item):
        _text = item._text
        clipboard = QApplication.clipboard()
        clipboard.setText(_text)

    def tab_widgetchanged(self, index: int):
        tab = self.tabWidget.widget(index)
        if tab.layout() is None:
            text = self.tabWidget.tabText(index)
            lay = self.add_tab_icon(text)
            tab.setLayout(lay)

    def connect(self):
        self.tabWidget.currentChanged.connect(self.tab_widgetchanged)
