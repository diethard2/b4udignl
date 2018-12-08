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
import os

class Iface:
    def __init__(self, iface):
        self.__iface = iface
        self.__path = os.path.dirname(os.path.realpath(__file__))

    def _iface(self):
        """return private attribute iface"""
        return self.__iface

    iface = property(fget=_iface)

    def _path(self):
        return self.__path

    path = property(fget=_path)

    def visibleLayers(self):
        """return list of current visible layer Ids"""
        mapCanvas = self.iface.mapCanvas()
        mapSettings = mapCanvas.Settings()
        layerIds = mapSettings.layers()
        return layerIds

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

    def refreshLegend(self):
        """refreshes legend"""
        legend = self.iface.legendInterface()
        for layer in self.loadedLayers().values():
            legend.refreshLayerSymbology(layer)

    def loadedLayers(self):
        """return dictionary where key is layer id and element is layer"""
        #dicLayers --> key = LayerId, Value = Layer
        layerLegend = core.QgsMapLayerRegistry.instance()
        dicLayers = layerLegend.mapLayers()
        return dicLayers

    def loadLayer(self, wvLayer):
        """load given layer, and return reference of layer"""
        if wvLayer.is_vector():
            layer = wvLayer.layer
            provider = layer.dataProvider()
            provider.addAttributes(wvLayer.fields)
            layer.updateFields()                        
            layer.dataProvider().addFeatures(wvLayer.features)
            layer.updateExtents()
            registry = core.QgsMapLayerRegistry.instance()
            registry.addMapLayer(layer)
            layer = registry.mapLayersByName(wvLayer.layerName)
            layer = layer[0]
            self.styleLayer(layer)
        else:
            layerFile = wvLayer.layerFile
            layer = self.iface.addRasterLayer(layerFile)
        self.iface.legendInterface().setLayerExpanded(layer, False)
        return layer

    def styleLayer(self, a_layer):
        qml_path = os.path.join(self.path, 'styles', 'qml')
        qml_file = os.path.join(qml_path, a_layer.name()) + '.qml'
        if os.path.exists(qml_file):
            a_layer.loadNamedStyle(qml_file)
        return a_layer

    def setVisibilityForLayer(self, wvLayer, visibility, theme = None):
        """change the visibility for one layer"""
        # check current visibility
        layer = wvLayer.layer
        if not wvLayer.is_vector() or theme is None:
            if self.isLayerVisible(layer) != visibility:
                # different so set visibility
                self.setLayerVisible(layer, visibility)
            else:
                renderer = layer.rendererV2()
                if isinstance(renderer, core.QgsRuleBasedRendererV2):
                    visibility = self.set_visibility_rules_symbol(layer, theme)
                elif isinstance(renderer, core.QgsSingleSymbolRendererV2):
                    self.setLayerVisible(layer, visibility)

    def visibilityForLayer(self, wvLayer, theme = None):
        """returns boolean, true if layer is visible false if not"""
        visibility = None
        layer = wvLayer.layer
        # check current visibility
        if wvLayer.is_vector() and theme is not None:
            visibility = self._visibility_for_layer_theme(layer, theme)
        else:
            visibility = self.isLayerVisible(layer)
        return visibility

    def isLayerVisible(self, layer):
        tree_layer = self._treeLayer(layer)
        value = tree_layer.isVisible()
        return value

    def setLayerVisible(self, layer, visibility):
        tree_layer = self._treeLayer(layer)
        tree_layer.setVisible(visibility)

    def _treeLayer(self, layer):
        root_group = self.iface.layerTreeView().layerTreeModel().rootGroup()
        return root_group.findLayer(layer.id())      

    def _visibility_for_layer_theme(self, layer, theme):
        '''check visibility of all themes in layer.
        If all are visible: return True
        If none are visible: return False
        If some are visible: return None
        '''
        renderer = layer.rendererV2()
        visibility = 0
        if isinstance(renderer, core.QgsRuleBasedRendererV2):
            visibility = self._visibility_from_rules_symbol(layer, theme)
        elif isinstance(renderer,core.QgsSingleSymbolRendererV2):
            visibility = self.isLayerVisible(layer)
        return visibility

    def _visibility_from_rules_symbol(self, layer, theme):
        renderer = layer.rendererV2()
        rules = renderer.rootRule().children()
        visibilities = []
        for rule in rules:
            expression = rule.filterExpression()
            if not 'NOT'in expression and theme in expression:
                visibilities.append(rule.checkState())
        visibility = sum(visibilities)/len(visibilities)
##        for v in visibilies:
##            if visibility is None:
##                visibility = v
##            else:
##                if visibility is not v:
##                    visibility = None
##                    break
        return visibility

    def _set_visibility_rules_symbol(self, layer, theme, visibility):
        renderer = layer.rendererV2()
        rules = renderer.rootRule().children()
        for rule in rules:
            expression = rule.filterExpression()
            if not 'NOT'in expression and theme in expression:
                if rule.checkState() != visibility:
                    rule.setCheckState(visibility)
        
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


        
