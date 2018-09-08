"""
/***************************************************************************
wv (Wion Viewer)
Holds all classes to hold all references to full WION reply                             -------------------
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

import os, wv
import xml.etree.ElementTree as ET
from core import imkl, xml_utils
from qgis.core import QgsGeometry

#import xml2obj

WIN = "startfile" in dir(os)
Ubuntu = os.environ.get('GNOME_DESKTOP_SESSION_ID') != None


##msg_dir = os.path.join(os.path.dirname(wv.__file__), "testMsg\\09G267447_1")
"""hold path to directory with test message, to be used for testing purposes only!!

using doc_test with >> python wv.py -v
official test result message is downloaded from www.klicviewer.nl, unpacked in
testfolder and this module attribute msg_dir will be set. Then used in doc_tests..
"""

class Doc():
    def __init__(self, path_message):
        """path_message = full path to directory which holds result of WION message.
        Creates instance of Doc which holds all information of WION result.
        Creates whole structure using XML file in given directory.
        Creates world files that are used in GIS systems to show rasterfiles.
        Interface to GIS is delegated to attribute iface.
        
        usage:
        >>> l_doc = Doc(msg_dir)
        >>> l_doc.version
        '1.5'
        >>> l_doc.klicnummer
        '14G166926'
        >>> l_doc.meldingsoort
        'Graafmelding'
        >>> l_doc.netOwners
        [Company('Liander'), Company('APELDOORN'), Company('Eurofiber'), Company('KPN'), Company('Reggefiber'), Company('Tele2'), Company('trent'), Company('upc'), Company('Vitens')]
        >>> l_doc.layers
        [Layer('GB_14G166926.png'), Layer('ET_KPN_0000546663_14G166926.png'), Layer('ET_Liander_0000574962_14G166926.png'), Layer('PT_KPN_0000546663_14G166926.png'), Layer('LG_datatransport_KPN_0000546663_14G166926.png'), Layer('LG_datatransport_trent_0000585212_14G166926.png'), Layer('LG_gas+lage+druk_Liander_0000574962_14G166926.png'), Layer('LG_laagspanning_Liander_0000574962_14G166926.png'), Layer('LG_middenspanning_Liander_0000574962_14G166926.png'), Layer('LG_riool+vrijverval_APELDOORN_0000586326_14G166926.png'), Layer('LG_water_Vitens_0000552354_14G166926.png'), Layer('MV_datatransport_KPN_0000546663_14G166926.png'), Layer('MV_datatransport_trent_0000585212_14G166926.png'), Layer('MV_gas+lage+druk_Liander_0000574962_14G166926.png'), Layer('MV_laagspanning_Liander_0000574962_14G166926.png'), Layer('MV_middenspanning_Liander_0000574962_14G166926.png'), Layer('AN_datatransport_KPN_0000546663_14G166926.png'), Layer('AN_datatransport_trent_0000585212_14G166926.png'), Layer('AN_gas+lage+druk_Liander_0000574962_14G166926.png'), Layer('AN_laagspanning_Liander_0000574962_14G166926.png'), Layer('AN_middenspanning_Liander_0000574962_14G166926.png'), Layer('AN_water_Vitens_0000552354_14G166926.png')]
        """

        # holds folder used to create whole structure
        self.__path = os.path.realpath(path_message)
        # holds interface to gis.   
        self.__iface = None
        # holds all information in imkl objects
        self.imkls = {}
        self.layers = []
        self.version = None
        self.klicnummer = None
        self.meldingsoort = None
        self.polygon = None
        self.rectangle = None
        self.netOwners = []
        self.pdfFiles = []
        self.layerGroups = {}
        self.themes = {}
        # find and read xml file holding metadata
        xml_files = self._xml_files()
        self._parse_xml_files(xml_files)
        # set layers and create world files
        self._setLayers()
        self._setAdditionalFiles()
        self._setThemes()
        self._createWorldFiles()

# defining access to attributes of class Layer

    def _iface(self):
        """return private attribute iface"""
        return self.__iface
    
    def _setIface(self, iface):
        """set private attribute iface"""
        # set it only once
        if self.__iface == None:
            self.__iface  = iface
    
    iface = property(fget=_iface, fset=_setIface)
        
    def _path(self):
        """return privat attribute path"""
        return self.__path

    path = property(fget=_path)
    
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
##        print(xmlFiles)
        return xmlFiles

    def _parse_xml_files(self, xmlFiles):
        """fill attributes of Doc from given xml files"""
        for xmlFile in xmlFiles:
            self._parse_xml(xmlFile)
            self._set_attributes_from_imkl()

    def _parse_xml(self, xmlFile):
        """fill attributes of Doc from a given xml file"""
        xml_stream = open(xmlFile)
        xml_element = ET.fromstring(xml_stream.read())
        tag = xml_utils.clean_tag(xml_element.tag)
##        print "tag = ", tag
        if tag == "Leveringsinformatie":
            obj = imkl.leveringsinformatie()
            obj.process(xml_element)
            self.imkls[tag] = obj
        xml_stream.close()

    def _set_attributes_from_imkl(self):
        if self.imkls.has_key("Leveringsinformatie"):
            imkl_obj = self.imkls["Leveringsinformatie"]
            self._set_from_old_imkl(imkl_obj)
        else:
            for imkl_obj in self.imkls.items():
                self._set_from_imkl(imkl_obj)

    def _set_from_imkl(self, imkl_obj):
        pass

    def _set_from_old_imkl(self, imkl_obj):
##        print "in _set_from_old_imkl()"
        self.version = imkl_obj.field("version").value
        self.klicnummer = imkl_obj.field("klicnummer").value
        self.meldingsoort = imkl_obj.field("meldingsoort").value
        self.polygon = imkl_obj.field("graafpolygoon").value
        omsluitende_rechthoek = imkl_obj.field("omsluitendeRechthoek").value
        wkt = omsluitende_rechthoek.field("omsluitendeRechthoek").value
        width = omsluitende_rechthoek.field("pixelsBreed").value
        height = omsluitende_rechthoek.field("pixelsHoog").value
        self.rectangle = Rectangle()
        self.rectangle.setFromWkt(wkt)
        self.rectangle.pixelsWidth = int(width)
        self.rectangle.pixelsHeight = int(height)
        netowner_deliveries = imkl_obj.field("netbeheerderLeveringen").value
        for netowner_delivery in netowner_deliveries:
            self._process_netowner_delivery(netowner_delivery)

    def _process_netowner_delivery(self, netowner):
##        print "in _process_netowner_delivery()"
        netOwner = Company()
        netOwner.name = netowner.field("bedrijfsnaam").value
        netOwner.shortName = netowner.field("bedrijfsnaam").value
        netOwner.telNrProblemIT = netowner.field("storingsnummer").value
        netOwner.telNrDamage = netowner.field("beschadigingsnummer").value
        
        contactpersoon = netowner.field("contactpersoon").value
        if contactpersoon is not None:
            person = self._process_person(contactpersoon)
            netOwner.contactPerson = person
            
        imkl_themes = netowner.field("themas").value
        if imkl_themes is not None:
            themes = self._process_themes(imkl_themes)
            netOwner.themes = themes

        imkl_docs = netowner.field("bijlagen").value
        if imkl_docs is not None:
            docs = self._process_imkl_docs(imkl_docs)
            self.pdfFiles.extend(docs)

        for topo_name in ("topo", "plan_topo"):
            imkl_topo = netowner.field(topo_name).value
            if imkl_topo is not None:
                filename = imkl_topo.field("bestandsnaam").value
                layer_file = os.path.join(self.path, filename)
                self.layers.append(Layer(self, layer_file))

        self.netOwners.append(netOwner)

    def _process_person(self, imkl_person):
        person = None
        if imkl_person is not None:
            person = Person()
            person.name = imkl_person.field("naam").value
            person.telephone = imkl_person.field("telefoon").value
            person.email = imkl_person.field("email").value
            person.fax = imkl_person.field("fax").value
        return person
                
    def _process_themes(self, imkl_themes):
        """
        process a list of imkl_themes and return a list of wv.Theme objects
        """
        themes = []
        for imkl_theme in imkl_themes:
            theme = self._process_theme(imkl_theme)
            themes.append(theme)
        return themes

    def _process_theme(self, imkl_theme):
        theme = Theme(self)
        theme.name = imkl_theme.field("themanaam").value
        theme.supervisionNecessary = imkl_theme.field("eisVoorzorgmaatregel").value
        imkl_toezichthouders = imkl_theme.field("toezichthouders").value
        if imkl_toezichthouders is not None:
            persons = self._process_persons(imkl_toezichthouders)
            theme.supervisors = persons
        theme._set_theme_layers(self.path, imkl_theme)
        theme._set_theme_docs(self.path, imkl_theme)
        return theme

    def _process_persons(self, imkl_persons):
        persons = []
        for imkl_person in imkl_persons:
            person = self._process_person(imkl_person)
            persons.append(person)
        return persons

    def _process_imkl_docs(self, imkl_docs):
        docs = []
        for imkl_doc in imkl_docs:
            pdf_name = imkl_doc.field("bestandsnaam").value
            pdf_file = PdfFile(pdf_name)
            pdf_file.type = imkl_doc.name
            pdf_file.filePath = os.path.join(self.path, pdf_name)
            docs.append(pdf_file)
        return docs

    def _setLayers(self):
        """
        using set attribute path of dig alert message find all
        image files of type png, then sort them into the right layer
        priority so when we load them they are loaded in exactly
        the right order. 
        """
        # find pgn files in themes
        layers = []
        for netowner in self.netOwners:
            for theme in netowner.themes:
                layers.extend(theme.layers)
        # add 1 layer not included in xml (but it should be included!)
        kadaster_png =  'GB_' + self.klicnummer + '.png'
        file_png = os.path.join(self.path, kadaster_png)
        layer = Layer(self, file_png)
        layers.append(layer)
        # set attribute layers with sorted list op PNG files.
        self.layers.extend(layers)
        self.layers.sort()
        
    def _setAdditionalFiles(self):
        """
        using set attribute path of dig alert message find all
        pdf files that we want to list and show to user.
        Again these are sorted in groups so it will be easy for
        user to find quickly right document.
        """
        # find pdf files in themes
        for theme in self.themes:
            self.pdFiles.extend(theme.pdf_files)
        self.pdfFiles.sort()

    def _setThemes(self):
        """
        fill attribute themes of doc from found themes for
        each netOwner. All themes are now accumulated in
        attribut themes and this will be used in dialog to
        present to user.
        """
        for i_netOwner in self.netOwners:
            for i_theme in i_netOwner.themes:
                l_nameTheme = i_theme.name
                #create theme for doc only once!!
                if not self.themes.has_key(l_nameTheme):
                    self.themes[l_nameTheme] = Theme(self, l_nameTheme)
                    # now traverse all my layers to add layer to this theme.
                    l_findString = l_nameTheme.replace(' ', '+')
                    for i_layer in self.layers:
                        if l_findString in i_layer.layerName():
                            self.themes[l_nameTheme].layers.append(i_layer)
        self._setLayerGroupThemes()

    def _setLayerGroupThemes(self):
        """
        Create themes for annotation, dimensioning, location and topo and
        add layers. These are not delivered themes by customer but these
        are special themes that have been added to turn on/off visibility for
        these visibility groups.
        """
        for i_layerGroupName in Layer.layerGroupNames.iterkeys():
            self.themes[i_layerGroupName] = Theme(self, i_layerGroupName)
        for i_layer in self.layers:
            self.themes[i_layer.groupName()].layers.append(i_layer)

    def _createWorldFiles(self):
        """
        For each png image create an ESRI world file.
        This in fact turns the image to a map, because now it can
        be loaded in QGIS as a raster map.
        """
        for i_layer in self.layers:
            l_pngFile = i_layer.layerFile
            l_pngAuxFile = l_pngFile + '.aux.xml'
            if not os.path.isfile(l_pngAuxFile):
                f=open(l_pngAuxFile, 'w')
                f.write(self.rectangle.worldFileData())
                f.close()

    def loadLayers(self):
        """Load all layers into QGIS"""
        for i_layer in self.layers:
            i_layer.load()

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
        l_layers = self.layers
        if l_layers != None and len(l_layers) > 0:
            l_firstLayer = l_layers[0]
        return l_firstLayer

    def removeLayers(self):
        """
        removes all layers
        """
        for i_layer in self.layers:
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
        for i_theme_name, i_theme in self.themes.iteritems():
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
            for i_theme in self.themes.itervalues():
                i_theme.owner = self
                for i_lyr in i_theme.layers:
                    i_lyr.layer = lyrs[i_lyr.layerId]
                    i_lyr.owner = self
            
class Layer:

    layerPriority=("GB_", "ET_", "PT_", "LG_" ,"MV_", "AN_")
    layerGroupNames= {"Topo": ("GB_", "ET_", "PT_"),
                      "Ligging": ("LG_",),
                      "Maatvoering": ("MV_",),
                      "Annotatie": ("AN_",)}
        
    def __init__(self, owner, raster_file_name):
        self.owner = owner
        self.__file = raster_file_name
        self.__layer = None # reference to realised layer in GIS
        self.__layerId = None # reference to layerID in GIS
        self.__visible = False # state in GIS
        self.__layerName = None # holds layername

# defining access to attributes of class Layer

    def _layerFile(self):
        """return private attribute file which holds filename"""
        return self.__file

    layerFile = property(fget=_layerFile)

    def _layer(self):
        """return private attribute layer"""
        return self.__layer

    def _setLayer(self, layer):
        """set private attribute layer"""
        # set it only once
        if self.__layer == None:
            self.__layer = layer

    layer = property(fget=_layer, fset=_setLayer)

    def _layerId(self):
        """ get private attribute layer id"""
        return self.__layerId

    layerId = property(fget=_layerId)

    def _visible(self):
        """return private attribute visible"""
        return self.__visible

    visible = property(fget=_visible)

# special methods of class Layer
    def __repr__(self):
        """Simple presentation of class Layer"""
        return "Layer('%s')" % (self.layerName())
    
    def __cmp__(self, other):
        """sort layers on prefix name"""
        if other is None:
            return 1
        l_this_name = self.layerName()
        l_other_name = other.layerName()
        l_this_index = 0
        l_other_index = 0
        l_index=0
        for compareStr in self.layerPriority:
            if l_this_name.startswith(compareStr):
                l_this_index = l_index
            if l_other_name.startswith(compareStr):
                l_other_index = l_index
            l_index += 1
        l_order_ok = -1
        if l_this_index > l_other_index:
            l_order_ok = 1
        elif l_this_index == l_other_index and l_this_name > l_other_name:
            l_order_ok = 1
        elif l_this_index == l_other_index and l_this_name == l_other_name:
            l_order_ok = 0
                
        return l_order_ok

# Public methods of class Layer
    def layerName(self):
        """return filename without path"""
        if self.__layerName is None:
            i = self.layerFile.rindex(os.sep)
            self.__layerName = self.layerFile[i+1:]
        return self.__layerName

    def load(self):
        """
        loads layer and set attributes layer, layer_id & visible 
        """
        iface = self.owner.iface
        if iface != None:
            self.__layer = iface.loadLayer(self)
            self.__layerId = unicode(iface.getLayerIdForLayer(self))
            self.__visible = True

    def pickle(self):
        """
        returns myself as an object that can be written to textfile
        using the pickle module.
        A copy is returned with no ties to quantum gis or owner (Doc)
        """
        l_layer = Layer(None, self.__file)
        l_layer.__layerId = self.__layerId
        l_layer.__visible = self.__visible
        l_layer.__layerName = self.__layerName
        return l_layer
        
    def setVisibility(self, pVisibility):
        """
        p_visibility = boolean used to set this layer 
        change visibility in set of layers
        """
        iface = self.owner.iface
        l_visible = self.isVisible()
        if iface != None and l_visible != pVisibility:
            iface.setVisibilityForLayer(self, pVisibility)
            self.__visible = pVisibility

    def isVisible(self):
        """
        Checks if layer is visible, sets private __visible
        and returns boolean layer is visible or not
        """
        iface = self.owner.iface
        if iface != None:
            l_visible = iface.visibilityForLayer(self)
            self__visible = l_visible
        return l_visible

    def goto(self):
        """
        goto bounds of layer
        the interface of Doc is used.
        """
        iface = self.owner.iface
        if iface != None:
            iface.gotoLayer(self)

    def remove(self):
        """
        remove layer from mapRegistry
        this will in fact remove the layer from QGIS
        """
        iface = self.owner.iface
        if iface != None:
            iface.removeLayer(self)

    def bestScale(self):
        """
        Set best scale for layer 
        """
        iface = self.owner.iface
        if iface != None:
            iface.bestScale(self)

    def groupName(self):
        """
        returns name of group this layer belongs to being one of
        Ligging, Maatvoering, Annotatie or Topo
        """
        l_groupName = ""
        l_prefix = self.layerName()[:3]
        for i_groupName, i_prefixes in self.layerGroupNames.iteritems():
            if l_prefix in i_prefixes:
                l_groupName = i_groupName
                break
        return l_groupName

class Coord:
    def __init__(self, p_x=0, p_y=0):
        """Initialises new instance of Coord with optional x & y value

        >>> c1 = Coord(4,5)
        >>> c1.x
        4
        >>> c1.y
        5
        >>> c1.x = 6
        >>> c1.x
        6
        """
        self.x = p_x
        self.y = p_y
        
    def __repr__(self):
        """"Return string representation of Coord"""
        return "Coord(%.2f, %.2f)" % (self.x, self.y)

