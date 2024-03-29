"""
/***************************************************************************
wv (Wion Viewer)
Holds all classes to hold all references to full WION reply
-------------------
begin                : 2010-02-01
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

wv holds all classes to hold all references to full WION reply.
it uses a helper class to communicate with a GIS.
This is implemented for QGIS but can be used for other GIS/purposes as well.

Doc is the top class that contains all elements of a Dutch
'reply to a call before you dig message' (Dutch=resultaat Graafmelding).
It should be created using the path to the folder that contain
all png files and pdf documents that will be made available in application.
(i.e. opensource desktop GIS/ web application).

This WION Viewer plugin named b4udignl was a reaction to the first versions of
the free klicviewer that the Dutch National Cartographic Agency supplies.
It lacked some important basic features that are available in QGIS like
a coordinate systems, measuring and the possibility to load design drawings.

Author: Diethard Jansen, 14-3-2010
"""

from __future__ import print_function
from __future__ import absolute_import
from builtins import object
import os
import xml.etree.ElementTree as ET
import gc
from . import imkl, xml_utils
from .wv_storage import Storage1, Storage2
from .wv_objects import Theme, Layer, PdfFile
from qgis.PyQt.QtWidgets import QMessageBox

class Doc(object):
    
    def __init__(self, path_message):
        """path_message = full path to directory which holds result of WION message.
        Creates instance of Doc which holds all information of WION result.
        Creates whole structure using XML file in given directory.
        Creates world files that are used in GIS systems to show rasterfiles.
        Interface to GIS is delegated to attribute iface.
        """

        self._tag2function = imkl.tag2function()        
        # holds folder used to create whole structure
        self.__path = os.path.realpath(path_message)
        # holds interface to gis.   
        self.__iface = None
        self._init_imkls()
        self.storage = None
        self.__version = None
        self.schemaLocation = None
        self.layerGroups = {}
        self.__themes = {}
        self.__showVector = True
        self.__showRaster = True
        # find and read xml file holding metadata
        xml_files = self._xml_files()
        self._parse_xml_files(xml_files)
        self._set_attributes_from_imkl()
        # set themes and create world files
        self._setThemes()
        self._createWorldFiles()

    def _init_imkls(self):
        self.imkls = {}
        self.imkls_on_id = {}

