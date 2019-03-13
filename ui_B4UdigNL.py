# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\diethard\Documents\ontwikkeling\b4udignl\B4UdigNL.ui'
#
# Created: Wed Nov 21 16:35:54 2018
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from qgis.PyQt import QtCore, QtGui
from qgis.gui import QgsColorButton

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_B4UdigNL(object):
    def setupUi(self, B4UdigNL):
        B4UdigNL.setObjectName(_fromUtf8("B4UdigNL"))
        B4UdigNL.resize(324, 432)
        B4UdigNL.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.verticalLayout = QtGui.QVBoxLayout(B4UdigNL)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(B4UdigNL)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.messageTab = QtGui.QWidget()
        self.messageTab.setObjectName(_fromUtf8("messageTab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.messageTab)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.messageBox = QtGui.QGroupBox(self.messageTab)
        self.messageBox.setObjectName(_fromUtf8("messageBox"))
        self.gridLayout = QtGui.QGridLayout(self.messageBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.openMsgButton = QtGui.QPushButton(self.messageBox)
        self.openMsgButton.setObjectName(_fromUtf8("openMsgButton"))
        self.horizontalLayout.addWidget(self.openMsgButton)
        self.openArchiveButton = QtGui.QPushButton(self.messageBox)
        self.openArchiveButton.setObjectName(_fromUtf8("openArchiveButton"))
        self.horizontalLayout.addWidget(self.openArchiveButton)
        spacerItem = QtGui.QSpacerItem(68, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.msgListWidget = QtGui.QListWidget(self.messageBox)
        self.msgListWidget.setMinimumSize(QtCore.QSize(100, 40))
        self.msgListWidget.setMaximumSize(QtCore.QSize(16777215, 60))
        self.msgListWidget.setObjectName(_fromUtf8("msgListWidget"))
        self.gridLayout.addWidget(self.msgListWidget, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gotoButton = QtGui.QPushButton(self.messageBox)
        self.gotoButton.setObjectName(_fromUtf8("gotoButton"))
        self.horizontalLayout_2.addWidget(self.gotoButton)
        self.bestScaleButton = QtGui.QPushButton(self.messageBox)
        self.bestScaleButton.setObjectName(_fromUtf8("bestScaleButton"))
        self.horizontalLayout_2.addWidget(self.bestScaleButton)
        self.removeMsgButton = QtGui.QPushButton(self.messageBox)
        self.removeMsgButton.setObjectName(_fromUtf8("removeMsgButton"))
        self.horizontalLayout_2.addWidget(self.removeMsgButton)
        spacerItem1 = QtGui.QSpacerItem(78, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.messageBox)
        self.additionsBox = QtGui.QGroupBox(self.messageTab)
        self.additionsBox.setMaximumSize(QtCore.QSize(16777215, 300))
        self.additionsBox.setObjectName(_fromUtf8("additionsBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.additionsBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.treeWidget = QtGui.QTreeWidget(self.additionsBox)
        self.treeWidget.setMinimumSize(QtCore.QSize(100, 100))
        self.treeWidget.setMaximumSize(QtCore.QSize(16777215, 250))
        self.treeWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout_2.addWidget(self.treeWidget, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.openDocButton = QtGui.QPushButton(self.additionsBox)
        self.openDocButton.setObjectName(_fromUtf8("openDocButton"))
        self.horizontalLayout_3.addWidget(self.openDocButton)
        spacerItem2 = QtGui.QSpacerItem(168, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.additionsBox)
        spacerItem3 = QtGui.QSpacerItem(17, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.saveButton = QtGui.QPushButton(self.messageTab)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_4.addWidget(self.saveButton)
        spacerItem4 = QtGui.QSpacerItem(13, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.helpButton = QtGui.QPushButton(self.messageTab)
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.horizontalLayout_4.addWidget(self.helpButton)
        self.closeButton = QtGui.QPushButton(self.messageTab)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout_4.addWidget(self.closeButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.tabWidget.addTab(self.messageTab, _fromUtf8(""))
        self.ThemesTab = QtGui.QWidget()
        self.ThemesTab.setObjectName(_fromUtf8("ThemesTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.ThemesTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.mColorButton = QgsColorButton(self.ThemesTab)
        self.mColorButton.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton.setAcceptLiveUpdates(False)
        self.mColorButton.setColor(QtGui.QColor(0, 255, 0))
        self.mColorButton.setObjectName(_fromUtf8("mColorButton"))
        self.horizontalLayout_5.addWidget(self.mColorButton)
        self.checkBoxData = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxData.setTristate(True)
        self.checkBoxData.setObjectName(_fromUtf8("checkBoxData"))
        self.horizontalLayout_5.addWidget(self.checkBoxData)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.refreshButton = QtGui.QPushButton(self.ThemesTab)
        self.refreshButton.setObjectName(_fromUtf8("refreshButton"))
        self.gridLayout_3.addWidget(self.refreshButton, 0, 1, 2, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.mColorButton_2 = QgsColorButton(self.ThemesTab)
        self.mColorButton_2.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_2.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_2.setAcceptLiveUpdates(False)
        self.mColorButton_2.setColor(QtGui.QColor(255, 215, 80))
        self.mColorButton_2.setObjectName(_fromUtf8("mColorButton_2"))
        self.horizontalLayout_6.addWidget(self.mColorButton_2)
        self.checkBoxGas_low = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxGas_low.setTristate(True)
        self.checkBoxGas_low.setObjectName(_fromUtf8("checkBoxGas_low"))
        self.horizontalLayout_6.addWidget(self.checkBoxGas_low)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.mColorButton_3 = QgsColorButton(self.ThemesTab)
        self.mColorButton_3.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_3.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_3.setAcceptLiveUpdates(False)
        self.mColorButton_3.setColor(QtGui.QColor(255, 175, 60))
        self.mColorButton_3.setObjectName(_fromUtf8("mColorButton_3"))
        self.horizontalLayout_7.addWidget(self.mColorButton_3)
        self.checkBoxGas_high = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxGas_high.setTristate(True)
        self.checkBoxGas_high.setObjectName(_fromUtf8("checkBoxGas_high"))
        self.horizontalLayout_7.addWidget(self.checkBoxGas_high)
        self.gridLayout_3.addLayout(self.horizontalLayout_7, 2, 0, 1, 1)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.mColorButton_4 = QgsColorButton(self.ThemesTab)
        self.mColorButton_4.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_4.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_4.setAcceptLiveUpdates(False)
        self.mColorButton_4.setColor(QtGui.QColor(255, 127, 0))
        self.mColorButton_4.setObjectName(_fromUtf8("mColorButton_4"))
        self.horizontalLayout_8.addWidget(self.mColorButton_4)
        self.checkBoxDanger = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxDanger.setTristate(True)
        self.checkBoxDanger.setObjectName(_fromUtf8("checkBoxDanger"))
        self.horizontalLayout_8.addWidget(self.checkBoxDanger)
        self.gridLayout_3.addLayout(self.horizontalLayout_8, 3, 0, 1, 2)
        self.horizontalLayout_20 = QtGui.QHBoxLayout()
        self.horizontalLayout_20.setObjectName(_fromUtf8("horizontalLayout_20"))
        self.mColorButton_8 = QgsColorButton(self.ThemesTab)
        self.mColorButton_8.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_8.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_8.setAcceptLiveUpdates(False)
        self.mColorButton_8.setColor(QtGui.QColor(255, 0, 0))
        self.mColorButton_8.setObjectName(_fromUtf8("mColorButton_8"))
        self.horizontalLayout_20.addWidget(self.mColorButton_8)
        self.checkBoxElec_land = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxElec_land.setTristate(True)
        self.checkBoxElec_land.setObjectName(_fromUtf8("checkBoxElec_land"))
        self.horizontalLayout_20.addWidget(self.checkBoxElec_land)
        self.gridLayout_3.addLayout(self.horizontalLayout_20, 4, 0, 1, 2)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.mColorButton_7 = QgsColorButton(self.ThemesTab)
        self.mColorButton_7.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_7.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_7.setAcceptLiveUpdates(False)
        self.mColorButton_7.setColor(QtGui.QColor(255, 0, 0))
        self.mColorButton_7.setObjectName(_fromUtf8("mColorButton_7"))
        self.horizontalLayout_11.addWidget(self.mColorButton_7)
        self.checkBoxElec_high = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxElec_high.setTristate(True)
        self.checkBoxElec_high.setObjectName(_fromUtf8("checkBoxElec_high"))
        self.horizontalLayout_11.addWidget(self.checkBoxElec_high)
        self.gridLayout_3.addLayout(self.horizontalLayout_11, 5, 0, 1, 1)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.mColorButton_6 = QgsColorButton(self.ThemesTab)
        self.mColorButton_6.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_6.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_6.setAcceptLiveUpdates(False)
        self.mColorButton_6.setColor(QtGui.QColor(200, 0, 0))
        self.mColorButton_6.setObjectName(_fromUtf8("mColorButton_6"))
        self.horizontalLayout_10.addWidget(self.mColorButton_6)
        self.checkBoxElec_mid = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxElec_mid.setTristate(True)
        self.checkBoxElec_mid.setObjectName(_fromUtf8("checkBoxElec_mid"))
        self.horizontalLayout_10.addWidget(self.checkBoxElec_mid)
        self.gridLayout_3.addLayout(self.horizontalLayout_10, 6, 0, 1, 2)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.mColorButton_5 = QgsColorButton(self.ThemesTab)
        self.mColorButton_5.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_5.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_5.setColor(QtGui.QColor(150, 0, 0))
        self.mColorButton_5.setObjectName(_fromUtf8("mColorButton_5"))
        self.horizontalLayout_9.addWidget(self.mColorButton_5)
        self.checkBoxElec_low = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxElec_low.setTristate(True)
        self.checkBoxElec_low.setObjectName(_fromUtf8("checkBoxElec_low"))
        self.horizontalLayout_9.addWidget(self.checkBoxElec_low)
        self.gridLayout_3.addLayout(self.horizontalLayout_9, 7, 0, 1, 1)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.mColorButton_13 = QgsColorButton(self.ThemesTab)
        self.mColorButton_13.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_13.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_13.setAcceptLiveUpdates(False)
        self.mColorButton_13.setColor(QtGui.QColor(182, 74, 0))
        self.mColorButton_13.setObjectName(_fromUtf8("mColorButton_13"))
        self.horizontalLayout_16.addWidget(self.mColorButton_13)
        self.checkBoxChemical = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxChemical.setTristate(True)
        self.checkBoxChemical.setObjectName(_fromUtf8("checkBoxChemical"))
        self.horizontalLayout_16.addWidget(self.checkBoxChemical)
        self.gridLayout_3.addLayout(self.horizontalLayout_16, 8, 0, 1, 1)
        self.vectorCheckBox = QtGui.QCheckBox(self.ThemesTab)
        self.vectorCheckBox.setObjectName(_fromUtf8("vectorCheckBox"))
        self.gridLayout_3.addWidget(self.vectorCheckBox, 8, 1, 1, 1)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.mColorButton_9 = QgsColorButton(self.ThemesTab)
        self.mColorButton_9.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_9.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_9.setColor(QtGui.QColor(186, 56, 168))
        self.mColorButton_9.setObjectName(_fromUtf8("mColorButton_9"))
        self.horizontalLayout_12.addWidget(self.mColorButton_9)
        self.checkBoxSewer_free = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxSewer_free.setTristate(True)
        self.checkBoxSewer_free.setObjectName(_fromUtf8("checkBoxSewer_free"))
        self.horizontalLayout_12.addWidget(self.checkBoxSewer_free)
        self.gridLayout_3.addLayout(self.horizontalLayout_12, 9, 0, 1, 1)
        self.rasterCheckBox = QtGui.QCheckBox(self.ThemesTab)
        self.rasterCheckBox.setEnabled(True)
        self.rasterCheckBox.setObjectName(_fromUtf8("rasterCheckBox"))
        self.gridLayout_3.addWidget(self.rasterCheckBox, 9, 1, 1, 1)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.mColorButton_10 = QgsColorButton(self.ThemesTab)
        self.mColorButton_10.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_10.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_10.setAcceptLiveUpdates(False)
        self.mColorButton_10.setColor(QtGui.QColor(128, 0, 128))
        self.mColorButton_10.setObjectName(_fromUtf8("mColorButton_10"))
        self.horizontalLayout_13.addWidget(self.mColorButton_10)
        self.checkBoxSewer_pressure = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxSewer_pressure.setTristate(True)
        self.checkBoxSewer_pressure.setObjectName(_fromUtf8("checkBoxSewer_pressure"))
        self.horizontalLayout_13.addWidget(self.checkBoxSewer_pressure)
        self.gridLayout_3.addLayout(self.horizontalLayout_13, 10, 0, 1, 1)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.mColorButton_11 = QgsColorButton(self.ThemesTab)
        self.mColorButton_11.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_11.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_11.setColor(QtGui.QColor(0, 128, 128))
        self.mColorButton_11.setObjectName(_fromUtf8("mColorButton_11"))
        self.horizontalLayout_14.addWidget(self.mColorButton_11)
        self.checkBoxHeat = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxHeat.setTristate(True)
        self.checkBoxHeat.setObjectName(_fromUtf8("checkBoxHeat"))
        self.horizontalLayout_14.addWidget(self.checkBoxHeat)
        self.gridLayout_3.addLayout(self.horizontalLayout_14, 11, 0, 1, 1)
        self.annotationCheckBox = QtGui.QCheckBox(self.ThemesTab)
        self.annotationCheckBox.setTristate(True)
        self.annotationCheckBox.setObjectName(_fromUtf8("annotationCheckBox"))
        self.gridLayout_3.addWidget(self.annotationCheckBox, 11, 1, 1, 1)
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.mColorButton_12 = QgsColorButton(self.ThemesTab)
        self.mColorButton_12.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_12.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_12.setColor(QtGui.QColor(0, 0, 255))
        self.mColorButton_12.setObjectName(_fromUtf8("mColorButton_12"))
        self.horizontalLayout_15.addWidget(self.mColorButton_12)
        self.checkBoxWater = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxWater.setTristate(True)
        self.checkBoxWater.setObjectName(_fromUtf8("checkBoxWater"))
        self.horizontalLayout_15.addWidget(self.checkBoxWater)
        self.gridLayout_3.addLayout(self.horizontalLayout_15, 12, 0, 1, 1)
        self.dimensioningCheckBox = QtGui.QCheckBox(self.ThemesTab)
        self.dimensioningCheckBox.setTristate(True)
        self.dimensioningCheckBox.setObjectName(_fromUtf8("dimensioningCheckBox"))
        self.gridLayout_3.addWidget(self.dimensioningCheckBox, 12, 1, 1, 1)
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.mColorButton_14 = QgsColorButton(self.ThemesTab)
        self.mColorButton_14.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_14.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_14.setColor(QtGui.QColor(145, 138, 111))
        self.mColorButton_14.setObjectName(_fromUtf8("mColorButton_14"))
        self.horizontalLayout_17.addWidget(self.mColorButton_14)
        self.checkBoxOrphan = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxOrphan.setTristate(True)
        self.checkBoxOrphan.setObjectName(_fromUtf8("checkBoxOrphan"))
        self.horizontalLayout_17.addWidget(self.checkBoxOrphan)
        self.gridLayout_3.addLayout(self.horizontalLayout_17, 13, 0, 1, 1)
        self.locationCheckBox = QtGui.QCheckBox(self.ThemesTab)
        self.locationCheckBox.setTristate(True)
        self.locationCheckBox.setObjectName(_fromUtf8("locationCheckBox"))
        self.gridLayout_3.addWidget(self.locationCheckBox, 13, 1, 1, 1)
        self.horizontalLayout_18 = QtGui.QHBoxLayout()
        self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
        self.mColorButton_15 = QgsColorButton(self.ThemesTab)
        self.mColorButton_15.setMinimumSize(QtCore.QSize(40, 10))
        self.mColorButton_15.setMaximumSize(QtCore.QSize(40, 10))
        self.mColorButton_15.setColor(QtGui.QColor(111, 92, 16))
        self.mColorButton_15.setObjectName(_fromUtf8("mColorButton_15"))
        self.horizontalLayout_18.addWidget(self.mColorButton_15)
        self.checkBoxOther = QtGui.QCheckBox(self.ThemesTab)
        self.checkBoxOther.setTristate(True)
        self.checkBoxOther.setObjectName(_fromUtf8("checkBoxOther"))
        self.horizontalLayout_18.addWidget(self.checkBoxOther)
        self.gridLayout_3.addLayout(self.horizontalLayout_18, 14, 0, 1, 1)
        self.topoCheckBox = QtGui.QCheckBox(self.ThemesTab)
        self.topoCheckBox.setTristate(True)
        self.topoCheckBox.setObjectName(_fromUtf8("topoCheckBox"))
        self.gridLayout_3.addWidget(self.topoCheckBox, 14, 1, 1, 1)
        self.tabWidget.addTab(self.ThemesTab, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_19 = QtGui.QHBoxLayout()
        self.horizontalLayout_19.setObjectName(_fromUtf8("horizontalLayout_19"))
        self.optionMsgDirButton = QtGui.QPushButton(self.groupBox)
        self.optionMsgDirButton.setMinimumSize(QtCore.QSize(0, 0))
        self.optionMsgDirButton.setObjectName(_fromUtf8("optionMsgDirButton"))
        self.horizontalLayout_19.addWidget(self.optionMsgDirButton)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_19)
        self.textEditDirPreffered = QtGui.QTextEdit(self.groupBox)
        self.textEditDirPreffered.setMinimumSize(QtCore.QSize(20, 20))
        self.textEditDirPreffered.setMaximumSize(QtCore.QSize(1000, 100))
        self.textEditDirPreffered.setBaseSize(QtCore.QSize(200, 40))
        self.textEditDirPreffered.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditDirPreffered.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textEditDirPreffered.setReadOnly(True)
        self.textEditDirPreffered.setObjectName(_fromUtf8("textEditDirPreffered"))
        self.verticalLayout_2.addWidget(self.textEditDirPreffered)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem6 = QtGui.QSpacerItem(20, 318, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem6)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(B4UdigNL)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(B4UdigNL)

    def retranslateUi(self, B4UdigNL):
        B4UdigNL.setWindowTitle(_translate("B4UdigNL", "KLIC Viewer", None))
        self.messageBox.setTitle(_translate("B4UdigNL", "KLIC Berichten", None))
        self.openMsgButton.setText(_translate("B4UdigNL", "&Open Folder...", None))
        self.openArchiveButton.setText(_translate("B4UdigNL", "Open &Zip-bestand...", None))
        self.gotoButton.setText(_translate("B4UdigNL", "&Ga naar", None))
        self.bestScaleButton.setText(_translate("B4UdigNL", "Beste S&chaal", None))
        self.removeMsgButton.setText(_translate("B4UdigNL", "&Sluit Bericht", None))
        self.additionsBox.setTitle(_translate("B4UdigNL", "Bijlagen", None))
        self.openDocButton.setText(_translate("B4UdigNL", "Open &Bijlage(n)", None))
        self.saveButton.setText(_translate("B4UdigNL", "Opslaan in Project", None))
        self.helpButton.setText(_translate("B4UdigNL", "&Help...", None))
        self.closeButton.setText(_translate("B4UdigNL", "Afsl&uiten", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.messageTab), _translate("B4UdigNL", "Berichten", None))
        self.checkBoxData.setText(_translate("B4UdigNL", "Datatransport", None))
        self.refreshButton.setText(_translate("B4UdigNL", "&Ververs", None))
        self.checkBoxGas_low.setText(_translate("B4UdigNL", "Gas lage druk", None))
        self.checkBoxGas_high.setText(_translate("B4UdigNL", "Gas hoge druk", None))
        self.checkBoxDanger.setText(_translate("B4UdigNL", "Buisleiding gevaarlijke inhoud", None))
        self.checkBoxElec_land.setText(_translate("B4UdigNL", "Electriciteit landelijk  hoogspanningsnet", None))
        self.checkBoxElec_high.setText(_translate("B4UdigNL", "Electriciteit hoogspanning", None))
        self.checkBoxElec_mid.setText(_translate("B4UdigNL", "Electriciteit middenspanning", None))
        self.checkBoxElec_low.setText(_translate("B4UdigNL", "Electriciteit laagspanning", None))
        self.checkBoxChemical.setText(_translate("B4UdigNL", "(Petro) chemie", None))
        self.vectorCheckBox.setText(_translate("B4UdigNL", "Vector", None))
        self.checkBoxSewer_free.setText(_translate("B4UdigNL", "Riool vrij verval", None))
        self.rasterCheckBox.setText(_translate("B4UdigNL", "Raster", None))
        self.checkBoxSewer_pressure.setText(_translate("B4UdigNL", "Riool onder druk", None))
        self.checkBoxHeat.setText(_translate("B4UdigNL", "Warmte", None))
        self.annotationCheckBox.setText(_translate("B4UdigNL", "Annotatie", None))
        self.checkBoxWater.setText(_translate("B4UdigNL", "Water ", None))
        self.dimensioningCheckBox.setText(_translate("B4UdigNL", "Maatvoering", None))
        self.checkBoxOrphan.setText(_translate("B4UdigNL", "Wees", None))
        self.locationCheckBox.setText(_translate("B4UdigNL", "Ligging", None))
        self.checkBoxOther.setText(_translate("B4UdigNL", "Overig", None))
        self.topoCheckBox.setText(_translate("B4UdigNL", "Topo", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ThemesTab), _translate("B4UdigNL", "Thema\'s", None))
        self.groupBox.setTitle(_translate("B4UdigNL", "KLIC Berichten", None))
        self.optionMsgDirButton.setText(_translate("B4UdigNL", "Standaard folder...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("B4UdigNL", "Opties", None))