class Rectangle:
    """Class which represents rectangular area which hold
    position of rasters in the world. Used to create contents of
    worldfile that will be created next to each rasterfile.
    """

# following shared template needs to be completed with following values
# x1, pixel_width,0 ,y2 ,0 -pixel_height
    worldFileTemplate = "<PAMDataset>\
<SRS>PROJCS[&quot;Amersfoort / RD New&quot;,GEOGCS[&quot;Amersfoort&quot;,\
DATUM[&quot;Amersfoort&quot;,SPHEROID[&quot;Bessel 1841&quot;,\
6377397.155,299.1528128,AUTHORITY[&quot;EPSG&quot;,&quot;7004&quot;]],\
AUTHORITY[&quot;EPSG&quot;,&quot;6289&quot;]],PRIMEM[&quot;Greenwich&quot;,0,\
AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;,\
0.01745329251994328,AUTHORITY[&quot;EPSG&quot;,&quot;9122&quot;]],\
AUTHORITY[&quot;EPSG&quot;,&quot;4289&quot;]],UNIT[&quot;metre&quot;,\
1,AUTHORITY[&quot;EPSG&quot;,&quot;9001&quot;]],PROJECTION[&quot;\
Oblique_Stereographic&quot;],PARAMETER[&quot;latitude_of_origin&quot;,\
52.15616055555555],PARAMETER[&quot;central_meridian&quot;,5.387638888888889],\
PARAMETER[&quot;scale_factor&quot;,0.9999079],PARAMETER[&quot;false_easting\
&quot;,155000],PARAMETER[&quot;false_northing&quot;,463000],\
AUTHORITY[&quot;EPSG&quot;,&quot;28992&quot;],AXIS[&quot;X&quot;,EAST],\
AXIS[&quot;Y&quot;,NORTH]]</SRS>\
<GeoTransform> %8.2f, %e, 0, %8.2f, 0,%e</GeoTransform>\
<PAMRasterBand band=\"1\"><NoDataValue>255</NoDataValue>\
</PAMRasterBand></PAMDataset>"        

    def __init__(self, lowerLeftCoord=Coord(), upperRightCoord=Coord()):
        """Initialises new instance of Rectangle with optional lowerLeftCoord
        & upperRightCoord

        usage:
        >>> l_doc = Doc(msg_dir)
        >>> r = l_doc.rectangle
        >>> r
        Rectangle(Coord(194154.00, 465849.00), Coord(194270.00, 465914.00))
        >>> r.lowerLeftCorner
        Coord(194154.00, 465849.00)
        >>> r.upperRightCorner
        Coord(194270.00, 465914.00)
        >>> r.pixelsWidth
        1624
        >>> r.pixelsHeight
        910
        """
        self.lowerLeftCorner = lowerLeftCoord
        self.upperRightCorner = upperRightCoord
        self.pixelsWidth = None
        self.pixelsHeight = None

    def __repr__(self):
        """Represenation of rectangle that can be used to reproduce object"""
        return "Rectangle(%s, %s)" % (self.lowerLeftCorner, self.upperRightCorner)

    def setFromWkt(self, wkt):
        """set lowerLeftCorner or upperRightCorner from polyon in WKT format
        """
