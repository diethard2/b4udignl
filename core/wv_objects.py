"""
/***************************************************************************
wv_objects (Wion Viewer)
begin                : 2018-09-15 
copyright            : (C) 2018 by Diethard Jansen
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

Holds different classes to store and process imkl to content used by wv.doc.
It is an integral part of wv, but choosen is to separate the wv.doc and other
wv.objects.

Author: Diethard Jansen, 16-9-2018
"""
from builtins import str
from builtins import object
from qgis.core import QgsGeometry, QgsVectorLayer
import os, sys
from . import imkl, basis

WIN = "startfile" in dir(os)
Ubuntu = os.environ.get('GNOME_DESKTOP_SESSION_ID') != None

PY3 = sys.version_info[0] >= 3
if PY3:
    def cmp(a, b):
        return (a > b) - (a < b)
    # mixin class for Python3 supporting __cmp__
    class PY3__cmp__:   
        def __eq__(self, other):
            return self.__cmp__(other) == 0
        def __ne__(self, other):
            return self.__cmp__(other) != 0
        def __gt__(self, other):
            return self.__cmp__(other) > 0
        def __lt__(self, other):
            return self.__cmp__(other) < 0
        def __ge__(self, other):
            return self.__cmp__(other) >= 0
        def __le__(self, other):
            return self.__cmp__(other) <= 0
else:
    class PY3__cmp__:
        pass

class Layer(PY3__cmp__):

    layerPriority=("GB_", "GP_", "SEL", "ET_", "PT_", "LG_" ,"MV_", "AN_")
    layerGroupNames= {"topo": ("GB_", "GP_", "SEL", "ET_", "PT_"),
                      "ligging": ("LG_",),
                      "maatvoering": ("MV_",),
                      "annotatie": ("AN_",)}
        
    def __init__(self, owner, raster_file_name = None):
        self.owner = owner
        self.__vectorType = None
        self.__layerFile = raster_file_name
        self.__layer = None # reference to realised layer in GIS
        self.__layerId = None # reference to layerID in GIS
        self.__featureIds = []
        self.__themes_visible = {} # visibility state of themes in layers
        self.__layerName = None # holds layername
        self.fields = []
        self.features = []
        self._setLayerNameFromFile()

# defining access to attributes of class Layer

    def _layerFile(self):
        """return private attribute file which holds filename"""
        return self.__layerFile

    layerFile = property(fget=_layerFile)

    def _vectorType(self):
        """return private attribute vectorType"""
        return self.__vectorType

    def _setVectorType(self, a_type):
        """set private attribute vectorType"""
        self.__vectorType = a_type

    vectorType = property(fget=_vectorType, fset=_setVectorType)

    def _layer(self):
        """return private attribute layer"""
        return self.__layer

    def _setLayer(self, layer):
        """set private attribute layer"""
        # set it only once
        if self.__layer is None:
            self.__layer = layer

    layer = property(fget=_layer, fset=_setLayer)

    def _layername(self):
        """return private attribute layerName"""
        return self.__layerName

    def _setLayername(self, layerName):
        """set private attribute layerName"""
        # set it only once
        self.__layerName = layerName

    layerName = property(fget=_layername, fset=_setLayername)

    def _layerId(self):
        """ get private attribute layer id"""
        return self.__layerId

    def _setLayerId(self, layerId):
        self.__layerId = layerId

    layerId = property(fget=_layerId, fset=_setLayerId)

    def _featureIds(self):
        """ get feature ids from private features"""
        return self.__featureIds

    featureIds = property(fget=_featureIds)

    def _themes_visible(self):
        """returns private attribute themes_visible"""
        return self.__themes_visible

    themes_visible = property(fget=_themes_visible)

