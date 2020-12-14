# -*- coding: utf-8 -*-

"""
/***************************************************************************
 DeepLearningTools
                                 A QGIS plugin
 QGIS plugin to aid training Deep Learning Models
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-04-108
        copyright            : (C) 2020 by Philipe Borba
        email                : philipeborba@gmail.com
        Compactness, complexity, deviation from the convex hull, amplitude of 
        vibration, frequency of the vibration and the number of vertexes
        taken from https://github.com/pondrejk/PolygonComplexity
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
import os, uuid
import tempfile
import processing
from osgeo import gdal, osr, ogr
gdal.UseExceptions()
from qgis.core import (
    QgsRectangle, QgsFeatureRequest,
    QgsCoordinateTransformContext, QgsCoordinateReferenceSystem,
    QgsRasterLayer, QgsSpatialIndex, QgsFeature, QgsWkbTypes, QgsGeometry
)
from math import sqrt, log, pi

class VectorUtils:

    statDict = {
        'n_vertexes' : lambda geom: find_feature_vertices(geom),
        'main_angle' : lambda geom: main_angle(geom),
        'hole_count' : lambda geom: hole_count(geom),
        'area' : lambda geom: geom.area(),
        'perimeter' : lambda geom: geom.length(),
        'compactness' : lambda geom: find_feature_compactness(geom),
        'fractal_dimension' : lambda geom: fractal_dimension(geom),
        'fractality' : lambda geom: fractality(geom),
        'vibration_amplitude' : lambda geom: find_feature_amplitude(geom),
        'vibration_frequency' : lambda geom: find_vibration_frequency(geom),
        'geometry_complexity' : lambda geom: find_feature_complexity(geom),
        'find_feature_shape_complexity_index' : lambda geom: find_feature_shape_complexity_index(geom),
        'equivaent_rectangular_index' : lambda geom: find_equivalent_rectangular_index(geom),
        'circularity' : lambda geom: find_circularity(geom),
        'squareness' : lambda geom: find_squareness(geom),
        'rectangularity' : lambda geom: find_rectangularity(geom)
    }

    def buildSpatialIndexAndIdDict(self, inputLyr, feedback = None, featureRequest=None):
        """
        creates a spatial index for the input layer
        :param inputLyr: (QgsVectorLayer) input layer;
        :param feedback: (QgsProcessingFeedback) processing feedback;
        :param featureRequest: (QgsFeatureRequest) optional feature request;
        """
        spatialIdx = QgsSpatialIndex()
        idDict = {}
        featCount = inputLyr.featureCount()
        size = 100/featCount if featCount else 0
        iterator = inputLyr.getFeatures() if featureRequest is None else inputLyr.getFeatures(featureRequest)
        addFeatureAlias = lambda x : self.addFeatureToSpatialIndex(
            current=x[0],
            feat=x[1],
            spatialIdx=spatialIdx,
            idDict=idDict,
            size=size,
            feedback=feedback
        )
        list(map(addFeatureAlias, enumerate(iterator)))
        return spatialIdx, idDict
    
    def addFeatureToSpatialIndex(self, current, feat, spatialIdx, idDict, size, feedback):
        """
        Adds feature to spatial index. Used along side with a python map operator
        to improve performance.
        :param current : (int) current index
        :param feat : (QgsFeature) feature to be added on spatial index and on idDict
        :param spatialIdx: (QgsSpatialIndex) spatial index
        :param idDict: (dict) dictionary with format {feat.id(): feat}
        :param size: (int) size to be used to update feedback
        :param feedback: (QgsProcessingFeedback) feedback to be used on processing
        """
        if feedback is not None and feedback.isCanceled():
            return
        idDict[feat.id()] = feat
        spatialIdx.addFeature(feat)
        if feedback is not None:
            feedback.setProgress(size * current)
    
    def runMergeVectorLayers(self, inputList, context, feedback=None, outputLyr=None, crs=None):
        outputLyr = 'memory:' if outputLyr is None else outputLyr
        parameters = {
            'LAYERS' : inputList,
            'CRS' : crs,
            'OUTPUT' : outputLyr
        }
        output = processing.run(
            'native:mergevectorlayers',
            parameters,
            context=context,
            feedback=feedback
        )
        return output['OUTPUT']
    
    def calculateStatistics(self, feat, statList, fields):
        newFeat = self.createNewFeat(feat, fields)
        for stat in statList:
            newFeat[stat] = abs(self.statDict[stat](newFeat.geometry()))
        return newFeat

    def createNewFeat(self, feat, fields):
        newFeat = QgsFeature(fields)
        for field in feat.fields():
            if field in fields:
                newFeat[field.name()] = feat[field.name()]
        newFeat.setGeometry(feat.geometry())
        return newFeat

def find_feature_compactness(geom):
    return (geom.length()/(3.54 * sqrt(geom.area()))) # 1 for a circle

def find_feature_shape_complexity_index(geom):
    """https://jblindsay.github.io/wbt_book/available_tools/gis_analysis_patch_shape_tools.html#ShapeComplexityIndex

    SCI = 1 - A/Ah

    Args:
        geom ([type]): [description]

    Returns:
        [type]: [description]
    """
    hull_area = 0
    geom_area = 0
    if geom.isMultipart():
      new_features = []
      temp_feature = QgsFeature()
      for part in geom.asGeometryCollection():
        temp_feature.setGeometry(part)
        new_features.append(QgsFeature(temp_feature))
      for subfeature in new_features:
          hull_area += subfeature.geometry().convexHull().area()
          geom_area += subfeature.geometry().area()
      return 1.0 - geom_area/hull_area
    else:
      hull_area = geom.convexHull().area()
      return 1.0 - geom.area()/hull_area

def find_feature_amplitude(geom):
    hull_length = 0
    geom_length = 0
    if geom.isMultipart():
      new_features = []
      temp_feature = QgsFeature()
      for part in geom.asGeometryCollection():
        temp_feature.setGeometry(part)
        new_features.append(QgsFeature(temp_feature))
      for subfeature in new_features:
          hull_length += subfeature.geometry().convexHull().length()
          geom_length += subfeature.geometry().length()
      return 1.0 - hull_length/geom_length
    else:
      hull_length =  geom.convexHull().length()
      geom_length =  geom.length()
      return 1.0 - hull_length/geom_length

def find_feature_notches(geom):
    notches = 0
    if geom.type() == QgsWkbTypes.PolygonGeometry:
        notches = 0
        if geom.isMultipart():
          polygons = geom.asMultiPolygon()
        else:
          polygons = [ geom.asPolygon() ]
        for polygon in polygons:
          for ring in polygon:
            triplet = []
            ring.append(ring[1])
            for i in ring:
                triplet.append(i) 
                if len(triplet) > 3:
                    del triplet[0]
                if len(triplet) == 3:
                    zcp = find_convex(triplet)
                    if zcp > 0: 
                        notches +=1

    return notches

def find_feature_vertices(geom):
    if geom is None:
        return None
    if geom.type() == QgsWkbTypes.PolygonGeometry:
        count = 0
        if geom.isMultipart():
          polygons = geom.asMultiPolygon()
        else:
          polygons = [ geom.asPolygon() ]
        for polygon in polygons:
          for ring in polygon:
            count += len(ring)
    count = count - 1.0
    return count

def find_feature_complexity(geom):
    conv = find_feature_shape_complexity_index(geom)
    ampl = find_feature_amplitude(geom)
    freq = find_vibration_frequency(geom)
    return ((0.8 * ampl * freq) * (0.2 * conv))

def find_convex(triplet):
    a1,a2,a3 = triplet[0], triplet[1], triplet[2]
    dx1 = a2[0] - a1[0]
    dy1 = a2[1] - a1[1]
    dx2 = a3[0] - a2[0]
    dy2 = a3[1] - a2[1]
    zcrossproduct = dx1*dy2 - dy1*dx2
    return zcrossproduct

def find_vibration_frequency(geom):
    feature_vertices = find_feature_vertices(geom)
    feature_notches = find_feature_notches(geom)
    feature_notches_normalized = float(feature_notches) / float(feature_vertices - 3) if feature_vertices != 3 else 0
    return 16.0*(feature_notches_normalized - 0.5)**4 - 8*(feature_notches_normalized - 0.5)**2 - 1.0


def fractal_dimension(geom):
    """Fractal dimension of a polygon
    http://www.umass.edu/landeco/research/fragstats/documents/Metrics/Shape%20Metrics/Metrics/P9%20-%20FRAC.htm

    Args:
        geom ([type]): [description]

    Returns:
        [type]: [description]
    """
    return 2*log(0.25*geom.length()) / log(geom.area())

def fractality(geom):
    """Fractality of a polygon

    Args:
        geom ([type]): [description]
    """
    return 1-log(geom.area())/(2*log(geom.length()))

def find_rectangularity(geom):
    orientedBB, area, angle, width, height = geom.orientedMinimumBoundingBox()
    return geom.area() / area

def find_squareness(geom):
    return 4*sqrt(geom.area()) / geom.length()

def main_angle(geom):
    area, angle, width, height = 0.0, 0.0, 0.0, 0.0
    orientedBB, area, angle, width, height = geom.orientedMinimumBoundingBox()
    return angle

def hole_count(geom):
    return len(getHoles(geom))

def getHoles(geom):
    donutholes = []
    for part in geom.asGeometryCollection():
        for current, item in enumerate(part.asPolygon()):
            newGeom = QgsGeometry.fromPolygonXY([item])
            if current == 0:
                continue
            else:
                donutholes.append(newGeom)
    return donutholes

def find_equivalent_rectangular_index(geom):
    orientedBB, area, angle, width, height = geom.orientedMinimumBoundingBox()
    return (orientedBB.length() / geom.length()) * sqrt(geom.area()/area)

def find_circularity(geom):
    return 4*pi*geom.area() / (geom.length)**2