##        print "wkt: ", wkt
        geom = QgsGeometry.fromWkt(wkt)
        bb = geom.boundingBox()
        self.lowerLeftCorner = Coord(bb.xMinimum(), bb.yMinimum())
        self.upperRightCorner = Coord(bb.xMaximum(), bb.yMaximum())

    def worldFileParameters(self):
        """returns essential parameters needed to create world files

        >>> r = Rectangle()
        >>> r.lowerLeftCorner = Coord(196723.0, 311495.0)
        >>> r.upperRightCorner = Coord(196970.0, 311731.0)
        >>> r.pixelsWidth = 3458
        >>> r.pixelsHeight = 3304
        >>> r.worldFileParameters()
        (196723.0, 0.07142857142857142, 311731.0, -0.07142857142857142)
        """
        ll = self.lowerLeftCorner
        ur = self.upperRightCorner
        x1 = ll.x
        y1 = ll.y
        x2 = ur.x
        y2 = ur.y
        width = x2-x1
        height = y2-y1
        l_pixelWidth = width/self.pixelsWidth
        l_pixelHeight = height/self.pixelsHeight
        return x1, l_pixelWidth, y2, -l_pixelHeight

    def worldFileData(self):
        """ contents of world files"""
        return self.worldFileTemplate % self.worldFileParameters()
    
    