# special methods of class Layer
    def __repr__(self):
        """Simple presentation of class Layer"""
        return "Layer('%s')" % (self.layerName)
    
    def __cmp__(self, other):
        """sort layers on vector/raster, for raster on prefix name for
        vector on geometry and when they are the same on name.
        """
        if other is None:
            return 1
        # raster below vector
        if self.is_vector() and not other.is_vector():
            return 1
        if not self.is_vector() and other.is_vector():
            return -1
        # same type... both vector or raster
        this_name = self.layerName
        other_name = other.layerName
        this_index = 0
        other_index = 0
        # when vector point above line above area
        if self.is_vector():
            geometry_types = basis.B_Field.GEOMETRY_TYPES
            this_index = geometry_types.index(self.vectorType)
            other_index = geometry_types.index(other.vectorType)
        else:
            index=0
            for compareStr in self.layerPriority:
                if this_name.startswith(compareStr):
                    this_index = index
                if other_name.startswith(compareStr):
                    other_index = index
                index += 1
        if this_index > other_index:
            return 1
        elif this_index < other_index:
            return -1
        elif this_name < other_name:
            return 1
        elif this_name > other_name:
            return -1
        else:
            return 0

    def _setLayerNameFromFile(self):
        """set layer namer from filename without path"""
        layerFile = self.layerFile
        if self.layerName is None:
            if layerFile is not None:
                seperator = '/'
                if seperator not in layerFile:
                    seperator = '\\'
                if seperator in layerFile:
                    i = layerFile.rindex(seperator)
                    self.layerName = layerFile[i+1:]
                else:
                    self.layerName = layerFile

# Public methods of class Layer
    def is_vector(self):
        return self.vectorType is not None

    def _iface(self):
        return self.owner.iface

    def load(self):
        """
        loads layer and set attributes layer, layer_id & visible 
        """
        iface = self._iface()
        layer = None
        if iface != None:
            layer = iface.layerByName(self.layerName)
            if layer is None:
                layer = iface.addLayer(self)
            
        if layer is not None:
            self.layer = layer
            self.layerName = layer.name()
            self.layerId = layer.id()
            features = iface.addFeatures(self)
            if features:
                feature_ids = [feature.id() for feature in features]
                self.__featureIds = feature_ids
            self.__visible = True

    def addVisibility(self, theme_name):
        if theme_name not in self.themes_visible:
            self.themes_visible[theme_name] = 2
        
    def setVisibility(self, visibility, show_raster, show_vector, theme):
        """
        visibility = 0 or 2 (all visible) to change visibility in
        set of themes
        """
        theme_name = theme.name
        iface = self._iface()
        if iface is None or visibility == 1:
            return
        if theme_name in list(Layer.layerGroupNames.keys()):
            # keys in themes_visibile are different from
            # incoming group_theme_name. Just set the visibility
            # of whole layer on or off.
            for i_theme_name in list(self.themes_visible.keys()):
                self._setVisibilityTheme(visibility, show_raster, show_vector,
                                         i_theme_name)
        elif theme_name in self.themes_visible:
            self._setVisibilityTheme(visibility, show_raster, show_vector,
                                     theme_name)

    def _setVisibilityTheme(self, visibility, show_raster, show_vector,
                            theme_name):
        iface = self._iface()
        visible = self.isVisible(theme_name)
        if visible != visibility:
            iface.setVisibilityForLayer(self, visibility, show_raster,
                                        show_vector, theme_name)
            self.themes_visible[theme_name] = visibility

    def visible(self, theme_name):
        """
        return 2 (all visible) if all values of cached theme_visibilities
        are also 2, 0 is all not visible and 1 when some are visible.
        """
        visible = None
        if theme_name in list(Layer.layerGroupNames.keys()):
            visible = self._allVisible()
        else:
            visible = self.themes_visible[theme_name]
        return visible

    def isVisible(self, theme_name):
        """
        Checks if layer is visible, sets private __visible
        and returns boolean layer is visible or not
        """
        visible = None
        if theme_name in list(Layer.layerGroupNames.keys()):
            visible = self._areAllVisible()
        else:
            visible = self._isVisible(theme_name)
        return visible
        
    def _isVisible(self, theme_name):
        """
        Checks if layer is visible, sets private __visible
        and returns boolean layer is visible or not
        """
        visible = 0
        iface = self._iface()
        if iface != None:
            visible = iface.visibilityForLayer(self, theme_name)
            self.themes_visible[theme_name] = visible
        return visible

    def _areAllVisible(self):
        for theme in list(self.themes_visible.keys()):
            self._isVisible(theme)
        visible = self._allVisible()
        return visible

    def _allVisible(self):
        visible = 0
        n_themes = 0
        value_visible = 0
        for value in list(self.themes_visible.values()):
            if value is not None:
                n_themes += 1
                value_visible += value
        if n_themes > 0:
            visible = int(value_visible / n_themes)
        return visible

    def goto(self):
        """
        goto bounds of layer
        the interface of Doc is used.
        """
        iface = self._iface()
        if iface != None:
            iface.gotoLayer(self)

    def remove(self):
        """
        remove layer from mapRegistry
        this will in fact remove the layer from QGIS
        """
        iface = self._iface()
        if iface != None:
            iface.removeLayer(self)

    def bestScale(self):
        """
        Set best scale for layer 
        """
        iface = self._iface()
        if iface != None:
            iface.bestScale(self)

    def groupName(self):
        """
        returns name of group this layer belongs to being one of
        Ligging, Maatvoering, Annotatie or Topo
        """
        group_name = ""
        layer_name = self.layerName