# defining access to attributes of class Doc
    def _iface(self):
        """return private attribute iface"""
        return self.__iface
    
    def _setIface(self, iface):
        """set private attribute iface"""
        # set it only once
        if self.__iface == None:
            self.__iface  = iface
    
    iface = property(fget=_iface, fset=_setIface)
        
    def _version(self):
        """return private attribute version"""
        if self.__version is None:
            self.__version = self._get_version()
        return self.__version

    version = property(fget=_version)

    def _get_version(self):
        """the first time the version is requested, find out the
        version from imkl elements"""
        version = None
        if self.schemaLocation is not None:
            l = self.schemaLocation.split(sep='/')
            if 'imkl2015' in l:
                i = l.index('imkl2015')
                version = l[i+1]
            else:
                l2 = l[5:]
                if 'imkl' in l2:
                    i = l2.index('imkl')
                    version = l2[i+1]
        if version is None and imkl.LEVERINGSINFORMATIE in self.imkls:
            imkl_obj = self.imkls[imkl.LEVERINGSINFORMATIE][0]
            version = imkl_obj.field("version").value
                            
        return version
        
    def _path(self):
        """return privat attribute path"""
        return self.__path

    path = property(fget=_path)

    def _themes(self):
        """return private attribute themes from storage"""
        return self.__themes
    
    themes = property(fget=_themes)

    def _showVector(self):
        """return private attribute showVector"""
        return self.__showVector
    
    def _setShowVector(self, state):
        """state = boolean, show vector layers?"""
        self.__showVector = state
    
    showVector = property(fget=_showVector, fset=_setShowVector)

    def _showRaster(self):
        """return private attribute showRaster"""
        return self.__showRaster
    
    def _setShowRaster(self, state):
        """state = boolean, show raster layers?"""
        self.__showRaster = state
    
    showRaster = property(fget=_showRaster, fset=_setShowRaster)

    '''access to attributes stored in Storage'''
    def _klicnummer(self):
        """return klicnummer from storage"""
        if self.storage is not None:
            return self.storage.klicnummer

    klicnummer = property(fget=_klicnummer)
    
    def _meldingsoort(self):
        """return private attribute meldingsoort from storage"""
        if self.storage is not None:
            return self.storage.meldingsoort

    meldingsoort = property(fget=_meldingsoort)

    def _rectangle(self):
        """return private attribute rectangle from storage"""
        if self.storage is not None:
            return self.storage.rectangle

    rectangle = property(fget=_rectangle)

    def _graafpolygoon(self):
        """return private attribute graafpolygoon from storage"""
        if self.storage is not None:
            return self.storage.graafpolygoon

    graafpolygoon = property(fget=_graafpolygoon)
    
    def _netOwners(self):
        """return private attribute netOwners from storage"""
        if self.storage is not None:
            return self.storage.netOwners
    
    netOwners = property(fget=_netOwners)

    def _pdfFiles(self):
        """return private attribute pdfFiles from storage"""
        if self.storage is not None:
            return self.storage.pdfFiles
    
    pdfFiles = property(fget=_pdfFiles)

    def _layers(self):
        """return private attribute layerGroups from storage"""
        if self.storage is not None:
            return self.storage.layers
    
    layers = property(fget=_layers)

    def _xml_files(self):
        """gives back xml_files containing metadata"""
        sourceDir = self.path
        allFiles = os.listdir(sourceDir)
        xmlFiles =[]
        xmlFile = ""
        for x in allFiles:
            if ".xml" in x and not ".aux.xml" in x:
                xmlFile = x
                xmlFile = os.path.join(sourceDir,xmlFile)
                xmlFiles.append(xmlFile)
        return xmlFiles

    def _parse_xml_files(self, xmlFiles):
        """fill attributes of Doc from given xml files"""
        for xmlFile in xmlFiles:
            self._parse_xml(xmlFile)

    def _parse_xml(self, xmlFile):
        """fill attributes of Doc from a given xml file"""
        xml_stream = open(xmlFile, encoding="UTF-8")
        xml_element = ET.fromstring(xml_stream.read())
        tag = xml_utils.clean_tag(xml_element.tag)
        if tag == imkl.LEVERINGSINFORMATIE:
            self._process_tag_to_object(xml_element)
        elif tag == imkl.FEATURECOLLECTION and not imkl.BOUNDEDBY in self.imkls:
            xml_attributes = xml_element.attrib
            schemaKey = None
            for a_key in xml_attributes.keys():
                if 'schemaLocation' in a_key:
                    schemaKey = a_key
            if schemaKey in xml_attributes:
                self.schemaLocation = xml_element.attrib[schemaKey]
            for i_elem in xml_element:
                tag = xml_utils.clean_tag(i_elem.tag)
                if tag == imkl.BOUNDEDBY:
                    self._process_tag_to_object(i_elem)
                else:
                    self._process_feature_member(i_elem)
        else:
            
            # fix_print_with_import
            print("not processed tag: ", tag)
        xml_stream.close()

    def _process_feature_member(self, xml_element):
        for i_elem in xml_element:
            tag = xml_utils.clean_tag(i_elem.tag)
            self._process_tag_to_object(i_elem)
                
    def _process_tag_to_object(self, xml_element):
        tag = xml_utils.clean_tag(xml_element.tag)