class Company:
    def __init__(self, name=None):
        """Company which represents the netowner.
        The netowner provide all information, including contactpersons
        rasters with positions of pipeline, pdf's with accompanying letters
        additional drawings etcetera...

        usage:
        >>> l_doc = Doc(msg_dir)
        >>> l_company = l_doc.netOwners[0]
        >>> l_company
        Company('Liander')
        >>> l_company.name
        'Liander'
        >>> l_company.shortName
        'Liander'
        >>> l_company.telNrDamage
        >>> l_company.telNrProblemIT
        '0800-9009'
        >>> l_company.contactPerson
        Person('Gis Data Klic')
        >>> l_company.themes
        [Theme('middenspanning'), Theme('gas lage druk'), Theme('laagspanning')]
        """
        self.name = name
        self.shortName = None
        self.telNrProblemIT = None
        """Telephone nr to call when raster/information seems incorrect"""
        self.telNrDamage = None
        """Telephone nr to call when pipe/cable is damaged"""
        self.contactPerson = None
        self.themes = []

    def __repr__(self):
        return "Company('%s')" % self.name

class Person:
    def __init__(self, name=None):
        """Person which can be a contactperson from the netowner.
        It can hold information like name/email/telnr/fax

        usage:
        >>> l_doc = Doc(msg_dir)
        >>> l_doc.netOwners
        [Company('Liander'), Company('APELDOORN'), Company('Eurofiber'), Company('KPN'), Company('Reggefiber'), Company('Tele2'), Company('trent'), Company('upc'), Company('Vitens')]
        >>> l_company = l_doc.netOwners[0]
        >>> l_company
        Company('Liander')
        >>> l_person = l_company.contactPerson
        >>> l_person
        Person('Gis Data Klic')
        >>> l_person.name
        'Gis Data Klic'
        >>> l_person.email
        'infoklic@alliander.com'
        >>> l_person.telephone
        '0611382570'
        >>> l_person.fax
        """
        self.name = name
        self.telephone = None
        self.email = None
        self.fax = None

    def __repr__(self):
        return "Person('%s')" % self.name


