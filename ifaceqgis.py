"""
/***************************************************************************
ifaceqgis
helper class to implement actions between classes of wv and QGIS
                             -------------------
begin                : 2010-05-18 
copyright            : (C) 2010 by Diethard Jansen
email                : diethard.jansen at gmail.com 
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

from PyQt4 import QtCore, QtGui
from qgis import core, gui

class Iface:
    def __init__(self, iface):
        self.__iface = iface

    def _iface(self):
        """return private attribute iface"""
        return self.__iface

    iface = property(fget=_iface)

    def visibleLayers(self):
        """return list of current visible layer Ids"""
        mapCanvas = self.iface.mapCanvas()
        mapRenderer = mapCanvas.mapRenderer()
        visLayerIds = mapRenderer.layerSet()
        return visLayerIds

    def doRendering(self, p_render=True):
        """
        p_render = boolean
        True do render, False = stop rendering to improve performance
        """
        mapCanvas = self.iface.mapCanvas()
        mapCanvas.setRenderFlag(p_render)

    def refreshMap(self):
        """refreshes map (render map)"""
        mapCanvas = self.iface.mapCanvas()
        mapCanvas.refresh()

    def loadedLayers(self):
        """return dictionary where key is layer id and element is layer"""
        #dicLayers --> key = LayerId, Value = Layer
        layerLegend = core.QgsMapLayerRegistry.instance()
        dicLayers = layerLegend.mapLayers()
        return dicLayers

    def loadLayer(self, wvLayer):
        """load given layer, and return reference of layer"""
        layerFile = wvLayer.layerFile
        layer = self.iface.addRasterLayer(layerFile)
        return layer 

    def getLayerIdForLayer(self, wvLayer):
        """get LayerId for given wv.Layer"""
        layerId = None
        lyrs = self.loadedLayers()
        for i_id, i_lyr in lyrs.iteritems():
            if i_lyr == wvLayer.layer:
                layerId = i_id
                break
        return layerId

    def setVisibilityForLayer(self, wvLayer, visibility):
        """change the visibility for one layer"""
        l_legend = self.iface.legendInterface()
        # check current visibility
        l_layer = wvLayer.layer
        if l_legend.isLayerVisible(l_layer) != visibility:
            # different so set visibility 
            l_legend.setLayerVisible(l_layer, visibility)

    def visibilityForLayer(self, wvLayer):
        """returns boolean, true if layer is visible false if not"""
        l_legend = self.iface.legendInterface()
        # check current visibility
        l_layer = wvLayer.layer
        return l_legend.isLayerVisible(l_layer)

    def gotoLayer(self, wvLayer):
        """ goto extent of given layer """
        lyr = wvLayer.layer
        self.iface.setActiveLayer(lyr)
        self.iface.zoomToActiveLayer()

    def removeLayer(self, wvLayer):
        """ remove layer from QGIS map registry"""
        lyr_id = wvLayer.layerId
        layerLegend = core.QgsMapLayerRegistry.instance()
        layerLegend.removeMapLayer(lyr_id)
        
    def bestScale(self, wvLayer):
        """Set best scale for given layer"""
        lyr = wvLayer.layer
        self.iface.setActiveLayer(lyr)
        action = self.iface.actionZoomActualSize()
        action.activate(0) # triggers/invokes the action


        
