# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DeepLearningTools
                                 A QGIS plugin
 QGIS plugin to aid training Deep Learning Models
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-03-12
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
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Philipe Borba'
__date__ = '2020-03-12'
__copyright__ = '(C) 2020 by Philipe Borba'

from .deep_learning_tools import DeepLearningTools
deepLearningTools = None

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load DeepLearningTools class from file DeepLearningTools.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    global deepLearningTools
    deepLearningTools = DeepLearningTools(iface)
    return deepLearningTools