class Theme:
    visibilities = ("None", "Some", "All")
    
    def __init__(self, p_owner, p_name=None):
        """Theme presenting a kind of network, like water or datatransport
        Holds also information if supervision is neccesary during works i.e.
        for Gas pipelines and information on supervisor that will attend.

        usage:
        >>> l_doc = Doc(msg_dir)
        >>> l_cmp = l_doc.netOwners[0]
        >>> l_cmp
        Company('Liander')
        >>> l_cmp.themes
        [Theme('middenspanning'), Theme('gas lage druk'), Theme('laagspanning')]
        >>> t = l_cmp.themes[0]
        >>> t
        Theme('middenspanning')
        >>> t.name
        'middenspanning'
        >>> t.supervisionNecessary
        'false'
        >>> t.supervisors
        [Person('None')]
        """
        self.owner = p_owner
        self.name = p_name
        self.supervisionNecessary = None
        self.supervisors = []
        self.layers = []
        self.pdf_docs = []
        self.__visible = 0

    def __repr__(self):
        return "Theme('%s')" % self.name

    def _visible(self):
        """return private attribute visible"""
        return self.visibilities[self.__visible]

    visible = property(fget=_visible)

    def pickle(self, l_pickled_layers):
        """
        returns myself as an object that can be written to textfile
        using the pickle module.
        A copy is returned with no ties to quantum gis or owner (Doc)
        """
        l_theme = Theme(None, self.name)
        l_theme.supervisionNecessary = self.supervisionNecessary
        l_theme.supervisors = self.supervisors[:] # make a copy of list
        # currently layers are referenced objects used in doc.layers and
        # theme.layers, so they are used in two places. We do not want to
        # pass the same layer objects twice.. this could otherwise end up in
        # really hard to solve bugs in the future..
        for i_layer in self.layers:
            for i_pickled_layer in l_pickled_layers:
                if  i_pickled_layer.layerId == i_layer.layerId:
                    l_theme.layers.append(i_pickled_layer)
                    break
        l_theme.__visible = self.__visible
        return l_theme

    def checkVisible(self, p_actual=False):
        """
        p_actual, optional argument if true visibility
        of layers belonging to theme is actually checked otherwise
        recorded visible state of layers is used.
        """
        l_len = len(self.layers)
        l_nVisible = 0
        l_visible = 0
        # using True == 1 for addition!
        for i_layer in self.layers:
            if p_actual:
                l_nVisible += i_layer.isVisible()
            else:
                l_nVisible += i_layer.visible
        # now check result!!
        if l_nVisible == 0:
            l_visible = 0
        elif l_nVisible == l_len:
            l_visible = 2
        else:
            l_visible = 1
        self.__visible = l_visible    
        return l_visible

    def setVisibility(self, p_visibility):
        """
        p_visibility = boolean used to set same visibility for  
        this theme (all on or all off!)
        """
        iface = self.owner.iface
        if iface != None:
            iface.doRendering(False)
        for i_layer in self.layers:
            i_layer.setVisibility(p_visibility)
        if iface != None:
            iface.doRendering()
            iface.refreshMap()
            
        # refresh state of visibility and return!
        # Result value should be 0 (all off) or 2 (all on)
        return self.checkVisible()

    def _set_theme_layers(self, msg_dir, imkl_theme):
        layer_names = [name.lower() for name in Layer.layerGroupNames.keys()]
        layer_names.remove("topo")
        for layer_name in layer_names:
            imkl_layer = imkl_theme.field(layer_name).value
            if imkl_layer is not None:
                layer_file = imkl_layer.field('bestandsnaam').value
                layer_file = os.path.join(msg_dir, layer_file)
                self.layers.append(Layer(self, layer_file))

    def _set_theme_docs(self, msg_dir, imkl_theme):
        pdf_files = []
        pdf_fields = ("detailkaarten", "huisaansluitschetsen", "themaBijlagen")
        for pdf_field in pdf_fields:
            a_container = imkl_theme.field(pdf_field).value
