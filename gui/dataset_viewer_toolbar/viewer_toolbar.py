# -*- coding: utf-8 -*-

"""
/***************************************************************************
 DeepLearningTools
                                 A QGIS plugin
 QGIS plugin to aid training Deep Learning Models

                              -------------------
        begin                : 2020-04-04
        copyright            : (C) 2020 by Philipe Borba
        email                : philipeborba@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
from qgis.PyQt.QtWidgets import QMessageBox, QSpinBox, QAction, QWidget
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QSettings, pyqtSignal, pyqtSlot, QObject, Qt
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.Qt import QObject

from qgis.core import QgsMapLayer, Qgis, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeatureRequest, QgsWkbTypes, QgsProject
from qgis.gui import QgsMessageBar

# from .inspectFeatures_ui import Ui_Form
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'viewer_toolbar.ui'))

class ViewerToolbar(QWidget,FORM_CLASS):
    def __init__(self, iface, parent=None):
        """
        Constructor
        """
        super(ViewerToolbar, self).__init__(parent)
        self.setupUi(self)
    
    def unload(self):
        pass