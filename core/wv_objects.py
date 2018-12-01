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
from qgis.core import QgsGeometry, QgsVectorLayer
import imkl, basis, os

WIN = "startfile" in dir(os)
Ubuntu = os.environ.get('GNOME_DESKTOP_SESSION_ID') != None

class Layer:

    layerPriority=("GB_", "SEL", "ET_", "PT_", "LG_" ,"MV_", "AN_")
    layerGroupNames= {"Topo": ("GB_", "SEL", "ET_", "PT_"),
                      "Ligging": ("LG_",),
                      "Maatvoering": ("MV_",),
                      "Annotatie": ("AN_",)}
        
    def __init__(self, owner, raster_file_name = None):
        self.owner = owner
        self.__vectorType = None
        self.__file = raster_file_name
        self.__layer = None # reference to realised layer in GIS
        self.__layerId = None # reference to layerID in GIS
        self.__themes_visible = {} # visibility state of themes in layers
        self.__layerName = None # holds layername
        self.fields = []
        self.features = []
        self._setLayerNameFromFile()

# defining access to attributes of class Layer

    def _layerFile(self):
        """return private attribute file which holds filename"""
        return self.__file

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

    def _setLayername(self, layer):
        """set private attribute layerName"""
        # set it only once
        if self.__layerName == None:
            self.__layerName = layerName

    layerName = property(fget=_layername, fset=_setLayername)

    def _layerId(self):
        """ get private attribute layer id"""
        return self.__layerId

    layerId = property(fget=_layerId)

    def _themes_visible(self):
        """returns private attribute themes_visible"""
        return self.__themes_visible

    themes_visible = property(fget=_themes_visible)

# special methods of class Layer
    def __repr__(self):
        """Simple presentation of class Layer"""
        return "Layer('%s')" % (self.layerName())
    
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

    def addVisibility(self, theme_name):
        if not self.themes_visible.has_key(theme_name):
            self.themes_visible[theme_name] = False
        
    def setVisibility(self, pVisibility, theme_name):
        """
        p_visibility = boolean used to set this layer 
        change visibility in set of layers
        """
        if not self.themes_visible.has_key(theme_name):
            return
        iface = self.owner.iface
        l_visible = self.isVisible()
        if iface != None and l_visible != pVisibility:
            iface.setVisibilityForLayer(self, pVisibility, theme_name)
            self.themes_visible[theme_name] = pVisibility

    def isVisible(self, theme_name):
        """
        Checks if layer is visible, sets private __visible
        and returns boolean layer is visible or not
        """
        visible = None
        iface = self.owner.iface
        if iface != None:
            if theme_name is None:
                # check all themes!
                for theme_name in self.themes_visible.keys():
                    visible = iface.visibilityForLayer(self, theme_name)
                    self.themes_visible[theme_name] = visible
                visible = self._all_themes_visible()
            else:
                visible = iface.visibilityForLayer(self, theme_name)
                self.themes_visible[theme_name] = visible
        return visible

    def visible(self, theme_name):
        """
        return true if all values of cached theme_visibilities are true,
        otherwise false.
        """
        visible = None
        if theme_name is None:
            visible = self._all_themes_visible()
        else:
            visible = self.themes_visible[theme_name]
        return visible

    def _all_themes_visible(self):
        visible = None
        n_themes = len(self.themes_visible)
        values_visible = [value for value in self.themes_visible.values()]
        n_visible = values_visible.count(True)
        if n_visible == 0:
            visible = False
        elif n_visible == n_themes:
            visible = True
        return visible

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
        group_name = ""
        layer_name = self.layerName
##        print "layer_name:", layer_name
        if self.vectorType:
            if layer_name in ('Annotatie', 'Maatvoering'):
                group_name = layer_name
            elif layer_name =='EigenTopografie':
                group_name = 'Topo'
            else:
                group_name = 'Ligging'
        else:
            prefix = layer_name[:3]
            for groupName, prefixes in self.layerGroupNames.iteritems():
                if prefix in prefixes:
                    group_name = groupName
                    break
        return group_name

    def qgisVectorType(self):
        qgisVectorTypes = {'POLYGON': 'Polygon',
                           'LINESTRING': 'LineString',
                           'POINT': 'Point'}
        return qgisVectorTypes[self.vectorType]
        

class Coord:
    def __init__(self, p_x=0, p_y=0):
        """Initialises new instance of Coord with optional x & y value
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
            
class Person:
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

class Theme:
    visibilities = ("None", "Some", "All")
    
    def __init__(self, p_owner, p_name=None):
        """Theme presenting a kind of network, like water or datatransport
        Holds also information if supervision is neccesary during works i.e.
        for Gas pipelines and information on supervisor that will attend.
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
##        l_len = len(self.layers)
        l_len = 0
        l_nVisible = 0
        l_visible = 0
        # using True == 1 for addition!
        theme_name = self.name
        # when it is a group name, check if layer is completely visible
        if theme_name in Layer.layerGroupNames.keys():
            theme_name = None
        is_visible = None 
        for i_layer in self.layers:
            if p_actual:
                is_visible = i_layer.isVisible(theme_name)
            else:
                is_visible = i_layer.visible(theme_name)
            if is_visible is None:
                continue
                l_len += 1
                l_nVisible += is_visible
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
            i_layer.setVisibility(p_visibility, self)
        if iface != None:
            iface.doRendering()
            iface.refreshMap()
            
        # refresh state of visibility and return!
        # Result value should be 0 (all off) or 2 (all on)
        return self.checkVisible()

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
        global WIN, Ubuntu
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
    import os, wv
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
