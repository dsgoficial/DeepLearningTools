# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewer_toolbar.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ViewerToolbar(object):
    def setupUi(self, ViewerToolbar):
        ViewerToolbar.setObjectName("ViewerToolbar")
        ViewerToolbar.resize(559, 44)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ViewerToolbar.sizePolicy().hasHeightForWidth())
        ViewerToolbar.setSizePolicy(sizePolicy)
        ViewerToolbar.setToolTip("")
        self.gridLayout = QtWidgets.QGridLayout(ViewerToolbar)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(ViewerToolbar)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.mMapLayerComboBox = gui.QgsMapLayerComboBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mMapLayerComboBox.sizePolicy().hasHeightForWidth()
        )
        self.mMapLayerComboBox.setSizePolicy(sizePolicy)
        self.mMapLayerComboBox.setObjectName("mMapLayerComboBox")
        self.label_2 = QtWidgets.QLabel(self.splitter)
        self.label_2.setObjectName("label_2")
        self.imageFieldComboBox = gui.QgsFieldComboBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.imageFieldComboBox.sizePolicy().hasHeightForWidth()
        )
        self.imageFieldComboBox.setSizePolicy(sizePolicy)
        self.imageFieldComboBox.setObjectName("imageFieldComboBox")
        self.label_3 = QtWidgets.QLabel(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.labelFieldComboBox = gui.QgsFieldComboBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.labelFieldComboBox.sizePolicy().hasHeightForWidth()
        )
        self.labelFieldComboBox.setSizePolicy(sizePolicy)
        self.labelFieldComboBox.setObjectName("labelFieldComboBox")
        self.activatePushButton = QtWidgets.QPushButton(self.splitter)
        self.activatePushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/plugins/DeepLearningTools/icons/refresh.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.activatePushButton.setIcon(icon)
        self.activatePushButton.setObjectName("activatePushButton")
        self.dynamicPushButton = QtWidgets.QPushButton(self.splitter)
        self.dynamicPushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/plugins/DeepLearningTools/icons/dynamic.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.dynamicPushButton.setIcon(icon1)
        self.dynamicPushButton.setCheckable(True)
        self.dynamicPushButton.setObjectName("dynamicPushButton")
        self.sideBySidePushButton = QtWidgets.QPushButton(self.splitter)
        self.sideBySidePushButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/plugins/DeepLearningTools/icons/dual_view.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.sideBySidePushButton.setIcon(icon2)
        self.sideBySidePushButton.setCheckable(True)
        self.sideBySidePushButton.setObjectName("sideBySidePushButton")
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(ViewerToolbar)
        self.mMapLayerComboBox.layerChanged["QgsMapLayer*"].connect(
            self.imageFieldComboBox.setLayer
        )
        self.mMapLayerComboBox.layerChanged["QgsMapLayer*"].connect(
            self.labelFieldComboBox.setLayer
        )
        QtCore.QMetaObject.connectSlotsByName(ViewerToolbar)

    def retranslateUi(self, ViewerToolbar):
        _translate = QtCore.QCoreApplication.translate
        ViewerToolbar.setWindowTitle(_translate("ViewerToolbar", "Form"))
        self.label.setText(_translate("ViewerToolbar", "Index Layer"))
        self.label_2.setText(_translate("ViewerToolbar", "Image Path"))
        self.label_3.setText(_translate("ViewerToolbar", "Label Path"))
        self.activatePushButton.setToolTip(
            _translate("ViewerToolbar", "Activate/Refresh")
        )
        self.dynamicPushButton.setToolTip(
            _translate("ViewerToolbar", "Activate Dynamic View")
        )
        self.sideBySidePushButton.setToolTip(
            _translate("ViewerToolbar", "Activate Side By Side View")
        )


from qgis import gui