##            print pdf_field, a_container
            if a_container is not None:
##                print a_container
                for pdf_object in a_container:
                    file_name = pdf_object.field("bestandsnaam").value
                    pdfFile = PdfFile(file_name)
                    pdfFile.type = pdf_object.name
                    pdfFile.filePath = os.path.join(msg_dir, file_name)
                    self.pdf_docs.append(pdfFile)     

class PdfFile:
    def __init__(self, name=None):
        self.type = None
        self.name = name
        self.filePath = None

    def __repr__(self):
        return "PdfFile('%s')" % (self.name)
    
    def __cmp__(self, other):
        """sort pdfFile on type and name"""
        
        l_this_type = self.type
        l_other_type = other.type
        l_this_name = self.name
        l_other_name = other.name
        
        l_order = 0 # equal
        if l_this_type > l_other_type:
            l_order = 1
        elif l_this_type < l_other_type:
            l_order = -1
        else:
            if l_this_name > l_other_name:
                l_order = 1
            elif l_this_name < l_other_name:
                l_order = -1
        return l_order
    
    def openPdf(self):
        """open the pdf file"""
        l_file = self.filePath
        if WIN:
            os.startfile(l_file)
        elif Ubuntu:
            os.system('gnome-open %s' % l_file)
        else:
            os.system('open %s' % l_file)

