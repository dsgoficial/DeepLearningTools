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
"""
from osgeo import gdal, osr, ogr
gdal.UseExceptions()
from qgis.core import QgsRectangle, QgsFeatureRequest,\
    QgsCoordinateTransformContext, QgsCoordinateReferenceSystem

class ImageUtils:

    def get_srs(self, input_ds):
        raster_srs = osr.SpatialReference()
        raster_srs.ImportFromWkt(
            input_ds.GetProjectionRef()
        )
        return raster_srs

    def set_output_srs_form_input(self, input_ds, output_ds):
        """
        Sets output srs the same as input
        """
        raster_srs = self.get_srs(input_ds)
        output_ds.SetGeoTransform(input_ds.GetGeoTransform())
        output_ds.SetProjection(raster_srs.ExportToWkt())

    def get_output_raster_from_input(self, input_path, output_path):
        """
        Gets the output raster equals to the input, but only with
        nodata.
        """
        input_ds = gdal.Open(input_path)
        driver = gdal.GetDriverByName('GTiff')
        output_ds = driver.Create(
            output_path,
            input_ds.RasterXSize,
            input_ds.RasterYSize,
            1,
            gdal.GDT_Byte
        )
        self.set_output_srs_form_input(input_ds, output_ds)
        input_ds = None
        return output_ds

    def get_band(self, raster_ds, band_number, nodata_value=0):
        band = raster_ds.GetRasterBand(band_number)
        band.Fill(nodata_value)
        # band.SetNoDataValue(nodata_value)
        return band
    
    def get_extents(self, raster_ds):
        geo_transform = raster_ds.GetGeoTransform()
        xmin = geo_transform[0]
        ymax = geo_transform[3]
        xmax = xmin + geo_transform[1] * raster_ds.RasterXSize
        ymin = ymax + geo_transform[5] * raster_ds.RasterYSize
        return [xmin, ymin, xmax, ymax]

    def build_ogr_temp_layer(self, input_lyr, raster_ds):
        driver = ogr.GetDriverByName('MEMORY')
        temp_ds = driver.CreateDataSource('temp_data')
        temp = driver.Open('temp_data', 1)
        temp_lyr = temp_ds.CreateLayer(
            "temp_layer",
            self.get_srs(raster_ds),
            geom_type=input_lyr.wkbType()
        )
        # burn
        xmin, ymin, xmax, ymax = self.get_extents(raster_ds)
        extents = QgsRectangle(
            xmin, ymin, xmax, ymax
        )
        request = QgsFeatureRequest().setDestinationCrs(
            QgsCoordinateReferenceSystem(
                raster_ds.GetProjectionRef()
            ),
            QgsCoordinateTransformContext()
        ).setFilterRect(extents)
        field_name = "f"
        field_id = ogr.FieldDefn(field_name, ogr.OFTInteger)
        temp_lyr.CreateField(field_id)
        feat_definition = temp_lyr.GetLayerDefn()
        def populate_temp_lyr(feat):
            wkt_geom = feat.geometry().asWkt()
            new_feat = ogr.Feature(feat_definition)
            new_feat.SetGeometry(
                ogr.CreateGeometryFromWkt(wkt_geom)
            )
            return new_feat
        temp_lyr.StartTransaction()
        for feat in input_lyr.getFeatures(request):
            new_feat = populate_temp_lyr(feat)
            temp_lyr.CreateFeature(new_feat)
            new_feat = None
        # list(
        #     map(temp_lyr.CreateFeature,
        #         map(populate_temp_lyr, input_lyr.getFeatures(request))
        #     )
        # )
        temp_lyr.CommitTransaction()
        return temp_lyr, temp, driver, temp_ds

    def create_image_label(self, input_path, output_path, input_lyr,\
        burn_value=0, nodata_value=0):
        """
        Creates image label with the same size as input_path
        """
        output_ds = self.get_output_raster_from_input(
            input_path,
            output_path
        )
        band = self.get_band(output_ds, 1, nodata_value=nodata_value)
        band.FlushCache()
        temp_lyr, temp, driver, temp_ds = self.build_ogr_temp_layer(
            input_lyr,
            output_ds
        )
        gdal.RasterizeLayer(
            output_ds,
            [1],
            temp_lyr,
            burn_values=[burn_value]
        )
        output_ds = None
        temp_lyr = None
