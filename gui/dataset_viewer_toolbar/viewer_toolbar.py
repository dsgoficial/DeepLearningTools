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
from functools import partial
from qgis.PyQt.QtWidgets import QMessageBox, QSpinBox, QAction, QWidget
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QSettings, pyqtSignal, pyqtSlot, QObject, Qt
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.Qt import QObject

from qgis.core import QgsMapLayer, Qgis, QgsVectorLayer,\
    QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeatureRequest,\
    QgsWkbTypes, QgsProject, QgsRasterLayer
from qgis.gui import QgsMessageBar
import processing

# from .inspectFeatures_ui import Ui_Form
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'viewer_toolbar.ui'))

class ViewerToolbar(QWidget,FORM_CLASS):
    def __init__(self, iface, parent=None):
        """
        Constructor
        """
        super(ViewerToolbar, self).__init__(parent)
        self.iface = iface
        self.loaded_label_ids = set()
        self.setupUi(self)
        self.labelView = None
    
    def unload(self):
        try:
            self.set_dynamic_mode(False)
        except:
            pass
    
    @pyqtSlot(bool, name = 'on_dynamicPushButton_toggled')
    def set_dynamic_mode(self, toggled):
        if toggled:
            self.iface.mapCanvas().extentsChanged.connect(
                self.update_loaded_layers
            )
        else:
            self.iface.mapCanvas().extentsChanged.disconnect(
                self.update_loaded_layers
            )
    
    @pyqtSlot(bool, name = 'on_sideBySidePushButton_toggled')
    def create_label_view(self, toggled):
        if self.labelView is None and toggled:
            self.labelView = self.iface.createNewMapCanvas(self.tr('Label View'))
            self.labelView.setLayers(
                [
                    i for i in self.iface.mapCanvas().layers()\
                        if isinstance(i, QgsRasterLayer) and 'label_' in i.name()
                ]
            )
            self.labelView.destroyed.connect(
                self.delete_view
            )
            self.iface.mapCanvas().extentsChanged.connect(
                self.set_label_view_extent
            )
    
    def set_label_view_extent(self):
        self.labelView.blockSignals(True)
        self.labelView.setExtent(self.iface.mapCanvas().extent())
        self.labelView.zoomScale(self.iface.mapCanvas().scale())
        self.labelView.blockSignals(False)
    
    def delete_view(self):
        self.sideBySidePushButton.blockSignals(True)
        self.sideBySidePushButton.setChecked(False)
        self.iface.mapCanvas().extentsChanged.disconnect(
                self.set_label_view_extent
            )
        self.sideBySidePushButton.blockSignals(False)
        self.labelView = None


    @pyqtSlot(name = 'on_activatePushButton_clicked')
    def update_loaded_layers(self):
        index_layer = self.mMapLayerComboBox.currentLayer()
        image_path = self.imageFieldComboBox.currentField()
        label_path = self.labelFieldComboBox.currentField()
        current_extent = self.iface.mapCanvas().extent()
        result_images = processing.run(
            "DeepLearningTools:loadimages",
            {
                'INPUT':index_layer,
                'SELECTED':False,
                'EXTENT':current_extent,
                'IMAGE_ATTRIBUTE':image_path,
                'ADD_TO_CANVAS':True,
                'UNIQUE_LOAD':True,
                'GROUP_EXPRESSION':"'images'",
                'NAME_TAG':'image'
            }
        )
        result_labels = processing.run(
            "DeepLearningTools:loadimages",
            {
                'INPUT':index_layer,
                'SELECTED':False,
                'EXTENT':current_extent,
                'IMAGE_ATTRIBUTE':label_path,
                'ADD_TO_CANVAS':True,
                'UNIQUE_LOAD':True,
                'GROUP_EXPRESSION':"'labels'",
                'NAME_TAG':'label'
            }
        )
        loadedSet = set(result_images['OUTPUT']).union(set(result_labels['OUTPUT']))
        if self.loaded_label_ids == set():
            self.loaded_label_ids = loadedSet
            return
        self.iface.mapCanvas().freeze(True)
        layers_to_remove = set(
            lyr_id for lyr_id in self.loaded_label_ids if lyr_id not in loadedSet
        )
        QgsProject.instance().removeMapLayers(
            layers_to_remove
        )
        self.loaded_label_ids = loadedSet.union(
            self.loaded_label_ids.difference(layers_to_remove)
        )
        self.iface.mapCanvas().freeze(False)