class LayerGroup:
    def __init__(self, name=None):
        """
        Layer group holds information on name and groupIndex
        """
        self.name = name
        self.index = None

    def __repr__(self):
        return "LayerGroup('%s')" % self.name

        
if __name__ == "__main__":
    import os, doctest, wv
    l_my_dir = os.path.dirname(wv.__file__)
    l_test_dir = os.path.join(l_my_dir,"testMsg")
    print "test_dir:", l_test_dir
    if not os.path.exists(l_test_dir):
        os.mkdir(l_test_dir)
    msg_dir = os.path.join(l_test_dir,"14G166926_1")
    if not os.path.exists(msg_dir):
        # download and unzip testmsg in testdir
        import urllib2, zipfile
        url = "https://www.kadaster.nl/documents/20838/87975/\
KLIC+proefbestand+Klic+viewer/0ffdb475-bd96-43c6-bf71-d639bad14a1c"
        l_remote_file = urllib2.urlopen(url)
        #l_file_name = os.path.join(l_test_dir,os.path.basename(url))
        l_file_name = os.path.join(l_test_dir,os.path.basename(url))
        l_file = open(l_file_name, "wb")
        l_file.write(l_remote_file.read())
        l_file.close()
        z = zipfile.ZipFile(l_file_name)
        z.extractall(l_test_dir)
        z.close
    doctest.testmod()