##        print "layer_name:", layer_name
        if self.vectorType:
            if layer_name in ('Annotatie', 'Maatvoering'):
                group_name = layer_name.lower()
            elif layer_name =='EigenTopografie':
                group_name = 'topo'
            else:
                group_name = 'ligging'
        else:
            prefix = layer_name[:3]
            for groupName, prefixes in self.layerGroupNames.items():
                if prefix in prefixes:
                    group_name = groupName
                    break
        return group_name

    def qgisVectorType(self):
        qgisVectorTypes = {'POLYGON': 'Polygon',
                           'LINESTRING': 'LineString',
                           'MULTILINESTRING': 'MultiLineString',
                           'POINT': 'Point'}
        return qgisVectorTypes[self.vectorType]
        

class Coord(object):
    def __init__(self, p_x=0, p_y=0):
        """Initialises new instance of Coord with optional x & y value
        """
        self.x = p_x
        self.y = p_y
        
    def __repr__(self):
        """"Return string representation of Coord"""
        return "Coord(%.2f, %.2f)" % (self.x, self.y)

class Rectangle(object):
    """Class which represents rectangular area which hold
    position of rasters in the world. Used to create contents of
    worldfile that will be created next to each rasterfile.
    """

# following shared template needs to be completed with following values
# x1, pixel_width,0 ,y2 ,0 -pixel_height
    worldFileTemplate = '<PAMDataset>\
<SRS>PROJCS["Amersfoort / RD New",GEOGCS["Amersfoort",\
DATUM["Amersfoort",SPHEROID["Bessel 1841",377397.155,299.1528128,\
AUTHORITY["EPSG","7004"]],AUTHORITY["EPSG","6289"]],PRIMEM["Greenwich",0,\
AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,\
AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4289"]],UNIT["metre",\
AUTHORITY["EPSG","9001"]],\
PROJECTION["Oblique_Stereographic"],\
PARAMETER["latitude_of_origin",52.15616055555555],\
PARAMETER["central_meridian",5.387638888888889],\
PARAMETER["scale_factor",0.9999079],\
PARAMETER["false_easting",155000],\
PARAMETER["false_northing",463000],\
AUTHORITY["EPSG","28992"],AXIS["X",EAST],\
AXIS["Y",NORTH]]</SRS>\
<GeoTransform> %8.2f, %e, 0, %8.2f, 0,%e</GeoTransform>\
<PAMRasterBand band="1"><NoDataValue>255</NoDataValue>\
</PAMRasterBand></PAMDataset>'
    
    def __init__(self, lowerLeftCoord=Coord(), upperRightCoord=Coord()):
        """Initialises new instance of Rectangle with optional lowerLeftCoord
        & upperRightCoord
        """
        self.lowerLeftCorner = lowerLeftCoord
        self.upperRightCorner = upperRightCoord
        self.pixelsWidth = None
        self.pixelsHeight = None

    def __repr__(self):
        """Represenation of rectangle that can be used to reproduce object"""
        return "Rectangle(%s, %s)" % (self.lowerLeftCorner,
                                      self.upperRightCorner)

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
    
    
class Company(object):
    def __init__(self, name=None):
        """Company which represents the netowner.
        The netowner provide all information, including contactpersons
        rasters with positions of pipeline, pdf's with accompanying letters
        additional drawings etcetera...
        """
        self.bronhoudercode = None
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

    def get_theme(self, name):
        for theme in self.themes:
            if theme.name == name:
                return theme
        return None

    def process_imkl_object(self, imkl_object):
        name = imkl_object.name
        if name == 'Beheerder':
            organisation = imkl_object.field("organisatie").value[0]
            self.name = organisation.field("naam").value
            self.bronhoudercode = imkl_object.field("bronhoudercode").value
        elif name == 'Belang':
            contactAanvraag = imkl_object.field("contactAanvraag").value
            contactBeschadiging = imkl_object.field("contactBeschadiging").value
            contactNetinformatie = imkl_object.field("contactNetinformatie").value
            if contactAanvraag is not None:
                contact = contactAanvraag.field("aanvraagSoortContact").value
                person = Person()
                person.process_imkl_object(contact)
                self.contactPerson = person
            if contactBeschadiging is not None:
                contact = contactBeschadiging.field("contact").value
                self.telNrDamage = contact.field("telefoon").value
            if contactNetinformatie is not None:
                contact = contactNetinformatie.field("aanvraagSoortContact").value
                self.telNrProblemIT = contact.field("telefoon").value
            