##        print tag
        if tag in self._tag2function:
            function = self._tag2function[tag]
            obj = function()
            obj.process(xml_element)
            self._add_obj_to_imkl(tag, obj)
        else:
            # fix_print_with_import
            print("not processed tag: ", tag)

    def _add_obj_to_imkl(self, tag, obj):
        if tag in self.imkls:
            self.imkls[tag].append(obj)
        else:
            self.imkls[tag] = [obj]

    def _set_attributes_from_imkl(self):
        storage_version = self._storage_version_to_use()
        if storage_version == 1:
            self.storage = Storage1(self)
        elif storage_version == 2:
            self._post_process_imkl()
            self.storage = Storage2(self)
        else:
            return
        self.storage.fill()

    def _storage_version_to_use(self):
        storage_version = 0
        version = self.version
        if version == '1.5':
            storage_version = 1
        else:
            storage_version = 2
        return storage_version
        
    def _post_process_imkl(self):
        self._fill_keyed_imkl_set()
        self._set_klicnummer()
        self._set_geometry_pipes()
        self._set_short_values_from_url()
        self._set_themes_imkl_objects()
        self._fill_graaf_polygoon()

    def _fill_keyed_imkl_set(self):
        for imkl_set in list(self.imkls.values()):
            for imkl_object in imkl_set:
                if imkl_object.field("id") is not None:
                    key = imkl_object.field("id").value
                    self.imkls_on_id[key] = imkl_object

    def _set_klicnummer(self):
        imkl_obj = self.imkls[imkl.GEBIEDSINFORMATIEAANVRAAG][0]
        klicnummer = imkl_obj.field("klicnummer").value 
        for imkl_set in list(self.imkls.values()):
            for imkl_object in imkl_set:
                field = imkl_object.field("klicnummer")
                if field is not None and field.value is None:
                    field.value = klicnummer

    def _set_geometry_pipes(self):
        for tag in imkl.tags_pipes_and_cables():
            if tag in self.imkls:
                imkl_set = self.imkls[tag]
                for imkl_object in imkl_set:
                    geom_field = imkl_object.geometry_field()
                    link_coords = []
                    for link_id in imkl_object.link_ids:
                        if link_id not in self.imkls_on_id:
##                            self._display_no_utilitylink(imkl_object, link_id)
                            continue
                        utility_link = self.imkls_on_id[link_id]
                        utility_link.field_names()
                        geom_value = utility_link.geometry_field().value
                        link_coords.append(geom_value[10:])
                    new_value = 'MultiLineString('
                    new_value += ','.join(link_coords)
                    new_value += ')'
                    geom_field.value = new_value

    def _display_no_utilitylink(self, imkl_object, link_id):
        title = u"object has no utility link!"
        msg = u"object concerned: " + imkl_object.name + "\n"
        msg += "link_id: " + imkl_object.field("link_id").value + "\n"
        msg += "is missing in all utility links that stores geometry!"
        QMessageBox.information(None, title, msg)

    def _set_short_values_from_url(self):
        for imkl_set in list(self.imkls.values()):
            for imkl_object in imkl_set:
                for imkl_field in imkl_object.attribute_fields():
                     if imkl_field.from_attribute == 'Href' and imkl_field.value is not None:
                         url_value = imkl_field.value
                         short_value = self._get_last_value_from_url(url_value)
                         imkl_field.value = short_value
                     if imkl_field.name == "geom_id":
                         geom_id = imkl_field.value
                         if geom_id is not None and geom_id in self.imkls_on_id:
                             geom_object = self.imkls_on_id[geom_id]
                             geom_object.field("object").value = imkl_object.name

    def _set_themes_imkl_objects(self):
        for tag in list(self.imkls.keys()):
            imkl_set = self.imkls[tag]
            for imkl_object in imkl_set:
                if imkl_object.geometry_field() is None:
                    break
                theme_field = imkl_object.field("thema")
                if theme_field is None:
                    break
                if imkl_object.name == imkl.EIGENTOPOGRAFIE:
                    theme = "topo"
                else:
                    network_id = imkl_object.field("network_id").value
                    network = self.imkls_on_id[network_id]
                    theme = network.field("thema").value
                theme_field.value = theme
        
    def _fill_graaf_polygoon(self):
        polygon_key = None
        if imkl.GRAAFPOLYGOON in self.imkls:
            polygon_key = imkl.GRAAFPOLYGOON
        elif imkl.ORIENTATIEPOLYGOON in self.imkls:
            polygon_key = imkl.ORIENTATIEPOLYGOON
        graafpolygoon = self.imkls[polygon_key][0]
        aanvraag = self.imkls[imkl.GEBIEDSINFORMATIEAANVRAAG][0]
        levering = self.imkls[imkl.GEBIEDSINFORMATIELEVERING][0]
        field_names = ("registratiedatum", "vervaldatum",
                       "ordernummer","positienummer","klicnummer",
                       "referentie","aanvraagsoort","aanvraagdatum",
                       "soortWerkzaamheden","locatieWerkzaamheden",
                       "startDatum","eindDatum")
        self._copy_field_values_from_to_imkl(aanvraag,graafpolygoon,field_names)
        field_names = ("leveringsvolgnummer","datumLeveringSamengesteld",
                       "indicatieLeveringCompleet")
        self._copy_field_values_from_to_imkl(levering,graafpolygoon,field_names)        
 
    def _copy_field_values_from_to_imkl(self ,from_imkl_object, to_imkl_object, field_names):
        '''copies field values from imkl_object to imkl_object'''
        for field_name in field_names:
            self._copy_value_from_to_imkl(from_imkl_object, to_imkl_object,
                                          field_name)
            
    def _copy_value_from_to_imkl(self, from_imkl_object, to_imkl_object, field_name):
        '''copies field value from imkl_object to imkl_object'''
        from_field = from_imkl_object.field(field_name)
        to_field = to_imkl_object.field(field_name)
        if from_field is not None and to_field is not None:
            value = from_imkl_object.field(field_name).value
            to_field.value = from_field.value

    def _get_last_value_from_url(self, url):
        value = url
        if url is not None:
            if '/' in url:
                i = url.rindex('/')
                value = url[i+1:]
        return value


    def _setThemes(self):
        """
        fill attribute themes of doc from found themes for
        each netOwner. All themes are now accumulated in
        attribut themes and this will be used in dialog to
        present to user.
        """
        names_themes = self._gather_layernames_and_themes()
        netowners = self.netOwners
        if netowners is None:
            return
        for netOwner in netowners:
            for theme in netOwner.themes:
                nameTheme = theme.name
                #create theme for doc only once!!
                if nameTheme not in self.themes:
                    self.themes[nameTheme] = Theme(self, nameTheme)
                    # now traverse all my layers to add layer to this theme.
                    findString = ''.join(nameTheme.split(' ')).lower()
                    for layername, layer in list(self.layers.items()):
                        layername_splitted = layername.split('_')
                        theme_in_layername = ""
                        if len(layername_splitted) > 1:
                            theme_in_layername = layername_splitted[1]
                        else:
                            theme_in_layername = layername_splitted[0]
                        theme_in_layer = ''.join(theme_in_layername.split('+')).lower()
                        add_layer = False
                        if layername is not None and findString == theme_in_layer:
                            add_layer = True
                        if layername in names_themes and nameTheme in names_themes[layername]:
                            add_layer = True
                        if add_layer:
                            self.themes[nameTheme].layers.append(layer)
        self._setLayerGroupThemes()
        self._set_themes_to_layers()
        self._allLayersHaveThemes()

    def _set_themes_to_layers(self):
        names_themes = self._gather_layernames_and_themes()
        for theme in list(self.themes.values()):
            for layer in theme.layers:
                name_layer = layer.layerName
                if layer.is_vector() and name_layer in names_themes:
                    for theme_name in names_themes[name_layer]:
                        if theme_name not in layer.themes_visible:
                            layer.addVisibility(theme_name)

    def _gather_layernames_and_themes(self):
        names_themes = {}
        for imkl_objects in list(self.imkls.values()):
            name_object = imkl_objects[0].name
            for imkl_object in imkl_objects:
                theme_field = imkl_object.field('thema')
                if theme_field is not None:
                    name_theme = theme_field.value.lower()
                    if name_object in names_themes:
                        if name_theme not in names_themes[name_object]:
                            names_themes[name_object].append(name_theme)
                    else:
                        names_themes[name_object] = [name_theme]
        return names_themes   
        
    def _allLayersHaveThemes(self):
        for theme in list(self.themes.values()):
            for layer in theme.layers:
                if len(layer.themes_visible) == 0:
                    layer.addVisibility(theme.name)                    

    def _setLayerGroupThemes(self):
        """
        Create themes for annotation, dimensioning, location and topo and
        add layers. These are not delivered themes by customer but these
        are special themes that have been added to turn on/off visibility for
        these visibility groups.
        """
        dict_layers = self.layers
        if dict_layers is None:
            return
        for layerGroupName in list(Layer.layerGroupNames.keys()):
            self.themes[layerGroupName] = Theme(self, layerGroupName)
        for layer in list(dict_layers.values()):
            if layer.groupName() in self.themes:
                self.themes[layer.groupName()].layers.append(layer)
            else:
                pass
