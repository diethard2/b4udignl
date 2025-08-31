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

from builtins import str
from builtins import object
from qgis.PyQt import QtCore, QtGui
from qgis import core, gui
import os

class Iface(object):
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
        mapCanvas.refreshAllLayers()

    def refreshLegend(self):
        """refreshes legend"""
        pass

    def loadedLayers(self):
        """return dictionary where key is layer id and element is layer"""
        #dicLayers --> key = LayerId, Value = Layer
        project = core.QgsProject.instance()
        dictLayers = project.mapLayers()
        return dictLayers

    def loadLayer(self, wvLayer):
        """
        load given layer, create a new layer when it does not exist
        add new features to it, return layer and new mapfeatures
        """
        layer = None
        features = []
        layer = self.layerByName(wvLayer.layerName)
        if layer is None:
            layer = self.addLayer(wvLayer)
        if layer is not None:
            features = self.addFeatures(wvLayer)
        return layer, features

    def layerByName(self, a_name):
        """return layer by name"""
        layer = None
        project = core.QgsProject.instance()
        layers = project.mapLayersByName(a_name)
        if len(layers) == 1:
            layer = layers[0]
        return layer

    def addLayer(self, wvLayer):
        """add layer to map and return the layer"""
        if wvLayer.is_vector():
            a_layer = wvLayer.layer
            provider = a_layer.dataProvider()
            provider.addAttributes(wvLayer.fields)
            a_layer.updateFields()
            project = core.QgsProject.instance()
            layer = project.addMapLayer(a_layer, True)
            self.styleLayer(layer)
        else:
            layerFile = wvLayer.layerFile
            layer = self.iface.addRasterLayer(layerFile)
        return layer

    def addFeatures(self, wvLayer):
        """add features to given layer"""
        features = []
        if wvLayer.is_vector():
            a_layer = wvLayer.layer
            with core.edit(a_layer):
                provider = a_layer.dataProvider()
                isAdded, features = provider.addFeatures(wvLayer.features)
            a_layer.updateExtents()
        return features

    def styleLayer(self, a_layer):
        """
        Using the layersname try to style the layer
        an existing QGIS style file included with plugin
        """
        qml_path = os.path.join(self.path, 'styles', 'qml')
        qml_file = os.path.join(qml_path, a_layer.name()) + '.qml'
        if os.path.exists(qml_file):
            a_layer.loadNamedStyle(qml_file)

    def setVisibilityForLayer(self, wvLayer, visibility,
                              show_raster, show_vector, theme = None):
        """change the visibility for one layer"""
        layer = wvLayer.layer
        if wvLayer.is_vector():
            if show_vector and theme is not None:
                renderer = layer.renderer()
                if isinstance(renderer, core.QgsRuleBasedRenderer):
                    self._set_visibility_rules_symbol(layer, theme, visibility)
                elif isinstance(renderer, core.QgsSingleSymbolRenderer):
                    self.setLayerVisible(layer, visibility)
        else:
            isVisible = self.isLayerVisible(layer)
            if show_raster and isVisible != visibility:
                # different so set visibility
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
        tree_layer.setItemVisibilityChecked(visibility)

    def _treeLayer(self, layer):
        root_group = self.iface.layerTreeView().layerTreeModel().rootGroup()
        return root_group.findLayer(layer.id())

    def _visibility_for_layer_theme(self, layer, theme):
        '''check visibility of all themes in layer.
        If all are visible: return 2
        If some are visible: return 1
        If none are visible: return 0
        '''
        renderer = layer.renderer()
        visibility = 0
        if isinstance(renderer, core.QgsRuleBasedRenderer):
            visibility = self._visibility_from_rules_symbol(layer, theme)
        elif isinstance(renderer,core.QgsSingleSymbolRenderer):
            visibility = self.isLayerVisible(layer)
        return visibility

    def _visibility_from_rules_symbol(self, layer, theme):
        state = 0
        renderer = layer.renderer()
        rules = renderer.rootRule().children()
        visibilities = []
        for rule in rules:
            expression = rule.filterExpression()
            expression = str(expression).lower()
            if theme in expression:
                visibilities.append(rule.active())
        n_visibilities = len(visibilities)
        if all(visibilities):
            state = 2
        elif any(visibilities):
            state = 1
        else:
            state = 0
        return state

    def _set_visibility_rules_symbol(self, layer, theme, visibility):
        state = None
        if visibility == 0:
            state = False
        elif visibility == 1:
            return
        elif visibility == 2:
            state = True
        renderer = layer.renderer()
        rules = renderer.rootRule().children()
        for rule in rules:
            expression = rule.filterExpression()
            expression = str(expression).lower()
            if theme in expression:
                if rule.active() != state:
                    rule.setActive(state)

    def gotoLayer(self, wvLayer):
        """ goto extent of given layer """
        lyr = wvLayer.layer
        self.iface.setActiveLayer(lyr)
        self.iface.zoomToActiveLayer()

    def removeLayer(self, wvLayer):
        """ remove layer from QGIS map registry"""
        lyr = wvLayer.layer
        remove = True
        if wvLayer.is_vector():
            lyr.startEditing()
            lyr.deleteFeatures(wvLayer.featureIds)
            lyr.commitChanges()
            if lyr.hasFeatures():
                remove = False
        if remove:      
            project = core.QgsProject.instance()
            project.removeMapLayer(lyr)

    def bestScale(self, wvLayer):
        """Set best scale for given layer"""
        lyr = wvLayer.layer
        self.iface.setActiveLayer(lyr)
        action = self.iface.actionZoomActualSize()
        action.activate(0) # triggers/invokes the action