class Person(object):
    def __init__(self, name=None):
        """Person which can be a contactperson from the netowner.
        It can hold information like name/email/telnr/fax
        """
        self.name = name
        self.telephone = None
        self.email = None
        self.fax = None

    def __repr__(self):
        return "Person('%s')" % self.name

    def process_imkl_object(self, imkl_object):
        self.name = imkl_object.field("naam").value
        self.telephone = imkl_object.field("telefoon").value
        self.email = imkl_object.field("email").value

class Theme(object):
    
    def __init__(self, p_owner, p_name=None):
        """Theme presenting a kind of network, like water or datatransport
        Holds also information if supervision is neccesary during works i.e.
        for Gas pipelines and information on supervisor that will attend.
        """
        self.owner = p_owner
        self.__name = None
        self.__visible = 0
        self.supervisionNecessary = None
        self.supervisors = []
        self.layers = []
        self.pdf_docs = []
        self.name = p_name

    def __repr__(self):
        return "Theme('%s')" % self.name

    def _visible(self):
        """return private attribute visible"""
        return self.__visible

    visible = property(fget=_visible)

    def _name(self):
        """return private attribute name"""
        return self.__name

    def _setName(self, name):
        """set private attribute name"""
        # Themename influences behaviour, make it uniform
        # take out spaces symbols etc. and convert to lowercase
        if name is not None:
            name = [c for c in name if c.isalpha()]
            name = ''.join(name).lower()
        self.__name = name

    name = property(fget=_name, fset=_setName)

    def checkVisible(self, p_actual=False):
        """
        p_actual, optional argument if true visibility
        of layers belonging to theme is actually checked otherwise
        recorded visible state of layers is used.
        """
        owner = self.owner
        show_raster = owner.showRaster
        show_vector = owner.showVector
        state = 0
        visible = 0
        theme_name = self.name
        visibilities = []
        for layer in self.layers:
            check_vector_only = show_vector and layer.is_vector()
            check_raster_only = show_raster and not show_vector and not layer.is_vector()
            if check_vector_only or check_raster_only:
                if p_actual:
                    visible = layer.isVisible(theme_name)
                else:
                    visible = layer.visible(theme_name)
                visibilities.append(visible)
        if all(visibilities):
            state = 2
        elif any(visibilities):
            state = 1
        else:
            state = 0
        return state

    def setVisibility(self, p_visibility, isVector=None):
        """
        p_visibility = 0 or 2 used to set same visibility for  
        this theme (all on or all off!)
        """
        owner = self.owner
        iface = owner.iface
        show_raster = owner.showRaster
        show_vector = owner.showVector
        if iface != None:
            iface.doRendering(False)
            for i_layer in self.layers:
                if isVector is None or i_layer.is_vector() == isVector:
                    i_layer.setVisibility(p_visibility, show_raster,
                                          show_vector, self)
            iface.doRendering(True)
            
        # refresh state of visibility and return!
        # Result value should be 0 (all off) or 2 (all on)
        return self.checkVisible()

class PdfFile(PY3__cmp__):
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
        global WIN, Ubuntu
        l_file = self.filePath
        if WIN:
            os.startfile(l_file)
        elif Ubuntu:
            os.system('gnome-open %s' % l_file)
        else:
            os.system('open %s' % l_file)

class LayerGroup(object):
    def __init__(self, name=None):
        """
        Layer group holds information on name and groupIndex
        """
        self.name = name
        self.index = None

    def __repr__(self):
        return "LayerGroup('%s')" % self.name