##                self._display_no_groupname(layer)

    def _display_no_groupname(self, layer):
        title = u"layer has not a (valid) groupname"
        msg = u"layer concerned: " + layer.layerName + "\n"
        msg += "group name: " + layer.groupName() + "\n"
        msg += "Not in: "
        for layerGroupName in list(Layer.layerGroupNames.keys()):
            msg += layerGroupName + "\n"
        QMessageBox.information(None, title, msg)

    def _createWorldFiles(self):
        """
        For each png image create an ESRI world file.
        This in fact turns the image to a map, because now it can
        be loaded in QGIS as a raster map.
        """
        dict_layers = self.layers
        if dict_layers is None:
            return
        for layer in list(dict_layers.values()):
            if not layer.vectorType:
                pngFile = layer.layerFile
                pngAuxFile = pngFile + '.aux.xml'
##                if not os.path.isfile(pngAuxFile):
                f=open(pngAuxFile, 'w')
                f.write(self.rectangle.worldFileData())
                f.close()

    def loadLayers(self):
        """Load all layers into QGIS"""
        layers_sorted = self.layersSorted()
        if layers_sorted is None:
            return
        for layer in layers_sorted:
            layer.load()

    def layersSorted(self):
        dict_layers = self.layers
        if dict_layers is None:
            return
        layers = [layer for layer in list(self.layers.values())]
        layers.sort()
        return layers        

    def goto(self):
        """
        Zoom to the extent of the first layer which is in fact
        the Background Topo provided by Dutch mapping agency Kadaster.
        """
        l_layer = self.getFirstLayer()
        if l_layer != None:
            l_layer.goto()

    def bestScale(self):
        """
        Zoom to the best scale of the first layer which is in fact
        the Background Topo provided by Dutch mapping agency Kadaster.
        """
        l_layer = self.getFirstLayer()
        if l_layer != None:
            l_layer.bestScale()

    def getFirstLayer(self):
        """
        returns first layer which is in fact Background Topo
        provided by Dutch mapping agency Kadaster
        """
        l_firstLayer = None
        l_layers = self.layersSorted()
        if l_layers != None and len(l_layers) > 0:
            l_firstLayer = l_layers[0]
        return l_firstLayer

    def removeLayers(self):
        """
        removes all layers
        """
        for i_layer in self.layers.values():
            i_layer.remove()

    def pickle(self):
        """
        return object which easily can be written to textfile
        using pickle module, it should be completely detached from QGIS.  
        """
        l_doc = Doc(self.path)
        l_doc.layers = []
        # use also copies of layers that can be stored to text file
        # using pickle.
        for i_layer in self.layers:
            l_doc.layers.append(i_layer.pickle())
        # do the same for themes!
        for i_theme_name, i_theme in self.themes.items():
            l_doc.themes[i_theme_name] = i_theme.pickle(l_doc.layers)
        # for now we do not mind to store and restore netOwners to old state
        # because it is not used directly by menu. It was vital
        # however as a container of information when reading information
        # from xml file.
##        l_doc.netOwners = self.netOwners[:]
        l_doc.klicnummer = self.klicnummer
        l_doc.meldingsoort = self.meldingsoort
        l_doc.polygon = self.polygon
        l_doc.rectangle = self.rectangle
        l_doc.pdfFiles = self.pdfFiles[:]
        l_doc.layerGroups = self.layerGroups
        return l_doc

    def attachLayers(self):
        """
        attaches layer back to QGIS again.
        Layers are allready loaded in right order and we just need
        to set right reference back to each layer.
        """
        l_iface = self.iface
        if l_iface != None:
            lyrs = l_iface.loadedLayers()
            for i_lyr in self.layers:
                i_lyr.layer = lyrs[i_lyr.layerId]
                i_lyr.owner = self
                
    def attachThemes(self):
        """
        attaches owner back to themes again.
        owner is neccesary for several actions, with owner
        doc object the pickle module can not store doc to textfile.
        """
        l_iface = self.iface
        if l_iface != None:
            lyrs = l_iface.loadedLayers()
            for i_theme in self.themes.values():
                i_theme.owner = self
                for i_lyr in i_theme.layers:
                    i_lyr.layer = lyrs[i_lyr.layerId]
                    i_lyr.owner = self
